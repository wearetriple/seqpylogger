FROM python:3.8-slim-buster AS compile-image
 
WORKDIR /code
 
RUN apt-get update -y --fix-missing; \
    apt-get install -y git python3-dev gcc build-essential
 
# Install latest pip version and pipenv for dependency installation
RUN pip install --upgrade pip && pip install pipenv
 
RUN python -m venv /opt/venv
 
ENV PATH="/opt/venv/bin:$PATH"
 
# Copy Pipfile for dependency installation
COPY Pipfile /code/
# (Optional) copy lockfile as well
COPY Pipfile.lock /code/
# Alternatively use requirements.txt
#COPY requirements.txt /code/
 
# Ensure pipenv installs in /opt/venv
RUN . /opt/venv/bin/activate && pipenv install
# When using requirements.txt
#RUN . /opt/venv/bin/activate && pipenv install -r requirements.txt
# Or simply install using pip
#RUN pip install -r requirements.txt
 
# Create a new clean image without all installation dependencies like build-essential
FROM python:3.8-slim-buster AS build-image
 
# Copy python dependencies
COPY --from=compile-image /opt/venv /opt/venv
 
ENV PATH="/opt/venv/bin:$PATH"
 
RUN mkdir /code
WORKDIR /code
 
# Copy all required project files
COPY seqpylogger /code/seqpylogger
COPY application.py /code/
 
# (Optional) copy init.sh startup script
COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
 
# (Optional) Hint exposed port
EXPOSE 8080
 
# Set default shell
ENTRYPOINT ["/bin/bash"]
# Run startup command on shell
CMD [ "-c", "init.sh" ]