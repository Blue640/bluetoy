import os
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Инициализируем консоль Rich
console = Console()

def clear_screen():
    """Очистка экрана в зависимости от платформы"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Красивая таблица с командами"""
    table = Table(title="Доступные команды", style="cyan")
    table.add_column("Команда", style="bold blue", no_wrap=True)
    table.add_column("Описание", style="white")
    
    table.add_row("help", "Показать этот список команд")
    table.add_row("clear", "Очистить экран")
    table.add_row("time", "Показать текущее время и дату")
    table.add_row("sysinfo", "Информация о системе")
    table.add_row("echo [текст]", "Вывести текст на экран")
    table.add_row("exit", "Завершить работу BlueOS")
    
    console.print(table)

def boot_sequence():
    """Имитация красивой загрузки системы"""
    clear_screen()
    console.print("[bold blue]Инициализация ядра BlueOS...[/bold blue]")
    time.sleep(0.7)
    console.print("[bold cyan]Загрузка модулей файловой системы...[/bold cyan]")
    time.sleep(0.5)
    console.print("[bold cyan]Подключение графического интерфейса терминала...[/bold cyan]")
    time.sleep(0.5)
    clear_screen()
    
    # Главное приветствие в рамке
    welcome_text = Text("Добро пожаловать в BlueOS", style="bold cyan on black", justify="center")
    console.print(Panel(welcome_text, border_style="blue", padding=(1, 2)))
    print()

def main_loop():
    """Главный цикл операционной системы"""
    boot_sequence()
    
    while True:
        try:
            # Кастомная строка ввода пользователя
            command_line = console.input("[bold cyan]BlueOS[/bold cyan]@[bold blue]root[/bold blue]> ")
            args = command_line.strip().split()
            
            if not args:
                continue
                
            cmd = args[0].lower()
            
            # Обработка команд
            if cmd == "help":
                show_help()
            elif cmd == "clear":
                clear_screen()
            elif cmd == "time":
                now = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
                console.print(f"[{'cyan'}]Текущее время:[/] {now}")
            elif cmd == "sysinfo":
                info_panel = Panel(
                    "ОС: [bold cyan]BlueOS v1.0[/bold cyan]\n"
                    "База: Python Core / Windows Host\n"
                    "Пользователь: root\n"
                    "Интерфейс: Rich Terminal",
                    title="Системная информация",
                    border_style="blue"
                )
                console.print(info_panel)
            elif cmd == "echo":
                text = " ".join(args[1:])
                console.print(f"[white]{text}[/white]")
            elif cmd == "exit":
                console.print("[bold red]Завершение работы системы...[/bold red]")
                time.sleep(1)
                break
            else:
                console.print(f"[bold red]Ошибка:[/bold red] команда '{cmd}' не найдена. Введите 'help' для справки.")
                
        except KeyboardInterrupt:
            # Защита от случайного нажатия Ctrl+C
            print("\n")
            continue
        except Exception as e:
            console.print(f"[bold red]Критическая ошибка ядра:[/bold red] {e}")

if __name__ == "__main__":
    main_loop()

