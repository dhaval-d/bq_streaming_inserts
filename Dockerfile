# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ADD app.py /
ADD requirements.txt /
ADD bq-editor.json /

# Install production dependencies.
RUN pip install -r requirements.txt

CMD [ "python", "./app.py", "--project", "google.com:testdhaval", "--dataset", "datastudio_demo", "--table", "rides" ]
