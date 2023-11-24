# syntax=docker/dockerfile:1

FROM python:3.9.2

WORKDIR web

COPY * /web/

# COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]
