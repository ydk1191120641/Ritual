#!/usr/bin/env bash
pip3 install requests pytz paramiko screen
echo "检查 screen 会话 ritual 是否存在..."
if screen -list | grep -q "see"; then
    echo "[提示] 发现 see 会话正在运行，正在终止..."
    screen -S see -X quit
    sleep 1
fi

echo "在 screen -S see 会话中开始容器部署" 
screen -S see -dm bash -c 'wget -O see.py https://raw.githubusercontent.com/ydk1191120641/Ritual/refs/heads/main/see.py && sed -i 's/\r$//' see.py && chmod +x see.py'
