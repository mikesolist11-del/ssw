#!/bin/bash

echo "[+] Установка SSW..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 не найден. Установи Python3"
    exit 1
fi

# Установка зависимостей
pip3 install cryptography

# Делаем скрипт исполняемым
chmod +x ssw.py

# Опционально: добавляем в PATH
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo ln -sf $(pwd)/ssw.py /usr/local/bin/ssw
    echo "[✓] Установлен глобально: ssw"
fi

echo "[✓] Готово! Используй: ./ssw.py start"