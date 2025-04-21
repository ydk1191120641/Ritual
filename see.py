    import json
    from time import sleep
    import requests
    from datetime import datetime
    import pytz
    import paramiko
    from concurrent.futures import ThreadPoolExecutor
    import queue
    import time
    import smtplib
    from email.message import EmailMessage
    import re
    walletsnum = {}
    update = {}

    def send_email(sender_email, sender_password, recipient_email, subject, body):
        # 创建邮件对象
        msg = EmailMessage()
        msg.set_content(body)  # 设置邮件正文
        msg['Subject'] = subject  # 邮件主题
        msg['From'] = sender_email  # 发件人
        msg['To'] = recipient_email  # 收件人

        try:
            # 连接腾讯企业邮箱 SMTP 服务器（使用 SSL）
            with smtplib.SMTP_SSL("smtp.exmail.qq.com", 465) as server:
                # 登录邮箱
                server.login(sender_email, sender_password)
                # 发送邮件
                server.send_message(msg)
                print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败：{e}")


    # 配置参数
    sender_email = "yandaokun@ntmtkj.wecom.work"  # 替换为你的企业邮箱地址
    sender_password = "1993YDKgyq"  # 替换为你的邮箱密码或授权码
    recipient_email = "1983980885@qq.com"  # 替换为目标邮箱地址

    # 钱包地址数组
    wallets = [
        '0x06bd5eb9645A0733F8d2027A78a779fa6C42b08e',
        '0x65c8E6E1c443554fA1F385bf6CE4495ba1eaFA3c',
        '0xE8D974cB4bD6b604cD1e952deE8B57ed22E4230A',
        '0xF43D6dE32a71C2A561CEE5d758304cfb12684e2d',
        '0xbAFB1fe4941431f4b39d8C6BCbC18D14e6512fC6',
        '0x58344fFc973FB97B54542f652B281dFf631C88A3',
        '0x999Db68c0DB29Ad5C8f24912AF68FD18D5Cffa1B',
        '0x0fa27987D02fBC5263879a1b5618459f71f7947d',
        '0xCd9f9F1243ea82ae304f6f23C79A7A0A88506Cf1',
        '0x2b9518721a0035a2B78759cFB51bEe1b1480c203',
        '0x61D65d3A6e72CaD5f0FbA4C596B347733033Ebc6',
        '0xC7521d67e2D7d6258C4EbE013AcCF54d3bba7212',
        '0x031AD236938a9d68a36B7B611B87CA6EaB02acA8',
        '0xf438ca2976Ab65A932C1c036a2D9edc10408bFFe',
        '0x99b03AF1bad5Fae85C646594900aB06c5b1efB0f',
        '0x082c34914119B7cBDe3A72C60D90A4fA5CFFF61B',
        '0xe5aDBBc371a4cAE8CA0947072daA56c8eAB6e467',
        '0xbfF33B4C1EdE8883655fFa370c4c4B40b76fC2F4',
        '0xeA83A7008A2A229866f97c609446F7a3e1E1ddEc',
        '0x224D80e3B3aCbaDf6193D2D68d05C5FFCB2ef59c',
        '0xDfA67dc7B5c716038BB2491808d4cCDB34770f36',
        '0x86F89c3f941fD55D210dd4Aec498DdcD8B66d829',
        '0xE5D2800bd434C9a7D89Ae3747fddB132AFFB0035',
        '0x160C7FbA44e124A2774Aa92d55b096f860D0B29e',
        '0x405ED75FC41e795EA9a62D04f8007ABd5Da24AeC',
        '0xC9079C5cD2d7BAD222c82a5e474D55d049773A5E',
        '0xAb12A6137E0950202f54B56937EEe3da9628bb3B',
        '0x6D9B12C2068b4E6f82F4A272893B47f24A327859',
        '0xcb0F68f4e04742d9573fF79C0851c69C9d754195',
        '0x074a309c4aa50227A92BD49e0cd69C2AAe5F932a',
        '0x9D8d1a39AD998CA89d2Ec75FA29498a1E960e35C',
        '0x71f0fBE64400D088378eca7Cee3Ab3456e88f262',
        '0x18E990065759517fb2fb4431211cBEc5Ac54ca32',
        '0xB08d035A5e4A57B69936501C270f4e964249dfcc',
        '0x316646D904F433F1fFe0A008D638685f413A54C6',
        '0xA8c3C5d834cBFE10B183eaf004A74CDFA76386E7',
        '0xa9830D4222Df2C962021562893D1482c60403482',
        '0x5F8BCC75B654Ada684e14e354b7976C24a632878',
        '0x3898F055Dd754Bc1078a7D82f27B7fbf187F062C',
        '0x42E70F4Dca2F0ba430b9C65B51136b76943dE5F9',
        '0x1900C55727588B7c923ba5077C5d4369123715f8',
        '0x1a8e86F1207A6Ba9E3959F70c3fF24e0c5B8aCd5',
        '0x9a76cE8A8448293074Dd145bbC387eF778883833',
        '0x08e5B2C3c52b92981D7E0Cb46176cE73025B0018',
        '0xA4d95E7FFb415f73d5d79525d9777b158201361C',
        '0x1E03E3EC229151b5a44C069E3aE7DAD36b759BB8',
        '0xC14F9d18115cc3665480ef3873607AeF66ae4f85',
        '0xC3AdE47C4E1bb6d36d8Ef9c8083bcb1f073EcE0b',
        '0xeD01841D17E77e5080ba24b3C529f37fCBeF902F',
        '0xb453046B86Bc2a7C447653E63F19608E4DBf9865',
        '0xF8B90213b5E113d5bd9A155376A7230c2dab3B13',
    ]

    # BaseScan API 配置
    BASESCAN_API = 'https://api.basescan.org/api'
    API_KEY = '7DDEE4CZAI6GIGR76KC5RW2CJGDTMME8W8'  # 可选：填写你的 API Key，空也可以调用
    proxies = {
        'http': 'socks5h://888:888@38.247.10.115:10000',  # 本地代理地址和端口
        'https': 'socks5h://888:888@38.247.10.115:10000'
    }


    def get_latest_transactions(address, limit=5000):
        params = {
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': limit,
            'sort': 'desc',
            'apikey': API_KEY
        }

        response = requests.get(BASESCAN_API, params=params)
        data = response.json()
        # print(data)
        if data.get("status") != "1":
            return None
        return data["result"]


    def calculate_time_difference(start_time_str, timezone_str="Asia/Shanghai"):
        """计算与当前时间的时间差（小时）"""
        try:
            tz = pytz.timezone(timezone_str)
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            start_time = tz.localize(start_time)
            now = datetime.now(tz)
            delta = now - start_time
            hours_diff = delta.total_seconds() / 3600
            return int(hours_diff)
        except Exception as e:
            return f"时间解析错误: {e}"


    def main(index, wallet):
        MAX_RETRY = 9999  # 设置一个非常大的重试次数（或用 while True 无限循环）

        # for index, wallet in enumerate(wallets):

        # 自动重试获取交易
        for attempt in range(MAX_RETRY):
            try:
                transactions = get_latest_transactions(wallet)
                if not transactions:
                    pass
                break  # 成功则跳出重试循环
            except Exception as e:
                # print(f"  ❌ 获取交易失败（尝试第 {attempt + 1} 次）: {e}")
                sleep(1)  # 每次失败后等 3 秒再试
        # 如果 transactions 为空也继续打印逻辑
        n = 0
        t = ""
        list = [f"\n📬 第 {index} 个钱包地址: {wallet}"]
        if not transactions:
            list.append(f"    合约地址: ")
        for i, tx in enumerate(transactions, 1):
            try:
                if not t:
                    t = tx
                if tx.get('contractAddress', ''):
                    list.append(f"    合约地址: {tx['contractAddress']}")
                if tx['to'].upper() == '0XD85EE50DA419CC5AF83A1E70A91D5C630B8C650A'.upper():
                    n += 1
            except Exception as e:
                print(f"     ⚠️ 处理交易失败: {e}")
                continue
        list.append(
            f"    时间: {datetime.fromtimestamp(int(t['timeStamp']))} 距离现在 {calculate_time_difference(str(datetime.fromtimestamp(int(t['timeStamp']))))} 个小时没有发起验证")
        list.append(f"    发起验证次数: {n}")
        list.append("     =====================================================================")
        print("\n".join(list))
        if wallet not in walletsnum:
            walletsnum[wallet] = n
        else:
            if walletsnum[wallet] != n:
                walletsnum[wallet] = n
                print(f'钱包{wallet} 发钱新的验证了，总次数{n}')
                send_email(sender_email, sender_password, recipient_email, f"地狱节点{wallet}", f'钱包{wallet} 发钱新的验证了，总次数{n}')
        #         发送邮箱
        return ""


    def process_items_main(batch_size=4):
        """多线程处理数据，每次 batch_size 个"""
        results = []
        result_queue = queue.Queue()
        b = 0
        for i in range(0, len(wallets), batch_size):
            batch = wallets[i:i + batch_size]
            print(f"处理批次 {i // batch_size + 1}，任务数: {len(batch)}")
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                # futures = [
                #     executor.submit(main, index, item)
                #     for index, item in enumerate(batch)
                # ]
                for index, item in enumerate(batch):
                    executor.submit(main, b + 1, item)
                    b += 1
                # 等待当前批次完成
                # for future in futures:
                #     try:
                #         future.result()  # 确保捕获异常
                #     except Exception as e:
                #         print(f"线程任务异常: {e}")

            # 收集结果
            while not result_queue.empty():
                results.append(result_queue.get())

            time.sleep(1)  # 批次间短暂休眠，避免过载

        return results


    def connect_to_server(host, username, password=None, key_path=None, port=22):
        """建立 SSH 连接"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if password:
                ssh.connect(host, port, username, password)
            elif key_path:
                ssh.connect(host, port, username, key_filename=key_path)
            print("成功连接到服务器")
            return ssh
        except Exception as e:
            print(f"连接失败: {e} {host}")
            return None
    last_sub_id_map = {"last_sub_id":'245773'}
    def read_last_sub_id():
        try:
            with open("last_sub_id.txt", "r") as file:
                last_sub_id = file.read().strip()
                if last_sub_id:
                    print(f"从 last_sub_id.txt 读取到 last_sub_id={last_sub_id}")
                    return last_sub_id
                else:
                    print("文件 last_sub_id.txt 为空")
                    return None
        except FileNotFoundError:
            print("错误：last_sub_id.txt 文件不存在")
            return None
        except Exception as e:
            print(f"读取文件时发生错误：{str(e)}")
            return None
    def execute_docker_logs(ssh, container_name, ip, tail_lines=100):
        """执行 docker logs 命令并返回结果"""
        command = f"docker logs --tail {tail_lines} {container_name}"
        #    command = f"wget -O rpc.sh https://raw.githubusercontent.com/ydk1191120641/Ritual/refs/heads/main/rpc.sh && sed -i 's/\r$//' rpc.sh && chmod +x rpc.sh && ./rpc.sh"
        strs = [ip]
        list = []
        try:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                list.append(f"日志输出:{ip}")
                list.append(output)
                if (('Subscription completed' in output and 'subscription creation' in output) or (
                        'Running containers' in output and 'SUCCESS' in output)) and 'retrying in 448' not in output:
                    strs.append("地狱节点日志正常")
                    if 'Running containers' in output and 'SUCCESS' in output:
                        # 正则表达式
                        pattern = r"sub id is: (\d+)"

                        # 查找匹配
                        match = re.search(pattern, output)
                        # 提取值
                        if match:
                            last_sub_id = match.group(1)
                            last_sub_id_map['last_sub_id'] = str(int(last_sub_id)-1)

                        else:
                            print("未找到 last_sub_id 的值")
                else:
                    strs.append("地狱节点日志不正常")
            if error:
                print("错误信息:")
                print(error)
        except Exception as e:
            print(f"命令执行失败: {e}")
        if ip not in update:
            sub_id = read_last_sub_id()
            try:
                command = "wget -O starting_sub_id.sh https://raw.githubusercontent.com/ydk1191120641/Ritual/refs/heads/main/starting_sub_id.sh && sed -i 's/\r$//' starting_sub_id.sh && chmod +x starting_sub_id.sh && ./starting_sub_id.sh "+sub_id
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                if output:
                    print(output)
                if error:
                    print("错误信息:")
                    print(error)
            except Exception as e:
                print(f"命令执行失败: {e}")
            finally:
                update[ip] = 1
                pass

        try:
            command = f"docker ps -a"
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                list.append(output)
                if 'infernet-node' in output and 'infernet-anvil' in output and 'infernet-redis' in output and 'infernet-fluentbit' in output and 'hello-world' in output:
                    strs.append("地狱节点docker容器数量正常")
                else:
                    strs.append("地狱节点docker容器数量不正常")
                if "exited" in output.lower() or "dead" in output.lower() or "oom_killed" in output.lower() or "removing" in output.lower():
                    strs.append("地狱节点docker容器状态不正常")
                else:
                    strs.append("地狱节点docker容器状态正常")
            if error:
                print("错误信息:")
                print(error)
        except Exception as e:
            print(f"命令执行失败: {e}")
        finally:
            print("\n".join(list))
            return strs


    ips = [
        '156.239.40.237:xkkgATRF2869',
    ]


    def process_items(batch_size=30):
        """多线程处理数据，每次 batch_size 个"""
        results = []
        result_queue = queue.Queue()
        for i in range(0, len(ips), batch_size):
            batch = ips[i:i + batch_size]
            print(f"处理批次 {i // batch_size + 1}，任务数: {len(batch)}")
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                futures = [
                    executor.submit(sship, item, result_queue)
                    for item in batch
                ]
                # 等待当前批次完成
                for future in futures:
                    try:
                        future.result()  # 确保捕获异常
                    except Exception as e:
                        print(f"线程任务异常: {e}")

            # 收集结果
            while not result_queue.empty():
                results.append(result_queue.get())

            time.sleep(1)  # 批次间短暂休眠，避免过载
        reload = []
        for v in results:
            print(v)
            if "服务器关机" in "".join(v):
                print(f"服务器关机{v[0]}")
            elif "地狱节点docker容器数量不正常" in "".join(v):
                reload.append(v)
            elif "地狱节点docker容器状态不正常" in "".join(v):
                reload.append(v)
            elif "地狱节点日志不正常" in "".join(v):
                reload.append(v)
            print("==================================================")
        result_queue = queue.Queue()
        res = []
        for i in range(0, len(reload), 5):
            batch = reload[i:i + batch_size]
            print(f"处理批次重启 {i // batch_size + 1}，任务数: {len(batch)}")
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(dockerrun, item, result_queue)
                    for item in batch
                ]
                # 等待当前批次完成
                for future in futures:
                    try:
                        future.result()  # 确保捕获异常
                    except Exception as e:
                        print(f"线程任务异常: {e}")

            # 收集结果
            while not result_queue.empty():
                res.append(result_queue.get())

            time.sleep(1)  # 批次间短暂休眠，避免过载


        return results


    def sship(ip, result_queue):
        # list = []
        # for ip in ips:
        # 服务器连接信息
        ips = ip
        ip = ip.split(":")
        host = ip[0]  # 替换为你的服务器 IP
        username = "root"  # 替换为你的用户名
        password = ip[1]  # 如果使用密码认证
        # 服务器连接信息
        # key_path = "/path/to/your/private/key"  # 如果使用密钥认证
        container_name = "infernet-node"
        tail_lines = 100

        for i in range(3):
            # 连接服务器
            try:
                ssh = connect_to_server(host, username, password=password)
            finally:
                if not ssh:
                    # 发送邮箱
                    if i == 2:  # 发送邮箱
                        # 调用发送函数
                        send_email(sender_email, sender_password, recipient_email, f"地狱节点{ips}服务器关机", f"地狱节点{ips}服务器关机")
                        result_queue.put([f"地狱节点{ips}服务器关机"])
                        return
                        pass
                else:
                    break
        try:
            # 执行 docker logs 命令
            strs = execute_docker_logs(ssh, container_name, ":".join(ip), tail_lines)
        finally:
            # 关闭连接
            ssh.close()
            result_queue.put(strs)
            print("SSH 连接已关闭")


    def dockerrun(item,result_queue):
        # list = []
        # for ip in ips:
        # 服务器连接信息
        ip = item[0]
        ip = ip.split(":")
        host = ip[0]  # 替换为你的服务器 IP
        username = "root"  # 替换为你的用户名
        password = ip[1]  # 如果使用密码认证
        # 服务器连接信息
        # key_path = "/path/to/your/private/key"  # 如果使用密钥认证
        container_name = "infernet-node"
        tail_lines = 100

        # 连接服务器
        ssh = connect_to_server(host, username, password=password)
        if not ssh:
            return
        try:
            """执行 docker logs 命令并返回结果"""
            command = f"docker compose -f /root/infernet-container-starter/deploy/docker-compose.yaml down&&docker compose -f /root/infernet-container-starter/deploy/docker-compose.yaml up -d"
            strs = [ip]
            list = [f"正在重启docker"]
            list.append(json.dumps(item))
            try:
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                if output:
                    list.append(f"日志输出:{ip}")
                    list.append(output)
                if error:
                    print("错误信息:")
                    print(error)
            except Exception as e:
                print(f"命令执行失败: {e}")
        finally:
            # 关闭连接
            result_queue.put("\n".join(list))
            ssh.close()
            print("SSH 连接已关闭")

    ip_list = [
        "38.247.14.73",
        "38.247.15.67",
        "38.247.10.79",
        "38.247.15.94",
        "38.247.8.123",
        "38.247.13.78",
        "38.247.11.108",
        "38.247.14.76",
        "38.247.8.125",
        "38.247.15.80",
        "38.247.14.67",
        "38.247.14.72",
        "38.247.8.68",
        "38.247.13.86",
        "38.247.12.90",
        "38.247.8.109",
        "38.247.9.69",
        "38.247.11.102",
        "38.247.10.122",
        "38.247.11.82",
        "38.247.10.82",
        "38.247.10.81",
        "38.247.8.115",
        "38.247.15.87",
        "38.247.11.86",
        "38.247.11.98",
        "38.247.12.73",
        "38.247.13.81",
        "38.247.14.69",
        "38.247.10.117",
        "38.247.13.79",
        "38.247.8.77",
        "38.247.10.112",
        "38.247.10.85",
        "38.247.9.71",
        "38.247.14.89",
        "38.247.14.83",
        "38.247.9.89",
        "38.247.11.113",
        "38.247.9.116",
        "38.247.14.81",
        "38.247.10.77",
        "38.247.10.105",
        "38.247.15.75",
        "38.247.11.88",
        "38.247.8.124",
        "38.247.10.123",
        "38.247.8.114",
        "38.247.13.90",
        "38.247.13.84",
        "38.247.10.106",
        "38.247.15.93",
        "38.247.12.66",
        "38.247.12.78",
        "38.247.14.87",
        "38.247.12.72",
        "38.247.8.89",
        "38.247.15.85",
        "38.247.14.77",
        "38.247.9.80",
        "38.247.12.74",
        "38.247.8.82",
        "38.247.15.90",
        "38.247.8.73",
        "38.247.8.86",
        "38.247.9.86",
        "38.247.9.126",
        "38.247.11.99",
        "38.247.10.90",
        "38.247.11.90",
        "38.247.12.67",
        "38.247.10.120",
        "38.247.8.99",
        "38.247.10.86",
        "38.247.11.83",
        "38.247.12.89",
        "38.247.8.81",
        "38.247.14.84",
        "38.247.8.94",
        "38.247.9.103",
        "38.247.13.67",
        "38.247.12.92",
        "38.247.15.69",
        "38.247.11.87",
        "38.247.10.115",
        "38.247.14.74",
        "38.247.14.92",
        "38.247.10.78",
        "38.247.12.84",
        "38.247.12.93",
        "38.247.12.85",
        "38.247.13.76",
        "38.247.14.71",
        "38.247.11.115",
        "38.247.10.76",
        "38.247.10.92",
        "38.247.9.120",
        "38.247.11.79",
        "38.247.9.67",
        "38.247.11.84",
        "38.247.13.73",
        "38.247.11.118",
        "38.247.8.83",
        "38.247.11.112",
        "38.247.8.88",
        "38.247.15.74",
        "38.247.12.77",
        "38.247.9.112",
        "38.247.10.110",
        "38.247.9.78",
        "38.247.10.83",
        "38.247.10.80",
        "38.247.11.89",
        "38.247.9.90",
        "38.247.12.76",
        "38.247.10.69",
        "38.247.11.101",
        "38.247.9.121",
        "38.247.13.77",
        "38.247.11.76",
        "38.247.13.72",
        "38.247.15.86",
        "38.247.9.118",
        "38.247.9.102",
        "38.247.11.91",
        "38.247.8.71",
        "38.247.11.123",
        "38.247.9.110",
        "38.247.14.85",
        "38.247.9.91",
        "38.247.9.124"
    ]
    my = ['38.247.10.115', '38.247.9.103', '38.247.11.87', '38.247.15.69', '38.247.9.71', '38.247.14.89', '38.247.12.92', '38.247.13.67', '38.247.14.84', '38.247.14.83', '38.247.8.94', '38.247.9.89', '38.247.11.113', '38.247.11.90', '38.247.10.90', '38.247.11.99', '38.247.9.126', '38.247.9.86', '38.247.8.86', '38.247.8.73', '38.247.15.90', '38.247.8.82', '38.247.12.74', '38.247.9.80', '38.247.14.77', '38.247.15.85', '38.247.8.89', '38.247.12.72', '38.247.14.87', '38.247.12.78', '38.247.15.93', '38.247.13.84', '38.247.13.90', '38.247.8.114', '38.247.12.66', '38.247.10.106', '38.247.8.124', '38.247.11.88', '38.247.15.75', '38.247.14.81', '38.247.10.123', '38.247.9.116', '38.247.10.77', '38.247.10.105']


    if __name__ == "__main__":
        pass
        # ls = []
        # for val in ips:
        #     val = val.split(":")[0]
        #     if val in ip_list:
        #         ls.append(val)
        # print(ls)
        # print(len(ls))
        while True:
            try:
                # 检测钱包验证
                process_items_main()

                # 检测服务器运行
                process_items()
                # 写入 last_sub_id.txt 文件
                with open("last_sub_id.txt", "w") as file:
                    file.write(last_sub_id_map['last_sub_id'])
            finally:
                print('等待10分钟再次运行')
                time.sleep(60 * 10)
