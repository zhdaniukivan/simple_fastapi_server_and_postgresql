Сначала клонируйте репозиторий из GitHub:

git clone https://github.com/zhdaniukivan/simple_fastapi_server_and_postgresql.git

Затем перейдите в каталог с файлом docker-compose.yml:

Установите необходимые зависимости с помощью pip:

pip install -r requirements.txt

Запустите сервер PostgreSQL в Docker-контейнере:

docker-compose up -d

Наконец, запустите сервер FastAPI:

uvicorn server_app.main:app --reload

Откройте программу Postman или Insomnia и отправьте POST-запрос с телом JSON:

{
    "questions_num": 50
}
В результате вы получите 50 вопросов с ресурса https://jservice.io/api/random?count=1. Программа проверит 
их на уникальность и на совпадение с сохраненными вопросами в базе данных. В случае необходимости, она запросит
ещё необходимое количество оригинальных вопросов и сохранит их в базе данных. В ответ пользователю будет возвращен 
JSON с 50 уникальными вопросами и ответами.
