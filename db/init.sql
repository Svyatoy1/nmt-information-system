CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL
);

INSERT INTO subjects (name)
VALUES
    ('Математика'),
    ('Українська мова'),
    ('Історія України');

INSERT INTO questions (
    subject_id,
    question_text,
    correct_answer,
    difficulty
)
VALUES
    (
        1,
        'Скільки буде 2 + 2 * 2?',
        '6',
        'easy'
    ),
    (
        1,
        'Знайдіть корінь рівняння x + 5 = 12.',
        '7',
        'easy'
    ),
    (
        2,
        'У якому слові правильно поставлено наголос: каталОг чи катАлог?',
        'каталОг',
        'medium'
    ),
    (
        2,
        'Яка частина мови відповідає на питання "який?"?',
        'Прикметник',
        'easy'
    ),
    (
        3,
        'У якому році Україна проголосила незалежність?',
        '1991',
        'easy'
    ),
    (
        3,
        'Хто був автором Конституції Пилипа Орлика?',
        'Пилип Орлик',
        'medium'
    );