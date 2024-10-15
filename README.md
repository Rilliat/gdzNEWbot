# gdzNEWbot

ГДЗ-бот, использующий популярные ГДЗ-сервисы, а также `aiogram`, `requests` и `journal-api`.

-----

## Установка
- Клонирование репозитория
```
git clone https://github.com/Rilliat/gdzNEWbot.git && cd gdzNEWbot
```
- Для Debian-базированных Linux:
```
sudo apt install python3 python3-pip
```

- Установка необходимых зависимостей:
```
pip3 install -r requirements.txt
```

-----

- Настройка конфигурационных файлов
```
cp .env.example .env
```

Измените значения на свои (при необходимости также измените имя базы данных)

**Необходимые для изменения поля:**
- `API_TOKEN` - Telegram-токен, полученный от <a href="https://t.me/BotFather">@BotFather</a>. 
- `ADMIN_IDS` - Строка с Telegram ID пользователей, которые должны иметь доступ к /admin-панели. Разделены двоеточием (`:`)

**Необязательные для изменения поля:**
- `DATABASE_NAME` - Файл базы данных. По умолчанию `data.db`, но при особом желании может быть изменено

-----

- Запуск бота
```
python3 main.py
```

-----

## Systemd и автозапуск
- Для того чтобы бот не останавливался и при ошибках перезапускался необходимо установить сервис systemd.
- **В строках `ExecStart` и `User` меняем `user` на имя вашего пользователя**

```
sudo cp gdzNEWbot.service /lib/systemd/system/gdzNEWbot.service
```

После настройки имени пользователя:

```
sudo systemctl daemon-reload
sudo systemctl enable gdzNEWbot.service
sudo systemctl start gdzNEWbot.service
```

- Проверяем работоспособность через несколько секунд после запуска:
```
systemctl status gdzNEWbot.service
```
