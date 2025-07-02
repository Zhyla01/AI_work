# (Завдання_1)

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import os
import dotenv
import json
from uuid import uuid4

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',  # або 'gemini-1.5-pro' якщо підтримується
    google_api_key=api_key
)

pc = Pinecone(api_key=pinecone_api_key)
index_name = "task1"

existing_indexes = [idx.name for idx in pc.list_indexes().indexes]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

huge_file_path = "data/lesson_rag/huge_file.txt"

if os.path.exists(huge_file_path):
    with open(huge_file_path, "r", encoding="utf-8") as f:
        huge_text = f.read()

    raw_blocks = huge_text.split("\n\n\n")
    blocks = [b.strip() for b in raw_blocks if b.strip()]

    docs = []
    doc_ids = []
    id_data = {}

    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue
        block_title = lines[0].strip()
        content = "\n".join(lines).strip()
        doc = Document(
            page_content=content,
            metadata={
                "file_path": huge_file_path,
                "block_title": block_title
            }
        )
        docs.append(doc)
        new_id = str(uuid4())
        doc_ids.append(new_id)
        file_name = os.path.basename(huge_file_path)
        key_name = f"{file_name} | {block_title}"
        id_data[key_name] = new_id

    json_path = "data_ai.json"
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as jf:
            existing_data = json.load(jf)
    else:
        existing_data = {}

    existing_data.update(id_data)

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(existing_data, jf, indent=2, ensure_ascii=False)

    vector_store.add_documents(docs, ids=doc_ids)
    print(f"Додано {len(docs)} блоків з huge_file.txt до векторної бази.")
else:
    print("Файл huge_file.txt не знайдено. Пропускаємо додавання.")

def doc_ser(user_text: str):
    """
    Повертає список релевантних документів до запиту користувача.
    """
    print("Виконується пошук документів...")
    docs = vector_store.similarity_search(user_text, k=2)
    for i, doc in enumerate(docs, start=1):
        print(f"Документ {i}: {doc.metadata.get('block_title')}")
    return docs

agent = create_react_agent(
    model=llm,
    tools=[doc_ser]
)

messages = {
    "messages": [
        SystemMessage(content="""
        Ти чат-бот, який відповідає на питання про штучний інтелект.
        Спочатку спробуй знайти відповіді у документах через 'doc_ser'.
        Якщо не знайдеш — дай відповідь сам.
        """)
    ]
}

while True:
    try:
        user_input = input("Ви: ")
        if user_input.strip() == '':
            print("Завершення чату.")
            break

        user_message = HumanMessage(content=user_input)
        messages["messages"].append(user_message)

        messages = agent.invoke(messages)
        ai_message = messages["messages"][-1]
        print("Бот:", ai_message.content)

    except KeyboardInterrupt:
        print("\nЧат завершено вручну.")
        break
    except Exception as e:
        print("Сталася помилка:", str(e))
