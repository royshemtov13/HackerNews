FROM python:3.12

ENV PYTHONUNBUFFERED=true

RUN pip install poetry==1.4

WORKDIR /code

COPY . .

WORKDIR /code/hackernews

RUN poetry install --only main

CMD ["poetry", "run", "python", "hackernews/main.py"]