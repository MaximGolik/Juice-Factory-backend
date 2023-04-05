# start by pulling the python image
FROM python:3.10-alpine
# copy the requirements file into the image
ENV PYTHONUNBUFFERED 1
ENV FLASK_RUN_HOST=0.0.0.0
COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app
# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# copy every content from the local file to the image
COPY . /app
EXPOSE 5000
# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["app.py"]