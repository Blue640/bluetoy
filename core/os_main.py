import os, time, sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.columns import Columns

console = Console()

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def get_weather():
    # Погода специально для твоего региона
    return "[bold cyan]Петрозаводск:[/] +12°C, Переменная облачность (Эмуляция)"

def neofetch():
    sys_info = (
        "[bold cyan]OS:[/] BlueOS v1.2\n"
        "[bold cyan]Kernel:[/] Python 3.x Hybrid\n"
        "[bold cyan]Shell:[/] BlueShell\n"
        "[bold cyan]Theme:[/] Midnight Blue\n"
        "[bold cyan]Location:[/] Petrozavodsk, Karelia"
    )
    logo = "[bold blue]      ____  __           \n     / __ )/ /_  _____  \n    / __  / / / / / _ \\ \n   / /_/ / / /_/ /  __/ \n  /_____/_/\\__,_/\\___/  [/]"
    console.print(Panel(Columns([logo, sys_info]), title="System Status", border_style="cyan"))

def file_manager():
    files = os.listdir('data') if os.path.exists('data') else []
    table = Table(title="Файлы в /data", style="blue")
    table.add_column("Имя файла", style="cyan")
    table.add_column("Размер", justify="right")
    for f in files:
        size = os.path.getsize(f"data/{f}")
        table.add_row(f, f"{size} bytes")
    console.print(table)

def main():
    clear()
    for _ in track(range(10), description="[bold blue]Загрузка ядра..."):
        time.sleep(0.1)
    
    clear()
    neofetch()
    console.print(f" {get_weather()}\n", justify="center")

    while True:
        try:
            cmd = console.input("[bold cyan]BlueOS[/]>[bold white] ").strip().split()
            if not cmd: continue
            
            base = cmd[0].lower()
            args = cmd[1:]

            if base == "help":
                t = Table(show_header=False, border_style="blue")
                t.add_row("ls", "Список файлов в папке данных")
                t.add_row("touch [имя]", "Создать пустой файл")
                t.add_row("rm [имя]", "Удалить файл")
                t.add_row("calc [выражение]", "Математический калькулятор")
                t.add_row("weather", "Прогноз погоды")
                t.add_row("fetch", "Информация о системе")
                t.add_row("clear", "Очистить экран")
                t.add_row("exit", "Выход")
                console.print(t)

            elif base == "ls":
                file_manager()

            elif base == "touch":
                if args:
                    os.makedirs('data', exist_ok=True)
                    open(f"data/{args[0]}", 'a').close()
                    console.print(f"[green]Файл {args[0]} создан.[/]")
                else: console.print("[red]Укажите имя файла[/]")

            elif base == "rm":
                if args and os.path.exists(f"data/{args[0]}"):
                    os.remove(f"data/{args[0]}")
                    console.print(f"[red]Файл {args[0]} удален.[/]")

            elif base == "calc":
                try: res = eval(" ".join(args))
                except: res = "Ошибка в выражении"
                console.print(f"[bold yellow]Результат:[/] {res}")

            elif base == "weather":
                console.print(get_weather())

            elif base == "fetch":
                neofetch()

            elif base == "clear":
                clear()

            elif base == "exit":
                console.print("[bold red]Завершение сессии...[/]")
                break
            
            else:
                console.print(f"[red]Команда '{base}' не распознана. Введи 'help'.[/]")

        except Exception as e:
            console.print(f"[bold red]Ошибка:[/] {e}")

if __name__ == "__main__":
    main()
