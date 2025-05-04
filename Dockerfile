FROM python:3.13.3

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 19874

CMD ["uvicorn", "agiota:app", "--host", "0.0.0.0", "--port", "19874", "--workers", "10"]	
#uvicorn agiota:app --host 0.0.0.0 --port 19874 --workers 4 --reload
#ngrok http http://localhost:19874