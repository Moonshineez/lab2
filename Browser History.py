import base64
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse

history = []
current_index = -1

def get_domain(url):
    if not url.startswith("http"):
        url = "https://" + url
    return urlparse(url).netloc

def add_page():
    global current_index, history

    url = input("Введите URL: ")
    bookmark_input = input("Это закладка? да/нет: ")
    is_bookmark = bookmark_input.lower() == "да"

   
    if current_index < len(history) - 1:
        history = history[:current_index + 1]

    history.append({
        "url": url,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bookmark": is_bookmark
    })
    current_index = len(history) - 1
    print("Страница добавлена.")

def navigate(direction):
    
    global current_index

    if not history:
        print("История пуста.")
        return

    new_index = current_index + direction
    if 0 <= new_index < len(history):
        current_index = new_index
        print("Текущая страница:", history[current_index])
    else:
        print("Вперёд идти нельзя." if direction == 1 else "Назад идти нельзя.")

def clear_history():
    global current_index
    history.clear()  # global не нужен, так как список мутирует clear(), а не переприсваивается
    current_index = -1
    print("История очищена.")

def search_by_domain():
    if not history:
        print("История пуста.")
        return

    domain = input("Введите домен для поиска: ")
    found = [record for record in history if domain in get_domain(record["url"])]

    if found:
        for record in found:
            print(record)
    else:
        print("Ничего не найдено.")

def save_to_file():
    filename = input("Введите имя файла: ")
    with open(filename, "w", encoding="utf-8") as file:
        for record in history:
            line = f"{record['url']}|{record['time']}|{record['bookmark']}"
            encoded_line = base64.b64encode(line.encode("utf-8")).decode("utf-8")
            file.write(encoded_line + "\n")
    print("История сохранена в файл.")

def top_transitions():
    if len(history) < 2:
        print("Недостаточно записей.")
        return

    try:
        n = int(input("Введите N: "))
    except ValueError:
        print("Ошибка: введите целое число.")
        return

    
    transitions = [
        f"{get_domain(history[i]['url'])} -> {get_domain(history[i+1]['url'])}"
        for i in range(len(history) - 1)
    ]
    
   
    print("Топ переходов:")
    for transition, count in Counter(transitions).most_common(n):
        print(f"{transition} - {count} раз(а)")

def show_history():
    if not history:
        print("История пуста.")
        return

    for i, record in enumerate(history):
        mark = "<-- текущая" if i == current_index else ""
        print(f"{i + 1} {record} {mark}".strip())

def menu():
   
    while True:
        print("\n--- История браузера ---")
        print("1. Добавить страницу\n2. Назад\n3. Вперёд\n4. Очистить историю")
        print("5. Поиск по домену\n6. Показать историю\n7. Сохранить в Base64-файл")
        print("8. Топ-N переходов\n0. Выход")

        choice = input("Выберите пункт: ")

        match choice:
            case "1": add_page()
            case "2": navigate(-1) 
            case "3": navigate(1)
            case "4": clear_history()
            case "5": search_by_domain()
            case "6": show_history()
            case "7": save_to_file()
            case "8": top_transitions()
            case "0": break
            case _: print("Неверный пункт меню.")

if __name__ == "__main__":
    menu()
