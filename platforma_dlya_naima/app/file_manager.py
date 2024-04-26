import json


class JsonFileManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._read_json()

    def _read_json(self):
        """Чтение JSON файла в словарь."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Возвращает пустой словарь, если файл не найден
        except json.JSONDecodeError:
            return {}  # Возвращает пустой словарь, если файл пуст или не корректен

    def add_record(self, key, value):
        """Добавление записи в словарь."""
        self.data[key] = value

    def save_json(self):
        """Сохранение словаря обратно в JSON файл."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def get_data_by_id(self, id):
        for key, value in self.data.items():
            if value['id'] == id:
                return value
        return None

    def get_data_by_key(self, key):
        return self.data[key]


# Использование класса
if __name__ == "__main__":
    # Создайте объект класса с указанием пути к вашему JSON файлу
    manager = JsonFileManager('path/to/your/file.json')

    # Добавление данных
    manager.add_record('new_key', 'new_value')

    # Сохранение данных в файл
    manager.save_json()
