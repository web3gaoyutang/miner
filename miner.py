import json

import requests
from prettytable import PrettyTable

miner_id = 0


class Miner:
    miner_id = 0
    user_url = "http://139.224.210.21:28089"
    bill_url = "http://139.224.210.21:28090"
    config_path = "config.json"

    def login(self):
        print("进行登录")

        username = input("请输入用户名: ")
        password = input("请输入密码: ")

        login_data = {
            "loginName": username,
            "password": password
        }

        url = self.user_url + "/api/login"
        response = requests.post(url, json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 200 and data["data"]["role"] == "miner":
                print(f'{data["data"]["nickName"]} login success, userId is {data["data"]["userId"]}')
                self.miner_id = data["data"]["userId"]
                self.update_config()
            else:
                print("登录失败")
        else:
            print("登录请求失败")

    def get_balance(self):
        if self.miner_id == 0:
            print("请先登录")
            return
        url = self.bill_url + "/api/balanceInfo?userId=" + str(self.miner_id)
        # url = "http://139.224.210.21:28090/api/balanceInfo?userId=28"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 200 and data["data"]["userId"] == self.miner_id:
                print(f'userId {data["data"]["userId"]} : balance is {data["data"]["balance"]}')

    def get_history(self):
        if self.miner_id == 0:
            print("请先登录")
            return
        url = self.bill_url + "/api/balanceHis?userId=" + str(self.miner_id)
        # url = "http://139.224.210.21:28090/api/balanceHis?userId=28"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 200 and data["data"] is not None:
                balance_his = data["data"]["balanceHis"]
                table = PrettyTable()
                table.field_names = ["ID", "Bill ID", "User ID", "Bill Value", "Before Balance", "Now Balance",
                                     "Create Time"]
                for item in balance_his:
                    table.add_row([
                        item["id"],
                        item["billId"],
                        item["userId"],
                        item["billValue"],
                        item["beforeBalance"],
                        item["nowBalance"],
                        item["createTime"]
                    ])

                print(table)
            else:
                print("历史记录为空")

    def logout(self):
        self.miner_id = 0
        print("退出登录")

    def update_config(self):
        with open(self.config_path, 'r') as file:
            data = json.load(file)
        data['miner_id'] = self.miner_id
        with open(self.config_path, 'w') as file:
            json.dump(data, file, indent=4)  # indent参数用于美化输出，非必需
        print("userId update")

    def update_addr(self):
        with open(self.config_path, 'r') as file:
            data = json.load(file)
        addr = input("请输入公网ip: ")
        port = input("请输入端口: ")
        data['executor_host'] = addr
        data['executor_port'] = int(port)
        with open(self.config_path, 'w') as file:
            json.dump(data, file, indent=4)  # indent参数用于美化输出，非必需
        print("addr update")


def main():
    miner = Miner()
    while True:
        print("==========================")
        print("请选择要执行的操作：")
        print("1. 执行登录操作")
        print("2. 查看当前余额")
        print("3. 查看余额明细")
        print("4. 退出登录")
        print("5. 修改公网ip和端口")
        print("q. 退出程序")
        print("==========================")

        choice = input("请输入选项: ")
        if choice == '1':
            miner.login()
        elif choice == '2':
            miner.get_balance()
        elif choice == '3':
            miner.get_history()
        elif choice == '4':
            miner.logout()
        elif choice == '5':
            miner.update_addr()
        elif choice.lower() == 'q':
            print("退出程序")
            break
        else:
            print("无效的选项，请重新输入")


if __name__ == "__main__":
    main()
