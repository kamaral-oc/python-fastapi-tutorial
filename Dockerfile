# Use ARG to specify user and group details
ARG USER_NAME=appuser
ARG GROUP_NAME=appgroup
ARG UID=1001
ARG GID=1001

FROM python:3.9

# Create a non-root user and group with a specific UID and GID
RUN addgroup --gid ${GID} ${GROUP_NAME} && \
    adduser --disabled-password --gecos "" --uid ${UID} --gid ${GID} ${USER_NAME}

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app

# Change the ownership of the application files to the non-root user
RUN chown -R ${USER_NAME}:${GROUP_NAME} /code

# Switch to the non-root user
USER ${USER_NAME}

# Start the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
