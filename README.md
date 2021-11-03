# Telegram бот - информирует о проверке работ на сайте [dvmn.org](https://dvmn.org/)

Бот отслеживает проверку работ. И если работа проверена информирует в Телеграме.

## Как установить

- Скачайте код.
```
git clone https://github.com/LobanAB/dvmn_tg_bot.git
```
- Для работы скачайте Python - https://www.python.org/.
- Установите зависимости 
```
pip install -r requirements.txt
```
- Создайте файл .env со следующим содержимым.
```
DVMN_API_TOKEN={API токен сайта [dvmn.org](https://dvmn.org/). Можно получить по ссылке [dvmn.org](https://dvmn.org/api/docs/)}
TG_API_TOKEN={API токен вашего Телеграм бота. Бота создает [Отец Ботов](https://telegram.me/BotFather)}
TG_CHAT_ID={Чтобы получить свой chat_id, напишите в Telegram специальному боту: @userinfobot}
```
- Запустите программу
```
python main.py
```

Бот ждет проверки работы и если работа будет проверена сообщит в Телеграм.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).