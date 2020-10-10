import sqlite3
from crypto import crypto_sys


class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect('files/accs.db')
        self.cur = self.conn.cursor()

        self.create_table()

    def execute_statement(self, statement):
        if not isinstance(statement, str):
            print('[ERROR] Pass the correct statement!')
            print(statement)
            return False

        try:
            self.cur.execute(statement)
            self.conn.commit()
            return True

        except Exception as e:
            print(repr(e))
            return False

    def create_table(self):
        statement = '''CREATE TABLE IF NOT EXISTS accounts (
                        account_name text,
                        account_pass text,
                        sda_check)'''

        self.execute_statement(statement)

    def add_account(self, name, passw, sda_check):
        cryp_pass = crypto_sys.encrypt_string(passw)
        cryp_pass = str(cryp_pass)[2:-1]
        statement = f'''INSERT INTO accounts (account_name, account_pass, sda_check) VALUES ('{name}', '{cryp_pass}',
                    '{sda_check}')'''

        self.execute_statement(statement)

    def fetch_account_pass(self, acc_name):
        print('DATABASE', acc_name)
        statement = f"""SELECT account_pass FROM accounts WHERE account_name='{acc_name}'"""
        data = self.cur.execute(statement).fetchall()[0]
        print('DATABASE', data)

        return data

    def fetch_account_sda(self, acc_name):
        print('DATABASE', acc_name)
        statement = f"""SELECT sda_check FROM accounts WHERE account_name='{acc_name}'"""
        data = self.cur.execute(statement).fetchall()[0]
        print('DATABASE', data)

        return data

    def fetch_data(self):
        statement = '''SELECT * FROM accounts'''
        data = self.cur.execute(statement).fetchall()

        return data

    def delete_account(self, account_name):
        statement = f"""DELETE FROM accounts WHERE account_name='{account_name}'"""
        self.execute_statement(statement)

        return True

    def update_account(self, account_name, account_pass):
        cryp_pass = crypto_sys.encrypt_string(account_pass)
        cryp_pass = str(cryp_pass)[2:-1]
        statement = f"""UPDATE accounts SET account_pass='{cryp_pass}' WHERE account_name='{account_name}'"""
        self.execute_statement(statement)

        return True


DB = DataBase()
print(DB.fetch_data())
