# 🔐 SecureBot

Асинхронний Telegram-бот для шифрування та дешифрування тексту.  
Створений на **Python 3.12** з використанням **Aiogram 3** і **aiosqlite**.

---

## 🚀 Можливості

- 🔑 Шифрування та дешифрування повідомлень (`cryptography.fernet`)
- 💾 Збереження користувачів і ключів у базі даних (`aiosqlite`)
- ⚙️ Асинхронна логіка на основі FSM
- 🧭 Зручні інлайн-кнопки для взаємодії

---

## ⚙️ Встановлення

```bash
# 1. Клонувати репозиторій
git clone https://github.com/username/securebot.git
cd securebot

# 2. Створити віртуальне середовище
python3 -m venv .venv
source .venv/bin/activate   # або .venv\Scripts\activate для Windows

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Запустити бота
python main.py
