from settings import LOGGING
import json

class Account:
    """一个账号，包含cookie和proxy"""
    def __init__(self, cookie, proxy):
        self.cookie = cookie
        self.proxy = proxy  # proxy[0]为proxy_host， proxy[1]为proxy_port

    def __repr__(self):
        return "proxy: {}, cookie: {}".format(self.proxy, self.cookie)


class AccountPool:
    """账号池，管理cookie和ip"""
    def __init__(self, cookies, proxies):
        if not cookies or not proxies:
            raise ValueError
        if type(cookies) is not list or type(proxies) is not list:
            raise TypeError

        self.__cookies = cookies
        self.__proxies = proxies
        self.accounts = list()
        self.__count = 0
        self._compound_accounts()

    def __repr__(self):
        return '\n'.join(self.accounts)

    def _compound_accounts(self):
        """根据cookies和proxies合成所有Account对象"""
        cookies_len = len(self.__cookies)
        proxies_len = len(self.__proxies)
        max_len = max(cookies_len, proxies_len)

        self.accounts.clear()
        for i in range(max_len):
            account = Account(self.__cookies[i % cookies_len], self.__proxies[i % proxies_len])
            self.accounts.append(account)

    def update(self, new_cookies=None, new_proxies=None):
        """对信息进行更新"""

        # 检查new_cookies和new_proxies是否为list或None
        if not isinstance(new_cookies, list) and new_cookies is not None:
            raise ValueError
        if not isinstance(new_proxies, list) and new_proxies is not None:
            raise ValueError
        # 分别进行更新
        if new_cookies:  # 如果new_cookies不是None就进行更新
            self.__cookies = new_cookies
        if new_proxies:
            self.accounts = new_proxies
        # 将更新后的cookie和proxy进行配对复合成多个account
        self._compound_accounts()

    def update_one_cookie(self, seq_num, new_cookie):
        try:
            self.accounts[seq_num].cookie = new_cookie
        except IndexError:
            LOGGING.warning("update fail because seq_num {} over the max account number {}."
                            .format(seq_num, len(self.accounts)))

    def update_one_proxy(self, seq_num, new_proxy):
        try:
            self.accounts[seq_num].proxy = new_proxy
        except IndexError:
            LOGGING.warning("update fail because seq_num {} over the max account number {}."
                            .format(seq_num, len(self.accounts)))

    def delete_one_proxy(self, seq_num):
        try:
            del self.accounts[seq_num]
        except IndexError:
            LOGGING.warning("delete fail because seq_num {} over the max account number {}."
                            .format(seq_num, len(self.accounts)))

    def fetch(self):
        """获取一个账号的cookie和代理"""
        self.__count += 1
        self.__count = self.__count % len(self.accounts)
        account = self.accounts[self.__count]
        return account.cookie, account.proxy


with open(r'account/account.json') as json_file:
    account_json = json.load(json_file)

account_pool = AccountPool(account_json['cookies'], account_json['proxies'])