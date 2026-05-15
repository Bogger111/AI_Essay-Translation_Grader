import os

from dotenv import load_dotenv
from openai import OpenAI

from prompt import build_prompt
from rag import retrieve_knowledge


load_dotenv()


def _setting(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st

        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass

    return default


def _client() -> OpenAI:
    api_key = _setting("OPENAI_API_KEY")
    base_url = _setting("BASE_URL")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    return OpenAI(api_key=api_key, base_url=base_url)


MODEL = _setting("MODEL", "deepseek-chat")


def grade_submission(exam_type, task_type, task_text, answer_text):
    knowledge = retrieve_knowledge(task_text + "\n" + answer_text)
    prompt = build_prompt(
        task_text,
        answer_text,
        knowledge,
        exam_type=exam_type,
        task_type=task_type,
    )

    response = _client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


def grade_essay(topic, essay, exam_type="CET-4"):
    return grade_submission(exam_type, "essay", topic, essay)


if __name__ == "__main__":
    print("Enter exam type, for example CET-4 / CET-6 / TOEFL / IELTS / GRE:")
    exam_type = input().strip() or "CET-4"

    print("Enter task type: essay / translation")
    task_type = input().strip() or "essay"

    print("Enter topic or source text:")
    topic = input().strip()

    print("Enter student answer. Type END on a new line to finish:")
    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    essay = "\n".join(lines)

    print("\nGrading, please wait...\n")
    result = grade_submission(exam_type, task_type, topic, essay)
    print(result)
