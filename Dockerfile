FROM python:3.8-slim-buster

WORKDIR /server

RUN pip3 install Flask pymongo prometheus_client


COPY server.py .

ENV FLASK_APP=/server/server.py 

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
