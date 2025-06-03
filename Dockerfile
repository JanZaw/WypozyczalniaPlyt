FROM python:3.11-slim


COPY music/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY music .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
