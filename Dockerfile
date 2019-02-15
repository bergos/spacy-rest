FROM python:3

ENV SPACY_MODEL=en_core_web_sm

RUN pip install flask flask-restful spacy
RUN python -m spacy download $SPACY_MODEL

ADD server.py /

CMD [ "python", "./server.py" ]
