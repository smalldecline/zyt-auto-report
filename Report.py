import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By


def report(username, password):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')  # 无界面
    option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
    option.add_argument('--disable-gpu')

    # 创建浏览器对象
    driver = webdriver.Chrome(options=option)
    # 设置隐式等待
    driver.implicitly_wait(2)

    driver.get('http://zyt.zjnu.edu.cn/H5/Login.aspx?op=phone_html5')

    driver.find_element(By.ID, 'UserText').send_keys(username)
    driver.find_element(By.NAME, 'PasswordText').send_keys(password)
    driver.find_element(By.ID, 'btn_Login').click()
    driver.find_element(By.CSS_SELECTOR, 'li:nth-child(2)').click()

    report = driver.find_element(By.CSS_SELECTOR, '#submit')

    # if element is not visible ,exit
    if not report.is_displayed():
        info = "学号 %s 已完成打卡" % username
        logging.info(info)
        driver.quit()
        return

    report.click()
    driver.get("http://zyt.zjnu.edu.cn/H5/ZJSFDX/FillIn.aspx?address=%E6%B5%99%E6%B1%9F%E7%9C%81%E2%9C%B0%E9%87%91%E5%8D%8E%E5%B8%82%E2%9C%B0%E5%A9%BA%E5%9F%8E%E5%8C%BA")

    driver.find_element(By.ID, 'DATA_5_1').click()
    driver.find_element(By.ID, 'DATA_13_1').click()
    driver.find_element(By.ID, 'DATA_15').click()
    driver.find_element(By.ID, 'btn_save').click()

    # DATA_8_1 是第二针
    # DATA_9_6 加强针

    info = '学号 %s 打卡成功' % (username)
    logging.info(info)

    driver.quit()
    return


def check_now(username, password):

    info = "为学号 %s 进行打卡检查" % username
    logging.info(msg=info)

    report(username, password)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        )


    # # loop check every two hour
    while True:
        # get account list from accounts.json
        try:
            with open('./config/accounts.json', 'r') as f:
                account_list = json.load(f)
        except Exception as e:
            logging.error('accouts.json 文件不存在')

        # for each account, check now
        for account in account_list:
            check_now(account['username'], account['password'])
        logging.info("所有账号检查完成,休眠2小时")
        time.sleep(7200)


if __name__ == '__main__':
    main()
