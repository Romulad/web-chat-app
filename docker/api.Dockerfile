FROM python:3.10-alpine

WORKDIR /api

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN addgroup -S api && adduser -G api -S api-user
RUN chown api-user:api /api

EXPOSE 8000

USER api-user

CMD [ "fastapi", "run", "--root-path", "/open-chat-api" ]