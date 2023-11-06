FROM rasa/rasa-sdk:1.10.2

WORKDIR /app


# COPY actions/requirements.txt ./

USER root

COPY ./actions /app/actions

# RUN pip install -r requirements.txt

USER 1000 

