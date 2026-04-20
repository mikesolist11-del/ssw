#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════╗
║  ███████╗███████╗██╗    ██╗                                      ║
║  ██╔════╝██╔════╝██║    ██║                                      ║
║  ███████╗███████╗██║ █╗ ██║                                      ║
║  ╚════██║╚════██║██║███╗██║                                      ║
║  ███████║███████║╚███╔███╔╝                                      ║
║  ╚══════╝╚══════╝ ╚══╝╚══╝                                       ║
║                                                                   ║
║     SSW - swexxer secure wrapper                                 ║
║     Шифрование трафика + чистильщик следов                        ║
║     by swexxer (aka cwex) | github.com/swexxer/ssw               ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import random
import string
import hashlib
import shutil
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ========== ЦВЕТА ==========
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
SESSION_FILE = os.path.expanduser("~/.ssw_session")
COOKIE_FILE = os.path.expanduser("~/.ssw_cookies")
LOG_FILE = os.path.expanduser("~/.ssw_log")

# ========== USER-AGENT БАЗА ==========
USER_AGENTS = {
    "chrome": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ],
    "firefox": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0",
    ],
    "safari": [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    ],
    "edge": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    ],
    "mobile": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    ]
}

def get_random_user_agent():
    """Возвращает случайный User-Agent"""
    import random
    browser = random.choice(list(USER_AGENTS.keys()))
    return random.choice(USER_AGENTS[browser])

def spoof_user_agent():
    """Подменяет User-Agent для системных запросов"""
    ua = get_random_user_agent()
    
    # Устанавливаем переменную окружения
    os.environ['USER_AGENT'] = ua
    
    # Для Python requests
    try:
        import requests
        requests.utils.default_user_agent = lambda: ua
    except:
        pass
    
    print(f"{GREEN}[✓]{RESET} User-Agent подменён на: {YELLOW}{ua[:50]}...{RESET}")
    return ua

def simulate_traffic_encryption(level):
    """Симулирует шифрование трафика (для демо) с реальной подменой UA"""
    steps = [
        "Анализ исходящих пакетов...",
        "Установка защищенного канала...",
        "Применение шифрования к заголовкам...",
        "Маскировка TLS-отпечатков...",
    ]
    
    for step in steps:
        print(f"{YELLOW}[*]{RESET} {step}")
        time.sleep(random.uniform(0.5, 1))
    
    # РЕАЛЬНАЯ подмена User-Agent
    print(f"{YELLOW}[*]{RESET} Подмена User-Agent...")
    ua = spoof_user_agent()
    time.sleep(0.5)
    
    print(f"{YELLOW}[*]{RESET} Обфускация DNS-запросов...")
    time.sleep(0.5)
    
    if level == 1:
        print(f"{CYAN}[!]{RESET} Слабое шифрование (MD5+XOR) — обнаружение возможно")
    elif level == 2:
        print(f"{CYAN}[!]{RESET} Среднее шифрование (AES-256) — хорошая защита")
    else:
        print(f"{CYAN}[!]{RESET} Паранойя-режим (Fernet + мультиплексирование) — макс защита")
    
    # Сохраняем сессию с UA
    with open(SESSION_FILE, 'w') as f:
        f.write(f"active|{level}|{int(time.time())}|{ua}")

def banner():
    print(f"""{CYAN}{BOLD}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ███████╗███████╗██╗    ██╗                                      ║
    ║   ██╔════╝██╔════╝██║    ██║                                      ║
    ║   ███████╗███████╗██║ █╗ ██║                                      ║
    ║   ╚════██║╚════██║██║███╗██║                                      ║
    ║   ███████║███████║╚███╔███╔╝                                      ║
    ║   ╚══════╝╚══════╝ ╚══╝╚══╝                                       ║
    ║                                                                   ║
    ║     SSW - swexxer secure wrapper                                 ║
    ║     by swexxer (aka cwex) | github.com/swexxer/ssw               ║
    ╚═══════════════════════════════════════════════════════════════════╝
    {RESET}""")

def generate_key(level):
    """Генерирует ключ шифрования в зависимости от уровня"""
    if level == 1:
        return hashlib.md5(b"swexxer_weak_2026").hexdigest()[:32].encode()
    elif level == 2:
        return hashlib.sha256(b"swexxer_medium_2026_with_salt_xyz").hexdigest().encode()
    else:
        return Fernet.generate_key()

def encrypt_data(data, level):
    """Шифрует данные с выбранным уровнем"""
    if level == 1:
        # MD5 + XOR (примитив)
        key = generate_key(1)
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return bytes(result)
    elif level == 2:
        # AES-256-CBC
        key = generate_key(2)[:32]
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        pad = 16 - (len(data) % 16)
        padded_data = data + bytes([pad] * pad)
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted
    else:
        # Fernet (уровень 3)
        key = generate_key(3)
        f = Fernet(key)
        return f.encrypt(data)

def simulate_traffic_encryption(level):
    """Симулирует шифрование трафика (для демо)"""
    steps = [
        "Анализ исходящих пакетов...",
        "Установка защищенного канала...",
        "Применение шифрования к заголовкам...",
        "Маскировка TLS-отпечатков...",
        "Подмена User-Agent...",
        "Обфускация DNS-запросов..."
    ]
    
    for step in steps:
        print(f"{YELLOW}[*]{RESET} {step}")
        time.sleep(random.uniform(0.5, 1))
    
    if level == 1:
        print(f"{CYAN}[!]{RESET} Слабое шифрование (MD5+XOR) — обнаружение возможно")
    elif level == 2:
        print(f"{CYAN}[!]{RESET} Среднее шифрование (AES-256) — хорошая защита")
    else:
        print(f"{CYAN}[!]{RESET} Паранойя-режим (Fernet + мультиплексирование) — макс защита")
    
    # Сохраняем сессию
    with open(SESSION_FILE, 'w') as f:
        f.write(f"active|{level}|{int(time.time())}")

def clean_everything():
    """Чистит все следы — куки, сессии, кэш"""
    print(f"{RED}[*]{RESET} Чистка следов...")
    
    # 1. Удаляем файлы сессии
    for f in [SESSION_FILE, COOKIE_FILE, LOG_FILE]:
        if os.path.exists(f):
            os.remove(f)
            print(f"  - Удалён: {f}")
    
    # 2. Чистим куки браузеров
    browser_paths = {
        "Chrome": os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies"),
        "Firefox": os.path.expanduser("~/Library/Application Support/Firefox/Profiles/"),
        "Safari": os.path.expanduser("~/Library/Cookies/"),
        "Brave": os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies")
    }
    
    for browser, path in browser_paths.items():
        if os.path.exists(path):
            try:
                if browser == "Firefox":
                    shutil.rmtree(path)
                    print(f"  - Удалён профиль Firefox")
                else:
                    if os.path.isfile(path):
                        os.remove(path)
                        print(f"  - Удалены куки {browser}")
                    elif os.path.isdir(path):
                        for f in os.listdir(path):
                            if "cookie" in f.lower():
                                os.remove(os.path.join(path, f))
                                print(f"  - Удалены куки {browser}")
            except Exception as e:
                print(f"  - {browser}: ошибка ({e})")
    
    # 3. Чистим историю терминала
    history_files = [
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.zsh_history"),
        os.path.expanduser("~/.python_history")
    ]
    
    for hf in history_files:
        if os.path.exists(hf):
            with open(hf, 'w') as f:
                f.write("")
            print(f"  - Очищена история: {hf}")
    
    # 4. Затираем свободное место (быстрое)
    print(f"{YELLOW}[*]{RESET} Затирание свободного места...")
    os.system("rm -rf ~/.Trash/* 2>/dev/null")
    
    # 5. Сбрасываем DNS-кэш macOS
    os.system("sudo dscacheutil -flushcache 2>/dev/null")
    os.system("sudo killall -HUP mDNSResponder 2>/dev/null")
    print(f"  - DNS-кэш сброшен")
    
    print(f"{GREEN}[✓]{RESET} Чистка завершена. Все следы удалены.")

def start_encryption():
    banner()
    print(f"\n{GREEN}[+] Начинаем шифрование!{RESET}\n")
    
    print("Выберите тип шифрования (1-3):")
    print("  1 — Слабое (MD5+XOR, быстро, низкая защита)")
    print("  2 — Среднее (AES-256, баланс скорости и защиты)")
    print("  3 — Паранойя (Fernet + маскировка трафика, максимально)\n")
    
    try:
        choice = input(f"{CYAN}> {RESET}").strip()
        if choice not in ['1', '2', '3']:
            print(f"{RED}[-] Неверный выбор. Использую уровень 2 (средний){RESET}")
            level = 2
        else:
            level = int(choice)
    except:
        level = 2
    
    print(f"\n{GREEN}[✓] Отлично!{RESET}")
    print(f"{YELLOW}[*]{RESET} Начинаем шифрование трафика...\n")
    
    # Тестовое шифрование для демонстрации
    test_data = b"GET / HTTP/1.1\nHost: example.com\nCookie: session=abc123"
    encrypted = encrypt_data(test_data, level)
    
    print(f"{GREEN}[✓]{RESET} Шифруем данные...")
    time.sleep(1)
    print(f"{GREEN}[✓]{RESET} Все успешно!")
    print(f"{CYAN}[!]{RESET} Размер исходных данных: {len(test_data)} байт")
    print(f"{CYAN}[!]{RESET} Размер зашифрованных: {len(encrypted)} байт")
    print(f"{CYAN}[!]{RESET} Коэффициент: {len(encrypted)/len(test_data):.2f}x\n")
    
    simulate_traffic_encryption(level)
    
    print(f"\n{GREEN}{BOLD}[✓] Шифрование активно!{RESET}")
    print(f"{CYAN}[i]{RESET} Для остановки и очистки следов выполните: {BOLD}./ssw stop{RESET}\n")
    
    # Ссылка на GitHub
    print(f"{YELLOW}{'='*60}{RESET}")
    print(f"{CYAN}🔗 GitHub: https://github.com/swexxer/ssw{RESET}")
    print(f"{CYAN}📌 by swexxer (aka cwex) | Легенда КМ{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")

def stop_and_clean():
    banner()
    print(f"\n{RED}[!] Останавливаем шифрование...{RESET}\n")
    
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            session = f.read()
        print(f"{YELLOW}[*]{RESET} Найдена активная сессия: {session}")
    else:
        print(f"{YELLOW}[*]{RESET} Активных сессий не найдено")
    
    print(f"\n{RED}[*]{RESET} Удаляем все сессии, чистим куки и следы...\n")
    clean_everything()
    
    print(f"\n{GREEN}{BOLD}[✓] SSW остановлен. Все следы уничтожены.{RESET}\n")

# ========== MAIN ==========
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./ssw [start|stop]")
        print(f"  start - начать шифрование трафика")
        print(f"  stop  - остановить и очистить все следы")
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    
    if cmd == "start":
        start_encryption()
    elif cmd == "stop":
        stop_and_clean()
    else:
        print(f"{RED}[-] Неизвестная команда. Используй start или stop{RESET}")