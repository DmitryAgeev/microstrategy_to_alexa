# Connecting Microstrategy to Alexa using Python
My project for the Veon company, created using Python(Flask, mstrio), which allows the user to receive data from MSTR reports through Alexa.

[Video demonstration](https://youtu.be/WXKr-kEGB9Q "YouTube video")


Instruction in Russian

Подготовка к работе:
1. Скачать все файлы проекта
2. Настроить окружение
3. Создать репорт (Revenue, Profit, Employee Headcount, Previous month transformations)
4. Создать скилл (custom)
5. Загурузить AlexaSkill.json в Interaction Model -> JSON Editor
6. Поменять skill_id в main.py
7. Поменять base_url, mstr_username, mstr_password, project_name, report_id в MicroConnect.py

Запуск:

0. Запустить сервер
1. Запустить main.py
2. Включить ngrok и создать тунель к локальному хосту (ngrok.exe http 5000)
3. Поменять endpoin на ngrok URL в настройках скилла
