FROM python:3.7
ENV DEBIAN_FRONTEND noninteractive

COPY ./backend /usr/src/
WORKDIR /usr/src/

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python", "server.py"]
