FROM python:3.12

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main.py"]