FROM python:3.9.15

CMD ["python", "main.py"]
WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip && \
    wget http://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . /app
