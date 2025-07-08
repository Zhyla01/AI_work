# (Завдання_1)

import os
import json
import dotenv
from uuid import uuid4

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

# Завантаження API ключів
dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

# Створення ембеддингів
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

# Підключення до Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index_name = "task1"

if not pc.has_index(index_name):
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

# Файл для збереження ID документів
json_path = "data_ai.json"

# Завантаження ID документів або ініціалізація пустого словника
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        id_data = json.load(f)
else:
    id_data = {}

def add_document_from_file(file_path: str):
    """Додає документ у векторну базу і зберігає ID"""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    doc = Document(page_content=text, metadata={"file_path": file_path})
    doc_id = str(uuid4())
    vector_store.add_documents([doc], ids=[doc_id])
    id_data[os.path.basename(file_path)] = doc_id
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(id_data, f)
    print(f"Документ '{file_path}' додано з ID: {doc_id}")

def doc_ser(user_text: str):
    """Пошук документів у векторній базі за текстом"""
    docs = vector_store.similarity_search(user_text, k=2)
    return docs

# Створення LLM моделі
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=api_key,
)

# Створення агента з інструментом пошуку
agent = create_react_agent(
    model=llm,
    tools=[doc_ser]
)

# Системне повідомлення
messages = {
    "messages": [
        SystemMessage(
            """
            Ти чат-бот який дає відповіді на запитання про штучний інтелект.
            Спочатку шукай інформацію через "doc_ser", якщо не знайшов відповідай самостійно.
            """
        )
    ]
}

def main():
    print("Векторна база даних — адмін-панель.")
    while True:
        print("\nОберіть дію:")
        print("1. Додати документ")
        print("2. Задати запит (пошук + чат)")
        print("3. Вийти")
        choice = input("Введіть номер: ").strip()

        if choice == "1":
            file_path = input("Введіть шлях до текстового файлу: ").strip()
            if os.path.isfile(file_path):
                add_document_from_file(file_path)
            else:
                print("Файл не знайдено.")
        elif choice == "2":
            user_input = input("Ви: ").strip()
            if user_input == "":
                print("Порожній запит.")
                continue
            messages["messages"].append(HumanMessage(user_input))
            messages = agent.invoke(messages)
            ai_message = messages["messages"][-1]
            print("AI:", ai_message.content)
        elif choice == "3":
            print("Вихід.")
            break
        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()