FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ../
RUN pip install --no-cache-dir -r ../requirements.txt && mkdir /usr/log
COPY . .
CMD ["python", "./src/ingest_blocks.py"]

