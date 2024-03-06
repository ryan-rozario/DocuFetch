FROM python:3
ARG BASE_URL
RUN mkdir /src
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python3 ./data-loader/main.py ${BASE_URL}
CMD ["uvicorn", "data-retriver.server:app", "--host=0.0.0.0", "--port=8080"]
