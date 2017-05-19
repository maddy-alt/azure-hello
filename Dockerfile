FROM python:3

EXPOSE 8080

RUN mkdir -p /usr/src/hello-world
COPY src /usr/src/hello-world/src

WORKDIR /usr/src/hello-world/src

RUN pip install -r requirements.txt

CMD python3 app.py
