FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY ./alembic ./alembic
COPY ./src ./src

CMD ["bash", "-c", "alembic upgrade head && python src/init_admin.py && python src/init_dummy_users.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

