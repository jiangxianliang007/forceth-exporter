# forceth-exporter

run in docker
```
docker run -d -it -p 3000:3000 -e forceth_rpc=http://172.31.7.223:8645 jiangxianliang/forceth-exporter:v1

curl http://127.0.0.1:3000/metrics/forceth
```
