FROM python

WORKDIR google-sheet

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "run.py" ]