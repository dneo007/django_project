FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pwd
EXPOSE 80
CMD [ "python", "./django/manage.py", "runserver", "0.0.0.0:80"]
