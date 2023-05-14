FROM python:3.9.7-slim
RUN pip3 install pyzmq
COPY sink /
COPY middleware.py /middleware.py
ENTRYPOINT ["/bin/sh"]