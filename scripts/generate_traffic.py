import random
import sys
import time

import requests


BASE_URL = "http://localhost:8000"

RANDOM_REQUESTS = 20
LIST_REQUESTS = 5
CREATE_REQUESTS = 3


def request_random_question():
    response = requests.get(
        f"{BASE_URL}/questions/random",
        timeout=5,
    )

    response.raise_for_status()


def request_questions():
    response = requests.get(
        f"{BASE_URL}/questions",
        timeout=5,
    )

    response.raise_for_status()


def create_question(index):
    number = random.randint(1000, 9999)

    payload = {
        "subject_id": 1,
        "question_text": (
            f"Автоматично створене тестове питання "
            f"#{index}-{number}"
        ),
        "correct_answer": "Тестова відповідь",
        "difficulty": "easy",
    }

    response = requests.post(
        f"{BASE_URL}/questions",
        json=payload,
        timeout=5,
    )

    response.raise_for_status()


def main():
    print()
    print("===== NMT TRAFFIC GENERATOR =====")
    print()

    total_requests = (
        RANDOM_REQUESTS
        + LIST_REQUESTS
        + CREATE_REQUESTS
    )

    completed = 0

    try:
        print(
            f"GET /questions/random: {RANDOM_REQUESTS}"
        )

        for _ in range(RANDOM_REQUESTS):
            request_random_question()

            completed += 1

            print(
                f"[{completed}/{total_requests}] "
                f"GET /questions/random"
            )

            time.sleep(0.1)

        print()

        print(
            f"GET /questions: {LIST_REQUESTS}"
        )

        for _ in range(LIST_REQUESTS):
            request_questions()

            completed += 1

            print(
                f"[{completed}/{total_requests}] "
                f"GET /questions"
            )

            time.sleep(0.1)

        print()

        print(
            f"POST /questions: {CREATE_REQUESTS}"
        )

        for index in range(
            1,
            CREATE_REQUESTS + 1,
        ):
            create_question(index)

            completed += 1

            print(
                f"[{completed}/{total_requests}] "
                f"POST /questions"
            )

            time.sleep(0.1)

        print()
        print(
            f"[OK] Generated {completed} HTTP requests"
        )

        print()
        print(
            "Open Prometheus:"
        )
        print(
            "http://localhost:9090"
        )

        print()
        print(
            "Query:"
        )
        print(
            "nmt_question_requests_total"
        )

        print()
        print(
            "Created questions:"
        )
        print(
            "nmt_questions_created_total"
        )

        print()

    except requests.exceptions.ConnectionError:
        print(
            "[ERROR] API is unavailable. "
            "Run Docker Compose first."
        )
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(
            f"[ERROR] HTTP request failed: {error}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()