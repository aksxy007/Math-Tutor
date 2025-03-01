FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0","--port", "8000"]