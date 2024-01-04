import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask_login import login_user

import app.config

from app import User
from app.auth.des_util import raw_str_enc
from app.auth.encrypt_util import Encryptor
from app.dao.user import UpdateInfo, UserManager

from app.service.message import MessageService


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login_url = app.config.CAS_URL
        self.message = MessageService()

    def _get_lt_execution_values(self):
        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.text, "html.parser")
        if 'id="lt"' in response.text:
            lt_value = soup.find("input", {"id": "lt"})["value"]
        else:
            lt_value = ''
        if 'name="execution"' in response.text:
            execution = soup.find("input", {"name": "execution"})["value"]
        else:
            execution = "e1s1"
        return lt_value, execution

    def login(self):
        username_verify = str(self.username)
        if len(username_verify) < 2:
            return self.message.send_error_message('请输入CUID/工号')
        if username_verify[:2].isdigit() and username_verify[:2] != '10':
            return self.message.send_error_message('请输入CUID/工号，而不是学号')
        if not self.password:
            return self.message.send_error_message('请输入密码')
        manager = UserManager(self.username)
        user = manager.get_user_info()
        encryptor = Encryptor()
        if user and encryptor.verify_password(self.password, user.password):
            if user.last_update > datetime.now() - timedelta(days=1):
                self.login_direct()
        lt_value, execution = self._get_lt_execution_values()
        data = {
            "rsa": raw_str_enc(username_verify + self.password + lt_value),
            "ul": len(username_verify),
            "pl": len(self.password),
            "lt": lt_value,
            "execution": execution,
            "_eventId": "submit",
        }
        post_headers = {
            "content-type": "application/x-www-form-urlencoded",
            "referer": self.login_url,
        }
        response = self.session.post(self.login_url, data=data, headers=post_headers)
        if "我的账户" not in response.text:
            return self.message.send_unauthorized_message('用户名或密码错误')
        else:
            return self.fetch_data()

    def fetch_data(self):
        url = app.config.EAM_STD_URL
        headers = {
            "accept": "text/html, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referrer": app.config.EAM_URL
        }
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cuid = self.username
            encryptor = Encryptor()
            password = encryptor.hash_password(self.password)
            uid = soup.find('td', class_='title', text='学号：').find_next('td').text.strip()
            name = soup.find('td', class_='title', text='姓名：').find_next('td').text.strip()
            if not uid:
                uid = soup.find('td', class_='title', text='工号：').find_next('td').text.strip()
                if not uid:
                    return self.message.send_error_message('校园网信息请求失败')
                upd_info = UpdateInfo(cuid, uid, name, password, "teacher", '', '')
                upd_info.update_user_info()
                login_user(User(cuid))
                return self.message.send_message('登录成功')
            department_name = soup.find('td', class_='title', text='院系：').find_next('td').text.strip()
            class_name = soup.find('td', class_='title', text='所属班级：').find_next('td').text.strip()
            upd_info = UpdateInfo(cuid, uid, name, password, "student", class_name, department_name)
            upd_info.update_user_info()
            login_user(User(cuid))
            return self.message.send_message('登录成功')
        else:
            return self.message.send_error_message('校园网信息请求失败')

    def login_direct(self):
        login_user(User(self.username))
        return self.message.send_message('登录成功')
