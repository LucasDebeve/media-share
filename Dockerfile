FROM python:3.9-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN mkdir uploads -p 

CMD ["python3", "-m", "flask", "--app=file_upload", "run", "--host=0.0.0.0", "--port=5000"]