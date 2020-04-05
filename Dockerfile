FROM python:3.8.2-slim
WORKDIR /opt/project
RUN pip install --upgrade pip && pip --no-cache-dir install poetry
COPY ./pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY . ./
CMD ["python", "main.py"]