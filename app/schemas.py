from pydantic import BaseModel


class QuestionCreate(BaseModel):
    subject_id: int
    question_text: str
    correct_answer: str
    difficulty: str