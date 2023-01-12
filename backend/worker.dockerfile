FROM python:3.9

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

ENV C_FORCE_ROOT=1

COPY ./app/wait-for-it.sh /bin/wait-for-it.sh
RUN ["chmod", "+x", "/bin/wait-for-it.sh"]

COPY ./app/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh

COPY ./app/worker-beat-start.sh /worker-beat-start.sh
RUN chmod +x /worker-beat-start.sh

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

CMD ["bash", "/worker-start.sh"]
# CMD ["bash", "/worker-beat-start.sh"] # For beat
