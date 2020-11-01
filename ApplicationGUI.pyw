import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkinter import StringVar, BooleanVar
from tkinter import filedialog as fd

from database import DB
from crypto import crypto_sys
from settings import logger

from steam_connection import SteamAccount, CreateAccountConnection


f = open('files/sda_path.txt')
f.close()
f = open('files/steam_path.txt')
f.close()


class SteamConnectionGui(tk.Tk):

    def __init__(self):
        super().__init__()
        try:
            self.steam_path = open('files/steam_path.txt', 'r').read()
            if not self.steam_path:
                messagebox.showinfo('Неверный путь!', 'Укажите путь до steam.exe во вкладке настройки!')
                logger.debug('Empty path to steam.exe!')
        except FileNotFoundError:
            self.steam_path = None

        try:
            self.sda_path = open('files/sda_path.txt', 'r').read()
            if not self.sda_path:
                messagebox.showinfo('Неверный путь!', 'Укажите путь до SDA во вкладке настройки!')
                logger.debug('Empty path to SDA!')
        except FileNotFoundError:
            self.sda_path = None

        self.geometry('250x250+600+300')
        self.resizable(False, False)
        self.title("Steam Authorized")
        self.protocol("WM_DELETE_WINDOW", self.close_system)
        self.bind('<Escape>', lambda e: self.destroy())
        self.new_window = None

        self.powered_label = ttk.Label(self, text="Powered by matsubus", font=('Consolas', 8, 'bold'))
        self.choose_label = ttk.Label(self, text="Choose Account", font=('Bahnschrift', 10, 'bold'))
        self.entry_button = ttk.Button(self, text="Enter Account",
                                       command=self.run_steam_connection)
        self.add_account_button = ttk.Button(self, text="Add Account",
                                             command=self.create_new_window)
        self.configure_button = ttk.Button(self, text="Configure Account",
                                           command=self.configure_accouns_window)

        self.combobox = ttk.Combobox(self, values=self.fetch_account_names(), state='readonly')

        if self.fetch_account_names():
            self.combobox.current(0)

    def draw_widgets(self):
        self.choose_label.place(relx=0.31, rely=0.2)
        self.powered_label.place(relx=0.03, rely=0.93)
        self.combobox.place(relx=0.22, rely=0.35)

        self.entry_button.place(relx=0.30, rely=0.55)
        self.add_account_button.place(relx=0.07, rely=0.7)
        self.configure_button.place(relx=0.5, rely=0.7)

    def draw_menu(self):
        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Выйти', command=self.close_system)
        menu_bar.add_cascade(label='File', menu=file_menu)

        func_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Functions", menu=func_menu)

        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=edit_menu)
        edit_menu.add_command(label="Path to Steam", command=self.get_steam_path)
        edit_menu.add_command(label="Path to SDA", command=self.get_sda_path)

        self.configure(menu=menu_bar)

    def get_steam_path(self):
        filedialog = fd.askopenfilename()
        if filedialog:
            self.steam_path = str(filedialog)
            print(self.steam_path)
            with open('files/steam_path.txt', 'w') as file:
                file.write(r''.join(self.steam_path))

    def get_sda_path(self):
        filedialog = fd.askopenfilename()
        if filedialog:
            self.sda_path = str(filedialog)
            with open('files/sda_path.txt', 'w') as file:
                file.write(r''.join(self.sda_path))

    def create_new_window(self):
        self.new_window = NewAccountWindow(self)

    def get_data_from_child(self):
        account_name = self.new_window.name_entry.get()
        account_password = self.new_window.password_entry.get()
        sda_checkbox = self.new_window.SDA_var.get()
        print(sda_checkbox)
        self.new_window.destroy()

        DB.add_account(account_name, account_password, sda_checkbox)

        self.reload_combobox()

    @staticmethod
    def fetch_account_names():
        data = DB.fetch_data()
        data = [str(i[0]) for i in data]

        return data

    def run_steam_connection(self):
        password = self.get_password()
        sda = self.get_sda()
        steam_acc = SteamAccount(self.combobox.get(), password, sda)
        st_connection = CreateAccountConnection(self.steam_path, self.sda_path, steam_account=steam_acc)
        st_connection.start()

    def configure_accouns_window(self):
        self.new_window = ConfigureAccountsWindow(self, self.combobox.get())

    def get_password(self):
        print('GUI', self.combobox.get())
        acc_name = self.combobox.get()
        password_data = DB.fetch_account_pass(acc_name)
        password = crypto_sys.decrypt_string(password_data)

        return password

    def get_sda(self):
        sda_data = DB.fetch_account_sda(self.combobox.get())
        sda_data = False if sda_data[0] == 'False' else True
        print('GUI', sda_data)

        return sda_data

    def reload_combobox(self, name=None):
        if name:
            self.combobox.insert(-1, name)
            self.combobox.current(0)
            self.draw_widgets()
        else:
            [self.combobox.delete(i) for i in self.combobox.winfo_children()]
            self.combobox = ttk.Combobox(self, values=self.fetch_account_names(), state='readonly')
            self.draw_widgets()

    def close_system(self):
        self.destroy()

    def run(self):
        self.draw_widgets()
        self.draw_menu()
        self.mainloop()


class NewAccountWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.geometry('230x120+600+300')
        self.resizable(False, False)
        self.SDA_var = BooleanVar()
        self.SDA_var.set(0)

        self.name_entry = ttk.Entry(self, width=20)
        self.password_entry = ttk.Entry(self, width=20, show="*")
        self.btn = ttk.Button(self, text="Add Account",
                              command=self.master.get_data_from_child)
        self.name_label = ttk.Label(self, text="Login")
        self.password_label = ttk.Label(self, text="Password")
        self.j_label = ttk.Label(self, text="Enter Data:", font=('Bahnschrift', 10, 'bold'))
        self.message_box = messagebox.showinfo("Info", "Your data is encrypted!!")
        self.sda_checkbox = ttk.Checkbutton(self, text="SDA", variable=self.SDA_var, onvalue=1, offvalue=0)
        self.grab_set()
        self.focus()

        self.draw_widgets()

    def draw_widgets(self):
        self.j_label.grid(column=1, row=0)
        self.name_label.grid(column=0, row=1, padx=2, pady=2)
        self.password_label.grid(column=0, row=2, padx=2, pady=2)
        self.name_entry.grid(column=1, row=1, padx=2, pady=2)
        self.password_entry.grid(column=1, row=2, padx=5, pady=2)
        self.btn.grid(column=1, row=3, sticky='NSEW', padx=3, pady=3)
        self.sda_checkbox.grid(column=0, row=3, padx=3, pady=3)


class ConfigureAccountsWindow(tk.Toplevel):
    counter = False
    # class_examples = 0
    #
    # def __new__(cls, *dt, **mp):  # класса Singleton.
    #     if cls.class_examples == 0:  # Если он еще не создан, то
    #         cls.obj = object.__new__(cls)  # вызовем __new__ родительского класса
    #         cls.class_examples += 1
    #         return cls.obj
    #     else:
    #         return

    def __init__(self, master, account):
        super().__init__(master)
        self.master = master
        self.account_name = account

        if ConfigureAccountsWindow.counter:
            return
        else:
            ConfigureAccountsWindow.counter = True

        self.bind('<Escape>', lambda e: self.destroy())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.geometry('250x120+600+300')
        self.resizable(False, False)
        self.title("Change Window")
        self.str_var = StringVar(self, self.account_name)

        self.account_label = ttk.Label(self, text="Login")
        self.password_label = ttk.Label(self, text="Password")
        self.account_entry = ttk.Entry(self, state='disable', textvariable=self.str_var)
        self.password_entry = ttk.Entry(self, show='*')
        self.delete_button = ttk.Button(self, text="Delete Account", command=self.delete_account)
        self.accept_changes = ttk.Button(self, text="Accept Changes", command=self.accept_changes)

        self.draw_widgets()

    def draw_widgets(self):
        self.account_label.grid(column=0, row=0, padx=5, pady=5, ipadx=2, ipady=2)
        self.password_label.grid(column=0, row=1, padx=5, pady=5, ipadx=2, ipady=2)
        self.account_entry.grid(column=1, row=0, padx=5, pady=5, ipadx=2, ipady=2)
        self.password_entry.grid(column=1, row=1, padx=5, pady=5, ipadx=2, ipady=2)
        self.delete_button.grid(column=0, row=2, padx=5, pady=5, ipadx=2, ipady=2)
        self.accept_changes.grid(column=1, row=2, padx=5, pady=5, ipadx=2, ipady=2)

    def delete_account(self):
        DB.delete_account(self.account_name)
        self.master.reload_combobox()
        messagebox.showinfo("Successfull!", "Account successfully deleted!")

    def accept_changes(self):
        passw = self.password_entry.get()
        if len(passw) >= 3:
            DB.update_account(self.account_name, passw)
            messagebox.showinfo("Successfull!", "Changes successfully accepted!")
            self.destroy()
        else:
            messagebox.showerror("Error!", "Check your data!")
            self.grab_set()
            self.focus()

    def on_closing(self):
        ConfigureAccountsWindow.counter = False
        self.destroy()


App = SteamConnectionGui()
App.run()
