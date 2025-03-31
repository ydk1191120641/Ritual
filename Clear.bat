#!/bin/bash

# 配置参数
FOLDER="/var/lib/docker/overlay2"  # 要监控的文件夹路径
MAX_SIZE_GB=20                      # 最大大小（单位：GB）
TMAX_SIZE_GB=20                      # 最大大小（单位：GB）
CHECK_INTERVAL=60                  # 检查间隔（单位：秒）
COMMAND="echo '文件夹大小超过 ${MAX_SIZE_GB}GB，已执行命令'"  # 要执行的命令

# 检查文件夹是否存在
if [ ! -d "$FOLDER" ]; then
    echo "错误：文件夹 $FOLDER 不存在"
    exit 1
fi

# 无限循环监控
while true; do
    # 使用 du 获取文件夹大小（单位：KB），然后转换为 GB
    SIZE_KB=$(du -s "$FOLDER" 2>/dev/null | awk '{print $1}')
    if [ -z "$SIZE_KB" ]; then
        echo "错误：无法获取 $FOLDER 的大小，可能权限不足"
        exit 1
    fi
    SIZE_GB=$(echo "scale=2; $SIZE_KB / 1024 / 1024" | bc)

    # 打印当前大小
    echo "当前文件夹 $FOLDER 大小：${SIZE_GB}GB"

    # 比较大小（使用 bc 进行浮点数比较）
    EXCEEDS=$(echo "$SIZE_GB >= $MAX_SIZE_GB" | bc)
    if [ "$EXCEEDS" -eq 1 ]; then
        echo "文件夹大小已超过 ${MAX_SIZE_GB}GB，执行命令删除..."
        docker exec infernet-anvil /bin/sh -c "find /root/.foundry/anvil/tmp/* -maxdepth 1 -name '*.json' -type f -delete"
    fi

    # 使用 du 获取文件夹大小（单位：KB），然后转换为 GB
    TSIZE_KB=$(du -s "$FOLDER" 2>/dev/null | awk '{print $1}')
    if [ -z "$TSIZE_KB" ]; then
        echo "错误：无法获取 $FOLDER 的大小，可能权限不足"
        exit 1
    fi
    TSIZE_GB=$(echo "scale=2; $TSIZE_KB / 1024 / 1024" | bc)

    # 打印当前大小
    echo "当前文件夹 $FOLDER 大小：${TSIZE_GB}GB"

    TEXCEEDS=$(echo "$TSIZE_GB >= $TMAX_SIZE_GB" | bc)
    if [ "$TEXCEEDS" -eq 1 ]; then
        echo "文件夹大小已超过 ${TMAX_SIZE_GB}GB，执行命令部署..."
        if screen -list | grep -q "ritual"; then
	    echo "[提示] 发现 ritual 会话正在运行，正在终止..."
	    screen -S ritual -X quit
	    sleep 1
	fi
	
	echo "在 screen -S ritual 会话中重新容器启动部署..."
	screen -S ritual -dm bash -c 'docker compose -f /root/infernet-container-starter/deploy/docker-compose.yaml down && docker compose -f /root/infernet-container-starter/deploy/docker-compose.yaml up -d && bash'
	sleep 1
    fi

    # 等待指定的时间间隔
    echo "等待指定的时间间隔：${CHECK_INTERVAL}秒"
    sleep "$CHECK_INTERVAL"
done

echo "脚本结束"
