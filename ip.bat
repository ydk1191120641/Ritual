#!/bin/bash

# 更新包列表
sudo apt update

# 设置端口
t=10000

# 安装 Dante 服务器
sudo apt install -y dante-server

# 使用 echo 直接写入配置文件，而不是使用 nano，因为 nano 是交互式编辑器
sudo bash -c "cat > /etc/danted.conf << EOF
logoutput: syslog
internal: eth0 port = $t
external: eth0

method: username
user.privileged: root
user.notprivileged: nobody

client pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    log: connect disconnect error
}

socks pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    command: connect
    log: connect error
    method: username
}

socks pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    command: bind
    log: connect error
    method: username
}
EOF"

echo "Dante configuration has been updated."

# 创建新用户
sudo useradd -m 888 --badname

# 设置新用户的密码
new_password="888"
echo "888:$new_password" | sudo chpasswd

# 检查密码是否设置成功
if [ $? -eq 0 ]; then
    echo "Password for user '888' has been set successfully."
else
    echo "Failed to set password for user '888'."
fi

# 配置防火墙
sudo ufw allow $t/tcp
sudo ufw allow $t/udp
sudo ufw reload

# 启动并配置 Dante 服务
sudo systemctl start danted
sudo systemctl enable danted  # 使其开机自启动
sudo systemctl status danted  # 检查服务状态