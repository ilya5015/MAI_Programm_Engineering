FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src

CMD ["bash", "-c", "python src/init_orders.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]

