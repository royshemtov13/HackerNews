FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry install --only main

CMD ["poetry", "run", "uvicorn", "hackernews.app:app", "--host", "0.0.0.0", "--port", "8000"]
