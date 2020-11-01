import pywinauto
import pywinauto.keyboard as keyboard
import pywinauto.clipboard as clipboard
import time
from settings import logger


class SteamAccount:

    def __init__(self, account_name: str, account_pass, check_box):
        self.account_name = account_name
        self.account_pass = account_pass
        print('CHECKBOX', check_box)
        self.check_box = True if check_box else False


class CreateAccountConnection:

    def __init__(self, steam_path, sda_path, steam_account: SteamAccount):
        self.steam_account = steam_account

        if self.steam_account.check_box and sda_path:
            try:
                self.app_sda = pywinauto.Application(backend="win32").connect(path=sda_path)
            except pywinauto.application.ProcessNotFoundError:
                self.app_sda = pywinauto.Application(backend="win32").start(sda_path)

        try:
            app = pywinauto.Application(backend='win32').connect(path=steam_path)
            app.kill()
        except pywinauto.application.ProcessNotFoundError:
            pass
            # args = [st_path, "-login", self.steam_account.account_name, self.steam_account.account_pass]
            # subprocess.call(args)

        path_with_args = steam_path + f' -login {steam_account.account_name} {steam_account.account_pass}'
        try:
            self.app = pywinauto.Application(backend="win32").start(path_with_args)
        except pywinauto.application.AppStartError:
            logger.debug('Отсутствует путь до steam.exe')

    def pull_out_sda_code(self):
        sda_control = self.app_sda['Steam Desktop Authenticator']
        sda_control.set_focus()
        sda_control['ListBox'].click()
        items = sda_control['ListBox'].item_texts()

        for i, item in enumerate(items):
            if item == self.steam_account.account_name:
                sda_control.set_focus()
                sda_control['ListBox'].select(i)
                sda_control['Copy'].click()
                code = clipboard.GetData()
                print('ST_CONN CODE', code)
                self.exec_steam_code(code)
                break

    def exec_steam_code(self, code):
        # try:
        #     self.app['Вход в Steam'].set_focus()
        # except pywinauto.findbestmatch.MatchError:
        #     time.sleep(2)
        print('STEAM_CONNECTION', code)
        if self.app['SteamBootstrapUpdateUIClass']:
            time.sleep(2)
        while not self.app['Steam Guard — Необходима авторизация компьютера']:
            time.sleep(2)
        self.app['Steam Guard — Необходима авторизация компьютера'].set_focus()
        keyboard.send_keys(f'{code}')

    def start(self):
        if self.steam_account.check_box:
            self.pull_out_sda_code()
