FROM python:3.7-slim as compile-image

WORKDIR /discussremover/
COPY requirements.txt /discussremover/
RUN pip install --user -r requirements.txt
COPY . /discussremover/

FROM python:3.7-alpine as run-image

COPY --from=compile-image /root/.local /root/.local
COPY --from=compile-image /discussremover/ /discussremover/

ENV PATH=/root/.local/bin:$PATH
CMD ["python3", "/discussremover/bot.py"]