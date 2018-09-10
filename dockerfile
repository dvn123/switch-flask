FROM python:3.7-slim
WORKDIR /switch
ADD . /switch
EXPOSE 4000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python","index.py"]
#CMD ["flask", "run --host=IP --port=PORT",]
#CMD ["flask run"]