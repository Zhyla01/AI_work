
# Напишіть промпт для генерації коду функції для
# вирішення певної задачі.
# Вхідні параметри – мова програмування, опис задачі
# Реалізуйте двома способами:
#  Zero-shot
#  Few-shot


from langchain_google_genai import GoogleGenerativeAI

from langchain.prompts import PromptTemplate

import dotenv
import os

# завантажити api ключі з папки .env
dotenv.load_dotenv()

# отримати сам ключ
api_key = os.getenv('GEMINI_API_KEY')

llm = GoogleGenerativeAI(
    model='gemini-2.0-flash',  # назва моделі
    google_api_key=api_key,    # ваша API
)

# zero_shot_promt = PromptTemplate.from_template(
#     """Ти помічник для написання коду - твоя задача полягає написати функцію мовою яка виконує певне завдання яке вкаже користувач
#
#     Мова програмування: {lang}
#     Завдання: {task}""")
#
# lang = input("Введіть певну мову програмування ")
# task = input("Введіть завдання ")
#
# zero_chain = zero_shot_promt | llm
# result = zero_chain.invoke({"lang": lang, "task": task})
# print(result)

few_shot_promt = PromptTemplate.from_template(
    """Ти помічник для написання коду - твоя задача полягає написати функцію мовою яка виконує певне завдання яке вкаже користувач
    
    Приклади: 
    Мова програмування: Python
    Завдання: Знайти суму трьох чисел
    Відповідь: def get_sum(a, b, c):
  \"\"\"
  Знаходить суму трьох чисел.

  Args:
    a: Перше число.
    b: Друге число.
    c: Третє число.

  Returns:
    Суму трьох чисел.
  \"\"\"
  return a + b + c
  
    Мова програмування: {lang}
    Завдання: {task}
    Відповідь: """)

lang = input("Введіть певну мову програмування ")
task = input("Введіть завдання ")

few_chain = few_shot_promt | llm
result = few_chain.invoke({"lang": lang, "task": task})
print(result)

