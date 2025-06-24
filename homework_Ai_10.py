# (Завдання_1)

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate

import dotenv
import os

# Завантажити API ключі з .env
dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Перевірка наявності ключа
if not api_key:
    raise ValueError("API ключ не знайдено. Додайте GEMINI_API_KEY у файл .env")

# Створення моделі (LLM)
llm = GoogleGenerativeAI(
    model='gemini-1.5-flash',  # або gemini-1.5-pro, якщо маєш доступ
    google_api_key=api_key,
)

# Параметри курсу
topic = "Основи штучного інтелекту"
audience = "Старшокласники (15-17 років), які цікавляться сучасними технологіями, але не мають технічного бекграунду"

# === Zero-shot варіант ===

zero_shot_template = PromptTemplate.from_template("""
Створи детальний план навчального курсу на тему "{topic}".  
Цільова аудиторія: {audience}.  
Курс повинен включати модулі, теми кожного модуля, короткий опис кожного розділу, тривалість курсу та кінцеві результати навчання.  
Будь лаконічним, логічним та адаптуй стиль до рівня підготовки та потреб аудиторії.
""")

zero_prompt = zero_shot_template.format(topic=topic, audience=audience)

try:
    response_zero = llm.invoke(zero_prompt)
    print("=== Zero-shot варіант ===\n")
    print(response_zero)
except Exception as e:
    print(f"Помилка при генерації zero-shot відповіді: {e}")

# === Few-shot варіант ===

few_shot_template = PromptTemplate.from_template("""
Приклад плану курсу для теми "Основи графічного дизайну" для початківців:

Назва курсу: Основи графічного дизайну  
Цільова аудиторія: Початківці без досвіду  
Тривалість: 6 тижнів  
Модулі:
1. Вступ до дизайну — Що таке графічний дизайн, галузі застосування  
2. Основи композиції — Принципи візуального сприйняття  
3. Колір та типографіка — Основи кольорових схем, шрифти  
4. Робота з Canva та Figma — Практичні інструменти  
5. Практичне завдання — Створення постера  
6. Портфоліо та наступні кроки

Тепер створи подібний план для теми "{topic}"  
Цільова аудиторія: {audience}  
Сформуй курс у схожому стилі: модулі, опис, тривалість, результати навчання.
""")

few_prompt = few_shot_template.format(topic=topic, audience=audience)

try:
    response_few = llm.invoke(few_prompt)
    print("\n=== Few-shot варіант ===\n")
    print(response_few)
except Exception as e:
    print(f"Помилка при генерації few-shot відповіді: {e}")


