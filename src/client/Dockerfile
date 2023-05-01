FROM python:3.9.7-slim
RUN pip3 install pyzmq
RUN pip3 install haversine
COPY client /
ENTRYPOINT ["/bin/sh"]