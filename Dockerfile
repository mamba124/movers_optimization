FROM python:3.8.2

ENV START=16

ENV FINISH=8

WORKDIR app/

#CMD ["python", " -m pip install --upgrade pip"]
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY secret_files/ ./secret_files

COPY . .

CMD ["python", "api.py"]
