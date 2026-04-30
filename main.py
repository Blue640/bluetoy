import os
import requests
import zipfile
import io
from tqdm import tqdm

# Настройки репозитория
OWNER = "ваш_логин_на_github"
REPO = "название_вашего_репозитория"
VERSION_FILE = "version.txt"
FOLDERS = ["core", "assets", "data"]

def create_folders():
    """Создаёт необходимую структуру директорий."""
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
    
    # Создаём файл версии, если его нет
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write("0.0.0")

def get_local_version():
    """Считывает текущую локальную версию."""
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def set_local_version(version):
    """Обновляет версию в файле."""
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        f.write(version)

def check_for_updates():
    """Проверяет обновления через API GitHub."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data["tag_name"], data["zipball_url"]
    except Exception as e:
        print(f"Не удалось проверить обновления: {e}")
    return None, None

def download_and_extract_update(zip_url):
    """Скачивает и распаковывает архив с обновлением."""
    try:
        print("Найдено обновление. Загрузка...")
        response = requests.get(zip_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        file_bytes = b''
        chunk_size = 1024
        
        # Скачивание с прогресс-баром
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Скачивание") as progress_bar:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    file_bytes += chunk
                    progress_bar.update(len(chunk))
        
        print("\nРаспаковка и сортировка файлов...")
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as zip_ref:
            for member in zip_ref.namelist():
                # Пропускаем папки
                if member.endswith('/'):
                    continue
                
                file_name = os.path.basename(member)
                
                # Логика распределения по папкам
                if "core/" in member:
                    target_path = os.path.join("core", file_name)
                elif "assets/" in member:
                    target_path = os.path.join("assets", file_name)
                elif "data/" in member:
                    target_path = os.path.join("data", file_name)
                else:
                    target_path = file_name # Файлы в корне проекта
                
                with open(target_path, 'wb') as f:
                    f.write(zip_ref.read(member))
                    
        print("Обновление успешно установлено.")
        return True
    except Exception as e:
        print(f"Ошибка при установке обновлений: {e}")
        return False

def main():
    create_folders()
    local_version = get_local_version()
    print(f"Текущая версия программы: {local_version}")
    
    print("Проверка наличия обновлений...")
    latest_version, zip_url = check_for_updates()
    
    if latest_version and latest_version != local_version:
        if download_and_extract_update(zip_url):
            set_local_version(latest_version)
    else:
        print("Обновлений не найдено. Пропускаем.")

if __name__ == "__main__":
    main()

