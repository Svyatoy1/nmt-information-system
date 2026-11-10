from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.schemas import QuestionCreate

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.database import engine


app = FastAPI(
    title="NMT Information System",
    version="0.1.0",
)


question_requests = Counter(
    "nmt_question_requests_total",
    "Total number of requests for NMT questions",
    ["operation"],
)

database_errors = Counter(
    "nmt_database_errors_total",
    "Total number of database errors",
)

questions_created = Counter(
    "nmt_questions_created_total",
    "Total number of created NMT questions",
)


@app.get("/")
def root():
    return {
        "service": "NMT Information System",
        "status": "running",
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        database_errors.inc()

        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )


@app.get("/questions")
def get_questions():
    question_requests.labels(operation="list").inc()

    query = text("""
        SELECT
            q.id,
            s.name AS subject,
            q.question_text,
            q.correct_answer,
            q.difficulty
        FROM questions q
        JOIN subjects s
            ON q.subject_id = s.id
        ORDER BY q.id
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            questions = result.mappings().all()

        return list(questions)

    except Exception:
        database_errors.inc()

        raise HTTPException(
            status_code=500,
            detail="Database error",
        )


@app.get("/questions/random")
def get_random_question():
    question_requests.labels(operation="random").inc()

    query = text("""
        SELECT
            q.id,
            s.name AS subject,
            q.question_text,
            q.correct_answer,
            q.difficulty
        FROM questions q
        JOIN subjects s
            ON q.subject_id = s.id
        ORDER BY RANDOM()
        LIMIT 1
    """)

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            question = result.mappings().first()

        if question is None:
            raise HTTPException(
                status_code=404,
                detail="No questions found",
            )

        return question

    except HTTPException:
        raise

    except Exception:
        database_errors.inc()

        raise HTTPException(
            status_code=500,
            detail="Database error",
        )


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
    
@app.post("/questions", status_code=201)
def create_question(question: QuestionCreate):
    query = text("""
        INSERT INTO questions (
            subject_id,
            question_text,
            correct_answer,
            difficulty
        )
        VALUES (
            :subject_id,
            :question_text,
            :correct_answer,
            :difficulty
        )
        RETURNING
            id,
            subject_id,
            question_text,
            correct_answer,
            difficulty
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "subject_id": question.subject_id,
                    "question_text": question.question_text,
                    "correct_answer": question.correct_answer,
                    "difficulty": question.difficulty,
                },
            )

            created_question = result.mappings().first()

        questions_created.inc()

        return created_question

    except Exception:
        database_errors.inc()

        raise HTTPException(
            status_code=500,
            detail="Database error",
        )