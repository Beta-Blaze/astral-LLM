FROM python:3.8.16-alpine3.17

WORKDIR /opt/app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]