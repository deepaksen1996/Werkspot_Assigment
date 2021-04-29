FROM python:3.7-slim AS compile-image
# RUN python -m venv /opt/venv
RUN mkdir -p /mydir/
WORKDIR /mydir/
COPY main.py /mydir/
COPY event_log.csv /mydir/
COPY requirements.txt /mydir/
# RUN /opt/venv/bin/python -m pip install --upgrade pip
RUN  pip3 install -r requirements.txt
RUN ls
RUN pwd
# run the application
ENTRYPOINT ["python3", "main.py"]