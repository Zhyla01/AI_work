# (Завдання_1)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.messages import SystemMessage, HumanMessage

import dotenv
import os

# Завантаження .env та API ключа
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Ініціалізація LLM
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=api_key
)

# --------------- ЛАНЦЮГ 1: Генерація вправ -----------------

# Схема для парсингу списку вправ
schema_chain1 = [
    ResponseSchema(name="exercises", description="список вправ для досягнення мети тренування")
]
parser_chain1 = StructuredOutputParser.from_response_schemas(schema_chain1)
instructions1 = parser_chain1.get_format_instructions()

prompt_exercise_list = PromptTemplate.from_template(
    """
    Твоя задача — скласти список вправ залежно від мети тренування.

    Мета: {goal}

    Формат відповіді:
    {instructions}
    """,
    partial_variables={"instructions": instructions1}
)

# Ланцюг 1
chain_exercise_list = prompt_exercise_list | llm | parser_chain1

# --------------- ЛАНЦЮГ 2: План тренувань -----------------

schema_chain2 = [
    ResponseSchema(name="plan", description="детальний план тренувань на тиждень")
]
parser_chain2 = StructuredOutputParser.from_response_schemas(schema_chain2)
instructions2 = parser_chain2.get_format_instructions()

prompt_training_plan = PromptTemplate.from_template(
    """
    На основі списку вправ склади детальний тижневий план тренувань.

    Список вправ: {exercises}
    Рівень підготовки: {level}
    Час на тиждень: {hours} годин

    Формат відповіді:
    {instructions}
    """,
    partial_variables={"instructions": instructions2}
)

# Ланцюг 2
chain_training_plan = prompt_training_plan | llm | parser_chain2

# ---------------- Інтерактивна частина -----------------

# Отримати мету від користувача
user_goal = input("Введіть вашу мету (наприклад: схуднення, набір м'язів): ")

# Генеруємо список вправ
result_chain1 = chain_exercise_list.invoke({"goal": user_goal})
exercises = result_chain1.get("exercises")
print("\nСписок рекомендованих вправ:")
print(exercises)

# Отримати додаткові параметри
user_level = input("\nВведіть ваш рівень підготовки (низький / середній / професіонал): ").lower()
user_hours = input("Скільки годин на тиждень ви готові тренуватись? ")

# Генеруємо план тренувань
result_chain2 = chain_training_plan.invoke({
    "exercises": exercises,
    "level": user_level,
    "hours": user_hours
})

plan = result_chain2.get("plan")
print("\nВаш персональний план тренувань на тиждень:")
print(plan)
