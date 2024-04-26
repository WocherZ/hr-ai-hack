from gigachat import GigaChat
import pandas as pd
import re
from dotenv import load_dotenv
import os

load_dotenv()

def send_prompt(prompt):
    with GigaChat(access_token=os.environ['GIGACHAT_TOKEN'], verify_ssl_certs=False, model="GigaChat-Pro", base_url=os.environ['GIGACHAT_BASE_URL']) as giga:
        response = giga.chat(prompt)
        return response.choices[0].message.content
    
def parse_response(response, df):
    pattern = r'(\d+)\.\s*(.+)'

    numbers = []
    questions = []

    matches = re.findall(pattern, response)
    for match in matches:
        numbers.append(match[0])
        questions.append(match[1])

    df['numbers'] = numbers
    df['question'] = questions

    return df

def get_answers(df):
    for index, row in df.iterrows():
        if pd.notna(row['giga_answer']):
            continue
        giga_answer = send_prompt("Ответь на вопрос" + row['question'])
        df.at[index, 'giga_answer'] = giga_answer
        
    return df

def execute_code(code):
    try:
        exec(code)
        print("Код успешно выполнен.")
    except Exception as e:
        print("Ошибка при выполнении кода:", e)

def rate_answers(df):
    for index, row in df.iterrows():
        question = row['question']
        giga_answer = row['giga_answer']
        rating = send_prompt(f"На вопрос: {question}. Получили ответ: {giga_answer}. Оцени ответ по 10-балльной шкале. В качестве ответа дай одно число")
        
        # Запись оценки в DataFrame
        df.at[index, 'similarity'] = rating
        
    return df