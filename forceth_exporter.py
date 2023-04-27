#encoding: utf-8

import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask, request, current_app
import os
import sys


Forceth_RPC = sys.argv[1]

NodeFlask = Flask(__name__)

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp

class RpcGet(object):
    def __init__(self, Forceth_RPC):
        self.Forceth_RPC = Forceth_RPC

    def get_forceth_info(self):
        headers = {"Content-Type":"application/json"}
        data = '{"id":83, "jsonrpc":"2.0", "method":"eth_blockNumber", "params":[]}'
        try:
            r = requests.post(
                url="%s" %(self.Forceth_RPC),
                data=data,
                headers=headers
            )
            replay = r.json()["result"]
            return {
                "last_blocknumber": convert_int(replay),
            }
        except:
            return {
                "last_blocknumber": "-1",
            }

@NodeFlask.route("/metrics/forceth")
def rpc_get():
    CKB_Chain = CollectorRegistry(auto_describe=False)
    Get_Forceth_Info = Gauge("Get_Forceth_LastBlockInfo",
                                   "Get LastBlockInfo, Show Forceth latest block height",
                                   ["forceth_rpc"],
                                   registry=CKB_Chain)

    get_result = RpcGet(Forceth_RPC)
    forceth_last_block_info = get_result.get_forceth_info()
    Get_Forceth_Info.labels(
        forceth_rpc=Forceth_RPC
    ).set(forceth_last_block_info["last_blocknumber"])
    return Response(prometheus_client.generate_latest(CKB_Chain), mimetype="text/plain")

if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0",port=3000)
