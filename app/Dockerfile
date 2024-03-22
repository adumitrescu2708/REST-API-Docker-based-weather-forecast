FROM python:3.9

# set working directory
WORKDIR /app

# upgrade pip
RUN pip install --upgrade pip

# install requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy required sources
COPY . /app

# run on port 6000
EXPOSE 6000

# command to run server
CMD ["python", "app.py"]
