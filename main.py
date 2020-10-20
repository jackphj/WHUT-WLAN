# coding:utf-8
import logging
import requests
import base64
import re
REQUEST_URL = "http://172.30.16.34/include/auth_action.php"
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s ====> %(message)s')


def login_request(username, password):
    # rawPassword = password
    if not is_net_ok():
        logging.info("your computer is offline ， request now... ")
        password = "{B}"+base64.b64encode(password.encode()).decode()  # 加密
        ac_id = getAcId()
        data = {"action": "login",
                "username": username,
                "password": password,
                "ac_id": ac_id,
                "save_me": 1,
                "ajax": 1}
        try:
            response = requests.post(REQUEST_URL, data=data)
            response.encoding = response.apparent_encoding
            if "login_ok" in response.text:
                logging.info("login successfully")
            else:
                logging.error("login failed")
        except:
            logging.exception("requsest error")
    else:
        logging.info("your computer is online  ")


def is_net_ok() -> bool:
    try:
        status = requests.get("https://www.baidu.com").status_code
        if status == 200:
            return True
        else:
            return False
    except Exception:
        return False


# 获取ac_id
def getAcId() -> int:
    response = requests.get('http://hao123.com')
    url = re.findall(
        r"<meta http-equiv='refresh' content='1; url=(.*?)'>", response.text, re.S)[0]
    url = requests.get(url).url
    url = url.replace('index_1.html', 'srun_portal_pc.php')
    response = requests.get(url)
    ac_id_str = re.findall(
        r'<input type="hidden" name="ac_id" value="(.*?)">', response.text, re.S)[0]
    ac_id = int(ac_id_str)
    return ac_id


# password必须为编码之前的密码
def logout(username, password):
    postData = {"action": "logout",
                "username": username,
                "password": password,
                "ajax": 1}
    response = requests.post(REQUEST_URL, data=postData)
    response.encoding = response.apparent_encoding
    logging.info(response.text)


if __name__ == "__main__":
    login_request("", "")
    #logout("", "")