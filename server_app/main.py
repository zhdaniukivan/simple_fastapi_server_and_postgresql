from sqlalchemy.orm import  declarative_base
from fastapi import FastAPI, HTTPException, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server_app.models import Question
from datetime import datetime
import requests
Base = declarative_base()

app = FastAPI()

# Настройки для подключения к PostgreSQL
DATABASE_URL = "postgresql://same_user:same_password@localhost:5435/same_base_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get('/get_info/')
def get_info():
    return {'msg': "that program get many questions"}


@app.post("/get_questions/")
def get_questions(questions_num: int = Body(..., embed=True)):
    count_of_response = 0
    questions_dict = {}
    repeat_questions = []
    while questions_num >= len(questions_dict):
        db = SessionLocal()
        create_date = datetime.now()
        # первый раз запрашиваем количество вопросов в соответсвии с запрсом пользовотеля, второй раз только количество
        # вопросов которые уже были в базе данных
        response = requests.get(f"https://jservice.io/api/random?count={questions_num - len(questions_dict)}")
        count_of_response += 1
        if response.status_code == 200:
            data = response.json()
            for item in data:
                if not item['id'] in questions_dict:
                    # записываем все ответы в словарь
                    questions_dict[item['id']] = {
                        "id_questions": item["id"],
                        "question_text": item["question"],
                        "answer_text": item["answer"],
                        "create_date": create_date
                    }
                # Пушка, бомба, за один запрос к бд полчучаем список id уже существующих в базе данных
            existing_question_ids = db.query(Question.id).filter(Question.id.in_(questions_dict.keys())).all()
            # если в бд есть элементы с такимиже id, то мы запускаем чистку словаря для их удаления.
            if existing_question_ids:
                for key in existing_question_ids:
                    if key in questions_dict:
                        repeat_questions += key
                        del questions_dict[key]
                        # если количество оригинальных записей соттветвует требуемому запускаем процес сохранения их в
                        # базу данны
            if len(questions_dict) >= questions_num:
                # Создаем список объектов модели Question из словаря уникальных вопросов в количестве
                # равном questions_num
                count = 0
                questions_to_add = {}
                for key, q_data in questions_dict.items():
                    if count <= questions_num:
                        questions_to_add[key] = Question(
                            id_questions=q_data['id_questions'],
                            question_text=q_data["question_text"],
                            answer_text=q_data["answer_text"],
                            create_date=q_data['create_date']
                        )
                    count += 1
                db.add_all(questions_to_add.values())  # Добавляем все вопросы в базу данных
                db.commit()
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch questions from the API")

            db.close()
            print(f'Вы запросили оригинальных вопросов в количестве: {questions_num}, для их получения было сделано '
                  f'{count_of_response - 1} запросов. В базе данных сохранено количество оригинальных вопросов: '
                  f'{len(questions_to_add)}. Количество обработанных записей, которые уже хранились в базе данных, '
                  f'составило: {len(repeat_questions)}.')
            return questions_dict
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch questions from the API")

    db.close()
    return questions_to_add


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
