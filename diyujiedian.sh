#!/bin/bash

# 创建清理脚本
cat > /root/json_cleaner.sh << 'EOF'
#!/bin/bash

# 日志文件路径
LOG_FILE="/root/rm.log"

# 确保日志文件存在
touch $LOG_FILE

# 记录脚本启动
echo "$(date +"%Y%m%d%H")--清理脚本启动" >> $LOG_FILE

# 定义清理函数
clean_json_files() {
    # 获取当前日期时间，格式为年月日时
    local timestamp=$(date +"%Y%m%d%H")
    
    # 执行docker命令
    if docker exec infernet-anvil /bin/sh -c "cd /root/.foundry/anvil/tmp/ && find . -name '*.json' -type f -delete"; then
        # 删除，json日志
        echo "${timestamp}--删除成功" >> $LOG_FILE
    else
        # 记录错误
        echo "${timestamp}--删除失败" >> $LOG_FILE
    fi
    # 执行docker命令
    if docker exec infernet-node /bin/sh -c "find . -type f -name '*infernet_node*' -exec rm -f {} \;"; then
        # 删除，json日志
        echo "${timestamp}--删除成功" >> $LOG_FILE
    else
        # 记录错误
        echo "${timestamp}--删除失败" >> $LOG_FILE
    fi

    # 提取 MergedDir
    MERGED_DIR=$(docker inspect infernet-anvil | jq -r '.[0].GraphDriver.Data.MergedDir')

    if [ -z "$MERGED_DIR" ]; then
        echo "无法获取 MergedDir 路径"
        exit 1
    fi

    echo "找到 MergedDir: $MERGED_DIR"

    # 2. 确定目标
    TARGET_DIR="${MERGED_DIR}/root/.foundry/anvil/tmp"

    if [ ! -d "$TARGET_DIR" ]; then
        echo "目标目录不存在: $TARGET_DIR"
        exit 1
    fi

    echo "正在处理目录: $TARGET_DIR"

    # 3. 重命名子文件夹
    for folder in "$TARGET_DIR"/*; do
        if [ -d "$folder" ]; then
            # 生成随机字符串
            NEW_NAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
            PARENT_DIR=$(dirname "$folder")
            mv "$folder" "$PARENT_DIR/$NEW_NAME"
            echo "将 $(basename "$folder") 重命名为 $NEW_NAME"
        fi
    done

    echo "所有文件夹已随机重命名"
}

# 立即执行一次
clean_json_files

# 主循环，每小时执行一次
while true; do
    # 计算下一个整点的等待时间
    minutes=$(date +"%M")
    seconds=$(date +"%S")
    sleep_seconds=$(( (60 - $minutes) * 60 - $seconds ))
    
    # 休眠到下一个整点
    sleep 60
    
    # 执行清理函数
    clean_json_files
done
EOF

# 设置执行权限
chmod +x /root/json_cleaner.sh

# 创建systemd服务文件
cat > /etc/systemd/system/json-cleaner.service << 'EOF'
[Unit]
Description=JSON Cleaner Service for Infernet Anvil
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStart=/bin/bash /root/json_cleaner.sh
Restart=always
RestartSec=10
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

# 重新加载systemd配置
systemctl daemon-reload

# 启用并启动服务
systemctl enable json-cleaner.service
systemctl start json-cleaner.service

#设置docker开机自启
sudo systemctl enable docker
docker update --restart=always $(docker ps -a -q)

sudo systemctl stop unattended-upgrades && sudo systemctl disable unattended-upgrades && sudo systemctl stop apt-daily.service && sudo systemctl disable apt-daily.service && sudo systemctl stop apt-daily-upgrade.service && sudo systemctl disable apt-daily-upgrade.service && sudo systemctl stop apt-daily.timer && sudo systemctl disable apt-daily.timer && sudo systemctl stop apt-daily-upgrade.timer && sudo systemctl disable apt-daily-upgrade.timer

echo "已成功安装并启动"
echo "服务状态："
systemctl status json-cleaner.service
