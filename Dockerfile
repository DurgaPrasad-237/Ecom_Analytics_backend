# it means use python 3.11 base iamge
FROM python:3.11-slim 

# set the workingdirectory inside the docker container to /app
# Your project on Windows: E:\indian_ecom\indian_ecommerce_analytics_backend -> in out system where our project is
# Your project inside Docker: /app -> in docker our projec inside docker
WORKDIR /app

# copy dependencies and installments
COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# copies project file in contianer
COPY . .

# documetn the api report
EXPOSE 8000

# start fastapi applicaation
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]