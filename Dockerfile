FROM python

WORKDIR google-sheet

COPY . .

ENV TZ="Asia/Tashkent"

RUN pip install -r requirements.txt

CMD [ "python", "-u", "run.py" ]