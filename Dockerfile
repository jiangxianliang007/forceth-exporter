FROM python:3.9

WORKDIR /config
COPY ./forceth_exporter.py ./requirements.txt /config/
RUN pip3 install -r requirements.txt
ENV PORT=3000

CMD "python3" "forceth_exporter.py" "$forceth_rpc"
