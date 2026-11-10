import sys

import requests


BASE_URL = "http://localhost:8000"


def print_separator():
    print("-" * 60)


def check_health():
    print("1. Checking system health...")

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=5,
    )

    response.raise_for_status()

    data = response.json()

    print(f"[OK] API status: {data['status']}")
    print(f"[OK] Database: {data['database']}")


def get_questions():
    response = requests.get(
        f"{BASE_URL}/questions",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


def show_random_questions(count=3):
    print(f"3. Getting {count} random questions...")

    for number in range(1, count + 1):
        response = requests.get(
            f"{BASE_URL}/questions/random",
            timeout=5,
        )

        response.raise_for_status()

        question = response.json()

        print()
        print(f"Random question #{number}")
        print(f"Subject: {question['subject']}")
        print(f"Question: {question['question_text']}")
        print(f"Answer: {question['correct_answer']}")
        print(f"Difficulty: {question['difficulty']}")


def create_question():
    print("4. Creating a new question...")

    new_question = {
        "subject_id": 1,
        "question_text": "Чому дорівнює 10 у квадраті?",
        "correct_answer": "100",
        "difficulty": "easy",
    }

    response = requests.post(
        f"{BASE_URL}/questions",
        json=new_question,
        timeout=5,
    )

    response.raise_for_status()

    question = response.json()

    print("[OK] Question created")
    print(f"ID: {question['id']}")
    print(f"Question: {question['question_text']}")


def main():
    print()
    print("===== NMT INFORMATION SYSTEM DEMO =====")
    print()

    try:
        check_health()

        print_separator()

        print("2. Reading questions from PostgreSQL...")

        questions_before = get_questions()

        print(
            f"[OK] Questions currently stored: "
            f"{len(questions_before)}"
        )

        print_separator()

        show_random_questions()

        print()
        print_separator()

        create_question()

        print_separator()

        questions_after = get_questions()

        print("5. Checking database after INSERT...")
        print(
            f"Questions before: {len(questions_before)}"
        )
        print(
            f"Questions after:  {len(questions_after)}"
        )

        if len(questions_after) > len(questions_before):
            print("[OK] PostgreSQL data changed successfully")
        else:
            print("[WARNING] Question count did not change")

        print()
        print("===== DEMO COMPLETED SUCCESSFULLY =====")
        print()

    except requests.exceptions.ConnectionError:
        print(
            "[ERROR] Cannot connect to API. "
            "Make sure Docker Compose is running."
        )
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Request failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()