FROM python:slim

#And the whole Flask / Jinja thing

RUN pip install flask

#We also want a user
RUN useradd -r flask
USER flask

#And then what we want to override
WORKDIR /opt
ADD ./opt /opt

CMD ["flask", "run", "--host=0.0.0.0"]
