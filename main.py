import os, requests, zipfile, io, shutil
from tqdm import tqdm

OWNER = "Blue640"
REPO = "BlueToy"
VERSION_FILE = "version.txt"

def get_local_version():
    if not os.path.exists(VERSION_FILE): return "0.0.0"
    with open(VERSION_FILE, 'r') as f: return f.read().strip()

def check_updates():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return data["tag_name"], data["zipball_url"]
    except: pass
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
        # GitHub упаковывает всё в одну корневую папку, её надо пропустить
        root = z.namelist()[0].split('/')[0]
        for member in z.namelist():
            if member == root + '/': continue
            # Убираем имя корневой папки из пути
            new_path = member.replace(root + '/', '', 1)
            if not new_path: continue
            
            if member.endswith('/'):
                os.makedirs(new_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                with open(new_path, 'wb') as f:
                    f.write(z.read(member))
    
    with open(VERSION_FILE, 'w') as f: f.write(new_ver)
    print("[Система] Обновление завершено.")

def main():
    cur_ver = get_local_version()
    print(f"BlueOS Launcher | Версия: {cur_ver}")
    new_ver, url = check_updates()
    
    if new_ver and new_ver != cur_ver:
        update_system(url, new_ver)
    else:
        print("Обновлений нет. Запуск...")
    
    # Запуск самой ОС в новом окне
    os.system('start cmd /c "title BlueOS Terminal & mode con: cols=100 lines=30 & python core/os_main.py"')

if __name__ == "__main__":
    main()
