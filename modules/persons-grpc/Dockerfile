FROM python:3.8

WORKDIR .

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app/main.py"]