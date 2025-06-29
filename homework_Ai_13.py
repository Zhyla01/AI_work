# (Завдання_1)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
api_key_serper = os.getenv('SERPER_API_KEY')

llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    google_api_key=api_key,
)

searcher = GoogleSerperAPIWrapper(api_key_serper=api_key_serper, type="places")

def restaurant_recommendation_func(query: str) -> str:
    result = searcher.results(query)

    if 'places' not in result or not result['places']:
        return "немає відповідної інформації"

    output = ""
    for place in result['places']:
        title = place.get('title', 'Невідомо')
        website = place.get('website', 'немає')
        rating = place.get('rating', 'немає')
        output += f"Назва: {title}\nСайт: {website}\nРейтинг: {rating}\n\n"

    return output.strip()

restaurant_tool = Tool.from_function(
    func=restaurant_recommendation_func,
    name="restaurant_recommender",  # Ім’я має бути валідним для Google Gemini
    description="Пошук ресторанів за запитом користувача (наприклад: 'ресторан Львів піца')."
)

agent = create_react_agent(
    model=llm,
    tools=[restaurant_tool]
)

messages = {
    "messages": [
        SystemMessage(
            """
            Ти чат-бот, який допомагає рекомендувати ресторани.
            Твоя задача — отримати від користувача запит для пошуку ресторанів
            і видати перелік ресторанів з назвою, посиланням на сайт (якщо є)
            та рейтингом. Якщо запит не про ресторан або місце — виведи повідомлення:
            «немає відповідної інформації».
            Кожен ресторан виводь з нового рядка у такому форматі:
            Назва: ...
            Сайт: ...
            Рейтинг: ...
            """
        )
    ]
}

while True:
    user_input = input("Ви: ").strip()
    if not user_input:
        break

    messages["messages"].append(HumanMessage(user_input))
    messages = agent.invoke(messages)

    ai_message = messages["messages"][-1]
    print("\nБот:")
    print(ai_message.content)

