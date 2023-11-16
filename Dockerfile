FROM rasa/rasa-sdk:1.10.2

WORKDIR /app

# Switch to root user temporarily to install system packages
USER root

RUN chown -R 1000:1000 /opt/venv


# Install the required system package for psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the non-root user
USER 1000

COPY ./actions /app/actions

# Install Python dependencies
RUN pip install psycopg2-binary

# Uncomment the following line if you have a separate requirements.txt file
# COPY actions/requirements.txt ./

# RUN pip install -r requirements.txt
