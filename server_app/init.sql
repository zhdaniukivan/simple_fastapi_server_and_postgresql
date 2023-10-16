-- Создание таблицы
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    id_questions INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    create_date TIMESTAMP NOT NULL
);