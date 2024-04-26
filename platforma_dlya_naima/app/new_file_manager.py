import json
from app.test_gigachat_service import send_prompt, parse_response, get_answers
import pandas as pd

class NewJsonFileManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._read_json()

    def _read_json(self):
        """Чтение JSON файла в словарь."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("FileNotFoundError")
            return {}  # Возвращает пустой словарь, если файл не найден
        except json.JSONDecodeError:
            print("JSONDecodeError")
            return {}  # Возвращает пустой словарь, если файл пуст или не корректен

    def save_json(self):
        """Сохранение словаря обратно в JSON файл."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
    
    def get_data_by_theme(self, theme, num_questions):
        test = self.data.get(theme)
        if test is None:
            df = pd.DataFrame(columns=['numbers', 'question', 'giga_answer', 'exact_answer', 'similarity'])
            answer = send_prompt(f'Сгенерируй {num_questions} тестовых вопросов по {theme}, которые можно задать на собеседовании. В качестве ответа выведи только вопросы')
            df = parse_response(answer, df)
            df = get_answers(df)
            return {row['question']: row['giga_answer'] for _, row in df.iterrows()}
        else:
            return test
    
    def add_question(self, theme, question, answer):
        """Добавление записи в словарь."""
        self.data[theme][question] = answer

    def add_questions(self, theme, test):
        self.data[theme] = test
