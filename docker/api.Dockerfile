FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD [ "fastapi", "run" ]