FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Create downloadable directory
RUN mkdir -p app/downloadable

COPY . .

EXPOSE 5000

CMD ["python", "app/main.py"]
