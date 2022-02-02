"""
对批量账号进行模拟登陆获取到cookie
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WeiboLogin():
    def __init__(self, username, password):
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        mobile_emulation = {"deviceMetrics": {"width": 1050, "height": 840, "pixelRatio": 3.0},
                            "userAgent": user_agent}
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        self.username = username
        self.password = password

    def login(self):
        """
        open login page and login
        :return: None
        """
        self.browser.get(self.url)
        wait = WebDriverWait(self.browser, 5)
        username = wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def run(self):
        try:
            self.login()
            WebDriverWait(self.browser, 20).until(
                EC.title_is('我的首页')
            )
            cookies = self.browser.get_cookies()
            cookie = [item["name"] + "=" + item["value"] for item in cookies]
            cookie_str = '; '.join(item for item in cookie)
            return cookie_str
        except Exception as e:
            print(e)
        finally:
            self.browser.quit()
        return None


if __name__ == '__main__':
    username = 'tnnmyvxj27431@sina.com'
    password = 'cxy633lil'
    cookie_str = None
    try:
        cookie_str = WeiboLogin(username, password).run()
        print('Cookie:', cookie_str)
    except Exception as e:
        print(e)