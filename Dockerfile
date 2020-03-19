FROM python:3.7-slim

WORKDIR /discussremover

COPY requirements.txt /discussremover/
RUN pip install -r /discussremover/requirements.txt
COPY . /discussremover/

CMD python3 /discussremover/main.py