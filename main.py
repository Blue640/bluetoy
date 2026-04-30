import os
import requests
import zipfile
import io
from tqdm import tqdm

OWNER = "Blue640"
REPO = "BlueToy"
VERSION_FILE = "version.txt"

def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def check_updates():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data["tag_name"], data["zipball_url"]
    except: 
        pass
    return None, None

def update_system(zip_url, new_ver):
    print(f"[Система] Найдено обновление {new_ver}. Загрузка...")
    r = requests.get(zip_url, stream=True)
    total = int(r.headers.get('content-length', 0))
    
    buf = io.BytesIO()
    with tqdm(total=total, unit='B', unit_scale=True, desc="Прогресс") as pbar:
        for chunk in r.iter_content(1024):
            buf.write(chunk)
            pbar.update(len(chunk))
    
    with zipfile.ZipFile(buf) as z:
        root = z.namelist()[0].split('/')[0]
        
        for member in z.namelist():
            # Пропускаем папки
            if member.endswith('/'):
                continue
            
            # Убираем имя корневой папки из пути
            new_path = member.replace(root + '/', '', 1)
            if not new_path:
                continue
            
            # Создаем директорию, если она есть в пути
            dir_name = os.path.dirname(new_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            
            # Записываем файл
            with open(new_path, 'wb') as f:
                f.write(z.read(member))
                
    with open(VERSION_FILE, 'w', encoding='utf-8') as f:
        f.write(new_ver)
    print("[Система] Обновление успешно установлено.")

def main():
    cur_ver = get_local_version()
    print(f"BlueOS Launcher | Версия: {cur_ver}")
    new_ver, url = check_updates()
    
    if new_ver and new_ver != cur_ver:
        update_system(url, new_ver)
    else:
        print("Обновлений нет. Запуск...")
    
    # Запуск ОС в новом окне
        os.system('start /max cmd /c "title BlueOS Terminal & python core/os_main.py"')

if __name__ == "__main__":
    main()
