FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

RUN useradd --system --user-group app

WORKDIR /app/prediction-app-backend
COPY requirements.txt requirements.txt
RUN pip install --quiet --no-cache-dir -r requirements.txt

EXPOSE 5001
COPY . .

RUN chown -R app:app /app/
USER app

