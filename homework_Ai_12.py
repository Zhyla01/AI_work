# (Завдання_1)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import json
import dotenv
import os

# Завантажити API ключі з .env
dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Створення LLM моделі
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=api_key,
)

# Меню піци
MENU = {
    "Маргарита": {
        "маленька": {"ціна": 150, "см": 25},
        "велика": {"ціна": 190, "см": 35},
        "склад": "Томатний соус, моцарела, базилік"
    },
    "Пепероні": {
        "маленька": {"ціна": 160, "см": 25},
        "велика": {"ціна": 210, "см": 35},
        "склад": "Томатний соус, моцарела, пепероні"
    },
    "4 сири": {
        "маленька": {"ціна": 165, "см": 25},
        "велика": {"ціна": 225, "см": 35},
        "склад": "Моцарела, дорблю, пармезан, чеддер"
    },
    "Гавайська": {
        "маленька": {"ціна": 155, "см": 25},
        "велика": {"ціна": 218, "см": 35},
        "склад": "Томатний соус, моцарела, шинка, ананас"
    },
    "Вегетаріанська": {
        "маленька": {"ціна": 137, "см": 25},
        "велика": {"ціна": 198, "см": 35},
        "склад": "Томатний соус, моцарела, болгарський перець, гриби, оливки, кукурудза"
    }
}

# Ініціалізація замовлення
order = {}

# Схема для парсингу
schemas = [
    ResponseSchema(name='pizza', description='назва піци'),
    ResponseSchema(name='size', description='розмір піци (маленька / велика)')
]

parser = StructuredOutputParser.from_response_schemas(schemas)
instructions = parser.get_format_instructions()

prompt_extract = PromptTemplate.from_template(
    """
    Твоя задача — дістати назву піци і розмір із тексту замовлення.

    Текст: {text}

    Формат відповіді:
    {instructions}
    """,
    partial_variables={"instructions": instructions}
)

chain_extract = prompt_extract | llm | parser

# Меню у текстовому вигляді
menu_text = """
1. Маргарита
Томатний соус, моцарела, базилік.
Маленька 25 см — 150 грн, велика 35 см — 190 грн

2. Пепероні
Томатний соус, моцарела, пепероні.
Маленька 25 см — 160 грн, велика 35 см — 210 грн

3. 4 сири
Моцарела, дорблю, пармезан, чеддер.
Маленька 25 см — 165 грн, велика 35 см — 225 грн

4. Гавайська
Томатний соус, моцарела, шинка, ананас.
Маленька 25 см — 155 грн, велика 35 см — 218 грн

5. Вегетаріанська
Томатний соус, моцарела, болгарський перець, гриби, оливки, кукурудза.
Маленька 25 см — 137 грн, велика 35 см — 198 грн
"""

# Системне повідомлення
system_prompt = """
Ти — ввічливий чат-бот для замовлення піци. 

Твої функції:
- показати меню
- прийняти замовлення
- змінити замовлення
- підтвердити замовлення і показати загальну суму

Меню:
{menu}

Формат відповіді:
- Будь чемним.
- Використовуй дружній тон.
- Якщо треба показати меню — виведи його у зручному вигляді.
- Якщо замовлення прийнято — підтвердь його.
- Якщо підтверджено — виведи повне замовлення і суму.
"""

messages = [SystemMessage(system_prompt.format(menu=menu_text))]

# Тріммер для скорочення історії
trimmer = trim_messages(
    strategy='last',
    token_counter=len,
    max_tokens=5,
    start_on='human',
    end_on='human',
    include_system=True
)

# Основний цикл взаємодії
while True:
    user_input = input("Ви: ")
    if user_input.strip() == "":
        break

    messages.append(HumanMessage(user_input))
    messages = trimmer.invoke(messages)

    response = llm.invoke(messages)
    print(f"Бот: {response.content}")

    try:
        parsed = chain_extract.invoke({"text": response.content})
        pizza = parsed.get('pizza')
        size = parsed.get('size')
        if pizza in MENU and size in MENU[pizza]:
            order[pizza] = size
            print(f"Додано до замовлення: {pizza} ({size})")
    except Exception as e:
        pass  # тут можна додати логування помилок

    messages[0] = SystemMessage(system_prompt.format(menu=menu_text))
    messages.append(response)

    if "підтвердити" in user_input.lower():
        total = 0
        print("\nВаше замовлення:")
        for pizza_name, pizza_size in order.items():
            price = MENU[pizza_name][pizza_size]["ціна"]
            size_cm = MENU[pizza_name][pizza_size]["см"]
            print(f"- {pizza_name} ({pizza_size}, {size_cm} см) — {price} грн")
            total += price
        print(f"Загальна сума замовлення: {total} грн")



