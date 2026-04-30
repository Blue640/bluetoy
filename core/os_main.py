import os
import sys
import time
import math
import random
import socket
import platform
import urllib.request
from datetime import datetime

# Проверка наличия нужной библиотеки для красивого интерфейса
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.progress import track, Progress
    from rich.columns import Columns
except ImportError:
    print("Критическая ошибка: не установлена библиотека 'rich'.")
    print("Пожалуйста, установите её командой: pip install rich")
    sys.exit(1)

# Инициализация консоли
console = Console()

# ==========================================
# КОНФИГУРАЦИЯ СИСТЕМЫ И ПЕРЕМЕННЫЕ
# ==========================================
OS_NAME = "BlueOS"
OS_VERSION = "2.5.0 Release"
AUTHOR = "Blue640"
SYSTEM_LANG = "RU"
USER = "root"

# Настройка виртуальной файловой системы (начинаем работу из папки data)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Если папки data нет, создаем её
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

# Текущая рабочая директория в ОС
CURRENT_DIR = DATA_DIR

# ==========================================
# СИСТЕМНЫЕ ФУНКЦИИ
# ==========================================

def clear_screen():
    """Очистка экрана (кроссплатформенная)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def boot_sequence():
    """Красивая анимация загрузки системы"""
    clear_screen()
    
    # Логотип при загрузке
    logo = f"""[bold blue]
    ██████╗ ██╗     ██╗   ██╗███████╗ ██████╗ ███████╗
    ██╔══██╗██║     ██║   ██║██╔════╝██╔═══██╗██╔════╝
    ██████╔╝██║     ██║   ██║█████╗  ██║   ██║███████╗
    ██╔══██╗██║     ██║   ██║██╔══╝  ██║   ██║╚════██║
    ██████╔╝███████╗╚██████╔╝███████╗╚██████╔╝███████║
    ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝[/]
    """
    console.print(logo, justify="center")
    console.print(f"[cyan]Версия ядра: {OS_VERSION}[/]", justify="center")
    print("\n")

    # Имитация загрузки драйверов и модулей
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Инициализация файловой системы...", total=100)
        task2 = progress.add_task("[blue]Загрузка сетевых драйверов...", total=100)
        task3 = progress.add_task("[white]Запуск графического интерфейса терминала...", total=100)

        while not progress.finished:
            progress.update(task1, advance=random.uniform(1, 5))
            progress.update(task2, advance=random.uniform(0.5, 3))
            progress.update(task3, advance=random.uniform(1, 4))
            time.sleep(0.05)
    
    time.sleep(0.5)
    clear_screen()

def show_neofetch():
    """Вывод системной информации в стиле neofetch"""
    logo = (
        "[bold blue]"
        "      ____  __           \n"
        "     / __ )/ /_  _____  \n"
        "    / __  / / / / / _ \\ \n"
        "   / /_/ / / /_/ /  __/ \n"
        "  /_____/_/\\__,_/\\___/  \n"
        "                        [/]"
    )
    
    sys_info = (
        f"[bold cyan]OS:[/] {OS_NAME} {OS_VERSION}\n"
        f"[bold cyan]Host OS:[/] {platform.system()} {platform.release()}\n"
        f"[bold cyan]Kernel:[/] Python {platform.python_version()}\n"
        f"[bold cyan]User:[/] {USER}\n"
        f"[bold cyan]Architecture:[/] {platform.machine()}\n"
        f"[bold cyan]Hostname:[/] {socket.gethostname()}\n"
        f"[bold cyan]Shell:[/] BlueShell Interactive"
    )
    
    panel = Panel(Columns([logo, sys_info], expand=True), title="System Information", border_style="blue")
    console.print(panel)

def display_help():
    """Отображение таблицы со всеми командами"""
    table = Table(title="Справочник команд BlueOS", style="blue", show_lines=True)
    table.add_column("Команда", style="cyan", no_wrap=True)
    table.add_column("Описание", style="white")
    table.add_column("Категория", style="magenta")

    # Файловая система
    table.add_row("pwd", "Показать текущую директорию", "Файлы")
    table.add_row("ls", "Показать содержимое папки", "Файлы")
    table.add_row("cd [папка]", "Перейти в другую папку (.. для выхода назад)", "Файлы")
    table.add_row("mkdir [имя]", "Создать новую папку", "Файлы")
    table.add_row("touch [имя]", "Создать пустой файл", "Файлы")
    table.add_row("rm [имя]", "Удалить файл или пустую папку", "Файлы")
    table.add_row("cat [имя]", "Прочитать содержимое файла", "Файлы")
    table.add_row("edit [имя]", "Текстовый редактор (запись в файл)", "Файлы")
    
    # Сеть и утилиты
    table.add_row("ping [url]", "Проверить соединение с сайтом", "Сеть")
    table.add_row("myip", "Узнать свой внешний IP-адрес", "Сеть")
    table.add_row("calc [выраж.]", "Инженерный калькулятор (например: calc 2+2*2)", "Утилиты")
    table.add_row("time", "Показать текущую дату и время", "Утилиты")
    table.add_row("echo [текст]", "Вывести текст на экран", "Утилиты")
    
    # Развлечения и система
    table.add_row("guess", "Мини-игра: Угадай число", "Игры")
    table.add_row("roll [max]", "Бросить кубик (случайное число от 1 до max)", "Игры")
    table.add_row("fetch", "Показать системную информацию", "Система")
    table.add_row("clear", "Очистить экран терминала", "Система")
    table.add_row("reboot", "Перезагрузить BlueOS", "Система")
    table.add_row("exit", "Завершить работу ОС", "Система")

    console.print(table)

# ==========================================
# ПРИЛОЖЕНИЯ И УТИЛИТЫ
# ==========================================

def app_text_editor(filename):
    """Простой текстовый редактор для консоли"""
    filepath = os.path.join(CURRENT_DIR, filename)
    console.print(f"[bold cyan]--- BlueEdit ---[/]")
    console.print(f"Файл: {filename}")
    console.print("Вводите текст. Чтобы сохранить и выйти, введите [bold red]:wq[/] на новой строке.")
    console.print("Чтобы выйти без сохранения, введите [bold red]:q[/]\n")
    
    lines = []
    while True:
        line = input("~ ")
        if line.strip() == ":wq":
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("\n".join(lines))
                console.print(f"[green]Файл {filename} успешно сохранен![/]")
            except Exception as e:
                console.print(f"[red]Ошибка при сохранении: {e}[/]")
            break
        elif line.strip() == ":q":
            console.print("[yellow]Выход без сохранения.[/]")
            break
        else:
            lines.append(line)

def app_guess_game():
    """Мини-игра: Угадай число"""
    console.print(Panel("Добро пожаловать в игру 'Угадай число'!\nЯ загадал число от 1 до 100. У тебя 7 попыток.", title="BlueGames", border_style="magenta"))
    secret = random.randint(1, 100)
    attempts = 7
    
    for i in range(attempts):
        try:
            guess = int(console.input(f"Попытка {i+1}/{attempts}. Твое число: "))
            if guess == secret:
                console.print(f"[bold green]Поздравляю! Ты угадал число {secret}![/]")
                return
            elif guess < secret:
                console.print("[yellow]Мое число БОЛЬШЕ.[/]")
            else:
                console.print("[yellow]Мое число МЕНЬШЕ.[/]")
        except ValueError:
            console.print("[red]Пожалуйста, введи целое число![/]")
            
    console.print(f"[bold red]Ты проиграл! Загаданное число было {secret}.[/]")

def get_public_ip():
    """Получение публичного IP-адреса"""
    console.print("[cyan]Подключение к серверу для получения IP...[/]")
    try:
        ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        console.print(f"Ваш внешний IP-адрес: [bold green]{ip}[/]")
    except Exception as e:
        console.print(f"[red]Не удалось получить IP. Проверьте интернет-соединение.[/]")

# ==========================================
# ГЛАВНЫЙ ЦИКЛ ОПЕРАЦИОННОЙ СИСТЕМЫ
# ==========================================

def main_loop():
    global CURRENT_DIR
    
    boot_sequence()
    show_neofetch()
    console.print("\nВведите [bold cyan]help[/] для списка команд.\n")

    while True:
        try:
            # Формирование строки приглашения (Prompt)
            # Показываем только путь относительно папки data, чтобы было красиво
            display_path = CURRENT_DIR
            if CURRENT_DIR.startswith(BASE_DIR):
                display_path = CURRENT_DIR.replace(BASE_DIR, "~")
                
            prompt_text = f"[bold cyan]{USER}@{OS_NAME}[/] [bold blue]{display_path}[/] > "
            command_line = console.input(prompt_text).strip()
            
            if not command_line:
                continue
                
            # Парсинг команды и аргументов
            parts = command_line.split()
            cmd = parts[0].lower()
            args = parts[1:]

            # --- ОБРАБОТКА КОМАНД ---

            if cmd == "help":
                display_help()

            elif cmd == "clear":
                clear_screen()

            elif cmd == "fetch":
                show_neofetch()

            elif cmd == "time":
                now = datetime.now()
                console.print(Panel(now.strftime("%H:%M:%S\n%d %B %Y"), title="Текущее время", expand=False, border_style="cyan"))

            elif cmd == "echo":
                console.print(" ".join(args))

            elif cmd == "calc":
                if not args:
                    console.print("[red]Укажите выражение, например: calc 2+2[/]")
                else:
                    expr = " ".join(args)
                    try:
                        # Используем eval безопасно, ограничивая встроенные функции
                        result = eval(expr, {"__builtins__": None}, {"math": math})
                        console.print(f"[bold green]Результат:[/] {result}")
                    except Exception as e:
                        console.print(f"[red]Ошибка вычисления: проверьте правильность выражения.[/]")

            elif cmd == "ping":
                if not args:
                    console.print("[red]Укажите адрес, например: ping google.com[/]")
                else:
                    target = args[0]
                    console.print(f"[cyan]Пингуем {target}...[/]")
                    # Вызов системного пинга в зависимости от ОС
                    param = '-n' if platform.system().lower()=='windows' else '-c'
                    os.system(f"ping {param} 4 {target}")

            elif cmd == "myip":
                get_public_ip()

            elif cmd == "guess":
                app_guess_game()

            elif cmd == "roll":
                max_val = 6
                if args and args[0].isdigit():
                    max_val = int(args[0])
                res = random.randint(1, max_val)
                console.print(f"Вы бросили кубик (d{max_val}). Выпало: [bold magenta]{res}[/]")

            # --- ФАЙЛОВАЯ СИСТЕМА ---
            
            elif cmd == "pwd":
                console.print(f"[cyan]{CURRENT_DIR}[/]")

            elif cmd == "ls":
                try:
                    items = os.listdir(CURRENT_DIR)
                    if not items:
                        console.print("[white]Папка пуста.[/]")
                    else:
                        table = Table(show_header=True, header_style="bold blue", box=None)
                        table.add_column("Тип")
                        table.add_column("Имя")
                        table.add_column("Размер")
                        
                        for item in sorted(items):
                            item_path = os.path.join(CURRENT_DIR, item)
                            if os.path.isdir(item_path):
                                table.add_row("[bold cyan]DIR[/]", f"[cyan]{item}[/]", "-")
                            else:
                                size = os.path.getsize(item_path)
                                table.add_row("[white]FILE[/]", item, f"{size} B")
                        console.print(table)
                except Exception as e:
                    console.print(f"[red]Ошибка чтения директории: {e}[/]")

            elif cmd == "cd":
                if not args:
                    CURRENT_DIR = DATA_DIR
                else:
                    target_dir = args[0]
                    new_path = os.path.abspath(os.path.join(CURRENT_DIR, target_dir))
                    if os.path.isdir(new_path):
                        CURRENT_DIR = new_path
                    else:
                        console.print(f"[red]Система не может найти указанный путь: {target_dir}[/]")

            elif cmd == "mkdir":
                if not args:
                    console.print("[red]Укажите имя папки: mkdir [имя][/]")
                else:
                    new_dir = os.path.join(CURRENT_DIR, args[0])
                    try:
                        os.makedirs(new_dir, exist_ok=True)
                        console.print(f"[green]Папка '{args[0]}' создана.[/]")
                    except Exception as e:
                        console.print(f"[red]Ошибка создания папки: {e}[/]")

            elif cmd == "touch":
                if not args:
                    console.print("[red]Укажите имя файла: touch [имя][/]")
                else:
                    file_path = os.path.join(CURRENT_DIR, args[0])
                    try:
                        open(file_path, 'a').close()
                        console.print(f"[green]Файл '{args[0]}' создан.[/]")
                    except Exception as e:
                        console.print(f"[red]Ошибка создания файла: {e}[/]")

            elif cmd == "rm":
                if not args:
                    console.print("[red]Укажите имя файла или папки для удаления: rm [имя][/]")
                else:
                    target_path = os.path.join(CURRENT_DIR, args[0])
                    if not os.path.exists(target_path):
                        console.print(f"[red]Файл или папка '{args[0]}' не существует.[/]")
                    else:
                        try:
                            if os.path.isdir(target_path):
                                os.rmdir(target_path)
                                console.print(f"[green]Папка '{args[0]}' удалена.[/]")
                            else:
                                os.remove(target_path)
                                console.print(f"[green]Файл '{args[0]}' удален.[/]")
                        except OSError as e:
                            console.print(f"[red]Ошибка удаления (возможно, папка не пуста): {e}[/]")

            elif cmd == "cat":
                if not args:
                    console.print("[red]Укажите имя файла: cat [имя][/]")
                else:
                    file_path = os.path.join(CURRENT_DIR, args[0])
                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            console.print(Panel(content, title=f"Файл: {args[0]}", border_style="white", expand=False))
                        except UnicodeDecodeError:
                            console.print("[red]Ошибка: Файл не является текстовым или имеет другую кодировку.[/]")
                        except Exception as e:
                            console.print(f"[red]Ошибка чтения файла: {e}[/]")
                    else:
                        console.print(f"[red]Файл '{args[0]}' не найден или это папка.[/]")

            elif cmd == "edit":
                if not args:
                    console.print("[red]Укажите имя файла: edit [имя][/]")
                else:
                    app_text_editor(args[0])

            # --- СИСТЕМНЫЕ УПРАВЛЯЮЩИЕ КОМАНДЫ ---

            elif cmd == "reboot":
                console.print("[bold red]Перезагрузка системы...[/]")
                time.sleep(1)
                boot_sequence()
                show_neofetch()

            elif cmd == "exit":
                console.print("[bold red]Завершение работы BlueOS...[/]")
                time.sleep(1)
                break

            else:
                console.print(f"[red]Команда '{cmd}' не найдена. Введите 'help' для просмотра списка команд.[/]")

        except KeyboardInterrupt:
            # Защита от случайного нажатия Ctrl+C
            print("\n")
            continue
        except Exception as e:
            console.print(f"\n[bold red]Критическая ошибка ядра:[/] {e}")

if __name__ == "__main__":
    # Запуск главного цикла при старте скрипта
    main_loop()
