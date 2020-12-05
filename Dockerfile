FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r req.txt

EXPOSE 5000

ENTRYPOINT ["flask"]
CMD ["run"]