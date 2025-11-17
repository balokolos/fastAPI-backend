pip install -r requirements.txt

uvicorn app.main:app --reload

http://127.0.0.1:8000/employee?emp_id=100


#If using Instant Client

Current code does not use instant client. Please google to learn about insatnt client.

1. Download Instant Client

Go to:

👉 https://www.oracle.com/database/technologies/instant-client/downloads.html

mkdir -p /opt/oracle
unzip instantclient-basic-linux.x64.zip -d /opt/oracle

export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13:$LD_LIBRARY_PATH

echo 'export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_13:$LD_LIBRARY_PATH' >> ~/.bashrc

python -c "import cx_Oracle; print(cx_Oracle.clientversion())"




# Docker

docker build -t fastapi-oracle .


docker run -d -p 8000:8000 --env-file .env fastapi-oracle


