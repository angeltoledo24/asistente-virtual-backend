FROM python:3.11.4-alpine3.17
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN  apk update \
    && apk add --no-cache gcc python3-dev libffi-dev \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]
