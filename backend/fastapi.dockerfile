FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app/

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends ffmpeg libsm6 libxext6 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app/wait-for-it.sh /bin/wait-for-it.sh
RUN ["chmod", "+x", "/bin/wait-for-it.sh"]

COPY ./app /app
ENV PYTHONPATH=/app
