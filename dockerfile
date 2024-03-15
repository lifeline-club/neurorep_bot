FROM python:latest

WORKDIR /bot

COPY . /bot

RUN python3 -m pip install poetry

RUN poetry install

CMD ["poetry", "run", "python3", "-m", "bot"]
