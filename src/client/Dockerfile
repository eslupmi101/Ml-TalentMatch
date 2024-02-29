FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /app/requirements.txt --no-cache-dir 

COPY . .

RUN  reflex init

CMD ["reflex", "run", "--env", "prod"]
