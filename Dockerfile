FROM python:3.9.12

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Europe/Moscow

EXPOSE 5000

CMD ["flask", "run"]