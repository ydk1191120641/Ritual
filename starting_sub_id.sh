#!/bin/bash

# 检查是否传入了 sub_id 参数
if [ -z "$1" ]; then
    sub_id="263058"
else
    # 获取 sub_id 参数
    sub_id="$1"
fi



# 示例：打印 sub_id
echo "接收到的 sub_id: $sub_id"
# RPC_URL="https://mainnet.base.org"
# RPC_URL_SUB="https://mainnet.base.org/"
# 替换 registry 地址
REGISTRY="0x3B1554f346DFe5c482Bb4BA31b880c1C18412170"
SLEEP=3

START_SUB_ID=160000
BATCH_SIZE=800  # 推荐使用公用 RPC
TRAIL_HEAD_BLOCKS=3
INFERNET_VERSION="1.4.0"  # infernet 镜像标签

 
# 修改 config.json / Deploy.s.sol / docker-compose.yaml / Makefile
 

# 修改 deploy/config.json
# sed -i 's|"rpc_url": ".*"|"rpc_url": "https://mainnet.base.org"|' /root/infernet-container-starter/deploy/config.json
# sed -i 's|"rpc_url": ".*"|"rpc_url": "https://mainnet.base.org"|' /root/infernet-container-starter/projects/hello-world/container/config.json
sed -i "s|\"batch_size\": [0-9]*|\"batch_size\": $BATCH_SIZE|" /root/infernet-container-starter/deploy/config.json
sed -i "s|\"sleep\": [0-9]\+\(\.[0-9]\+\)\?|\"sleep\": $SLEEP|" /root/infernet-container-starter/deploy/config.json
sed -i "s|\"sleep\": [0-9]\+\(\.[0-9]\+\)\?|\"sleep\": $SLEEP|" /root/infernet-container-starter/projects/hello-world/container/config.json

sed -i "s|\"sync_period\": [0-9]\+\(\.[0-9]\+\)\?|\"sync_period\": 30|" /root/infernet-container-starter/deploy/config.json
sed -i "s|\"sync_period\": [0-9]\+\(\.[0-9]\+\)\?|\"sync_period\": 30|" /root/infernet-container-starter/projects/hello-world/container/config.json
sed -i "s|\"starting_sub_id\": [0-9]\+\(\.[0-9]\+\)\?|\"starting_sub_id\": $sub_id|" /root/infernet-container-starter/deploy/config.json
sed -i "s|\"starting_sub_id\": [0-9]\+\(\.[0-9]\+\)\?|\"starting_sub_id\": $sub_id|" /root/infernet-container-starter/projects/hello-world/container/config.json
# 修改 projects/hello-world/container/config.json

sed -i "s|\"batch_size\": [0-9]*|\"batch_size\": $BATCH_SIZE|" /root/infernet-container-starter/projects/hello-world/container/config.json


# 修改 Deploy.s.sol
# sed -i "s|\(RPC_URL\s*=\s*\).*|\1\"$RPC_URL\";|" /root/infernet-container-starter/projects/hello-world/contracts/script/Deploy.s.sol

# 使用 latest node 镜像
# 修改 Makefile (sender, RPC_URL)
MAKEFILE_PATH="/root/infernet-container-starter/projects/hello-world/contracts/Makefile"
# sed -i "s|^RPC_URL := .*|RPC_URL := $RPC_URL|"    "$MAKEFILE_PATH"
