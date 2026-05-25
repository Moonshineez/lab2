import base64
from datetime import datetime
from urllib.parse import urlparse

history = []
current_index = -1

def get_domain(url):
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    return parsed.netloc

def add_page():
    global current_index, history

    url = input("Введите URL: ")
    bookmark_input = input("Это закладка? да/нет: ")

    is_bookmark = bookmark_input.lower() == "да"

    if current_index < len(history) - 1:
        history = history[:current_index + 1]

    record = {
        "url": url,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bookmark": is_bookmark
    }

    history.append(record)
    current_index = len(history) - 1

    print("Страница добавлена.")

def go_back():
    global current_index

    if len(history) == 0:
        print("История пуста.")
    elif current_index == 0:
        print("Назад идти нельзя.")
    else:
        current_index -= 1
        print("Текущая страница:")
        print(history[current_index])

def go_forward():
    global current_index

    if len(history) == 0:
        print("История пуста.")
    elif current_index == len(history) - 1:
        print("Вперёд идти нельзя.")
    else:
        current_index += 1
        print("Текущая страница:")
        print(history[current_index])

def clear_history():
    global current_index, history

    history.clear()
    current_index = -1
    print("История очищена.")

def search_by_domain():
    if len(history) == 0:
        print("История пуста.")
        return

    domain = input("Введите домен для поиска: ")

    found = False

    for record in history:
        if domain in get_domain(record["url"]):
            print(record)
            found = True

    if not found:
        print("Ничего не найдено.")

def save_to_file():
    filename = input("Введите имя файла: ")

    with open(filename, "w", encoding="utf-8") as file:
        for record in history:
            line = record["url"] + "|" + record["time"] + "|" + str(record["bookmark"])
            encoded_line = base64.b64encode(line.encode("utf-8")).decode("utf-8")
            file.write(encoded_line + "\n")

    print("История сохранена в файл.")

def load_from_file():
    global current_index, history
    
    filename = input("Введите имя файла для загрузки: ")
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            new_history = []
            for line in file:
                line = line.strip()
                if not line:
                    continue
                decoded = base64.b64decode(line).decode("utf-8")
                url, time_str, bookmark = decoded.split("|")
                new_history.append({
                    "url": url,
                    "time": time_str,
                    "bookmark": bookmark == "True"
                })
            history = new_history
            current_index = len(history) - 1 if history else -1
            print("История загружена из файла.")
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print("Ошибка при загрузке файла:", e)

def top_transitions():
    if len(history) < 2:
        print("Недостаточно записей.")
        return

    n = int(input("Введите N: "))

    transitions = {}

    for i in range(len(history) - 1):
        domain1 = get_domain(history[i]["url"])
        domain2 = get_domain(history[i + 1]["url"])

        transition = domain1 + " -> " + domain2

        if transition not in transitions:
            transitions[transition] = 1
        else:
            transitions[transition] += 1

    sorted_transitions = sorted(
        transitions.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Топ переходов:")

    for i in range(min(n, len(sorted_transitions))):
        print(sorted_transitions[i][0], "-", sorted_transitions[i][1], "раз(а)")

def show_history():
    if len(history) == 0:
        print("История пуста.")
        return

    for i in range(len(history)):
        mark = ""

        if i == current_index:
            mark = "<-- текущая"

        print(i + 1, history[i], mark)

def menu():
    while True:
        print("\n--- История браузера ---")
        print("1. Добавить страницу")
        print("2. Назад")
        print("3. Вперёд")
        print("4. Очистить историю")
        print("5. Поиск по домену")
        print("6. Показать историю")
        print("7. Сохранить в Base64-файл")
        print("8. Загрузить из Base64-файла")
        print("9. Топ-N переходов")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_page()
        elif choice == "2":
            go_back()
        elif choice == "3":
            go_forward()
        elif choice == "4":
            clear_history()
        elif choice == "5":
            search_by_domain()
        elif choice == "6":
            show_history()
        elif choice == "7":
            save_to_file()
        elif choice == "8":
            load_from_file()
        elif choice == "9":
            top_transitions()
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню.")

menu()

