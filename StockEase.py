import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import bcrypt
import customtkinter
import pymysql
from datetime import datetime
import numpy as np
import traceback
import re

root = Tk()  # Janela principal (estoque)
root.geometry("720x640")
root.title("Sistema de Gerencimento de Estoque")

top = Toplevel()  # Janela secundária (login)
top.title("Login")
top.config(bg="#001220")
top.resizable(False, False)
top.overrideredirect(True)  # esconder barra de minimizar

font1 = ("Helvetica", 25, "bold")
font2 = ("Arial", 17, "bold")
font3 = ("Arial", 13, "bold")
font4 = ("Arial", 13, "bold", "underline")

""" 
# Função para centralizar a tela de login
def CenterWindowToDisplay(Screen: Toplevel, width: int, height: int):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 1.5))
    return f"{width}x{height}+{x}+{y}"


top.geometry(CenterWindowToDisplay(top, 450, 360))

def CenterWindowToDisplay(width: int, height: int):
    return lambda Screen: f"{width}x{height}+{(Screen.winfo_screenwidth() - width) // 2}+{(Screen.winfo_screenheight() - height) // 3}"
top.geometry(CenterWindowToDisplay(450, 360)(top))
"""
# Função para centralizar a tela de login, utilizando currying
center_window_display = lambda Screen: lambda width: lambda \
        height: f"{width}x{height}+{(Screen.winfo_screenwidth() - width) // 2}+" \
                f"{(Screen.winfo_screenheight() - height) // 3}"

top.geometry(center_window_display(top)(450)(360))

#Faz a conexão com o banco de dados
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        db='stockmanagementsystem'
    )
    return conn


conn = connection()
cursor = conn.cursor()


# Função que cadastra novo usuário
def singup():
    username = username_entry.get()
    password = password_entry.get()
    if username != "" and password != "":
        check_username_sql = "SELECT username FROM users WHERE username = %s"
        cursor.connection.ping()
        cursor.execute(check_username_sql, (username,))
        if cursor.fetchone() is not None:
            messagebox.showerror("Error", "Este nome de usuário já existe!")
        else:
            encoded_password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, hashed_password))
            conn.commit()
            messagebox.showinfo("", "Conta criada!")

    else:
        messagebox.showerror("Error", "Todos os campos são obrigatórios!")


# Função que faz a validação das credenciais do usuário
def login_account():
    username = username_entry2.get().strip()
    password = password_entry2.get().strip()
    if username and password:
        sql = "SELECT password, is_admin FROM users WHERE username = %s"
        cursor.connection.ping()
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result:
            stored_password, is_admin = result
            if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                if is_admin == 1:
                    generate_buttons(button_commands())
                    root.deiconify()
                    top.destroy()
                else:
                    generate_buttons(button_commands_normal_user())
                    root.deiconify()
                    top.destroy()
            else:
                messagebox.showerror("Error", "Senha Inválida!")
        else:
            messagebox.showerror("Error", "Usuário não encontrado!")
    else:
        messagebox.showerror("Error", "Todos os campos são obrigatórios!")


# Função que retorna para a tela de cadastro
def return_to_signup():
    frame2.destroy()


# Função que mostra a tela de login
def login():
    global frame2
    frame2 = customtkinter.CTkFrame(top, bg_color="#001220", fg_color="#001220", width=470, height=360)
    frame2.place(x=0, y=0)

    # Carrega a imagem usando PhotoImage
    image = PhotoImage(file="C:\\Users\\matheus.moura\\PycharmProjects\\AV3_stock\\image\\logo2.png")

    # Cria um widget Label para exibir a imagem
    image_label = Label(frame2, image=image, bg="#001220", anchor="center")
    image_label.image = image  # Mantém uma referência à imagem para evitar que seja coletada pelo garbage collector
    image_label.place(x=170, y=-15)

    login_label2 = customtkinter.CTkLabel(frame2, font=font1, text="Log in", text_color="#fff", bg_color="#001220")
    login_label2.place(x=220, y=90, anchor="center")

    global username_entry2
    global password_entry2

    username_entry2 = customtkinter.CTkEntry(frame2, font=font2, text_color="#fff",
                                             fg_color="#001a2e", bg_color="#121111", border_color="#004780",
                                            border_width=3, placeholder_text="Username",
                                             placeholder_text_color="#a3a3a3", width=200, height=5)
    username_entry2.place(x=120, y=120)

    password_entry2 = customtkinter.CTkEntry(frame2, font=font2, show="*", text_color="#fff",
                                             fg_color="#001a2e", bg_color="#004780", border_color="#004780",
                                             border_width=3, placeholder_text="Password",
                                             placeholder_text_color="#a3a3a3",
                                             width=200, height=5)
    password_entry2.place(x=120, y=165)

    login_button2 = customtkinter.CTkButton(frame2, font=font2, text_color="#fff", text="Conecte-se",
                                            fg_color="#00965d", hover_color="#006e44", bg_color="#121111",
                                            cursor="hand2",
                                            corner_radius=5, width=120,
                                            command=login_account)
    login_button2.place(x=220, y=220, anchor="center")

    return_to_signup_button = customtkinter.CTkButton(frame2, font=font4,
                                                      text_color="#00bf77",
                                                      text="Voltar para Cadastro",
                                                      fg_color="#001220", cursor="hand2", width=150,
                                                      command=return_to_signup)
    return_to_signup_button.place(x=235, y=250)

    close_button = customtkinter.CTkButton(frame2, text="X", command=close_app, fg_color="red", text_color="#fff",
                                           width=30, hover_color="#e61919", anchor="center")
    close_button.place(x=410, y=10)


image = PhotoImage(file="C:\\Users\\matheus.moura\\PycharmProjects\\AV3_stock\\image\\logo2.png")
image_label = Label(top, image=image, bg="#001220", anchor="center")
image_label.place(x=170, y=-15)

singnup_label = customtkinter.CTkLabel(top, font=font1, text="Sign Up", text_color="#fff", bg_color="#001220")
singnup_label.place(x=220, y=90, anchor="center")

username_entry = customtkinter.CTkEntry(top, font=font2, text_color="#fff", fg_color="#001a2e", bg_color="#121111",
                                        border_color="#004780", border_width=3,
                                        placeholder_text="Username", placeholder_text_color="#a3a3a3",
                                        width=200, height=5)
username_entry.place(x=120, y=120)

password_entry = customtkinter.CTkEntry(top, font=font2, show="*", text_color="#fff",
                                        fg_color="#001a2e", bg_color="#004780", border_color="#004780",
                                        border_width=3, placeholder_text="Password",
                                        placeholder_text_color="#a3a3a3",
                                        width=200, height=5)
password_entry.place(x=120, y=165)

singnup_button = customtkinter.CTkButton(top, font=font2, text_color="#fff", text="Registrar",
                                         fg_color="#00965d", hover_color="#006e44", bg_color="#121111", cursor="hand2",
                                         corner_radius=5, width=120, command=singup)

singnup_button.place(x=220, y=220, anchor="center")

login_label = customtkinter.CTkLabel(top, font=font3, text="Já tem uma conta?",
                                     text_color="#fff", bg_color="#001220")
login_label.place(x=230, y=250)

login_button = customtkinter.CTkButton(top, font=font4, command=login, text_color="#00bf77", text="Login",
                                       fg_color="#001220", cursor="hand2", width=40)
login_button.place(x=351, y=250)


def close_app():
    top.destroy()
    sys.exit()


close_button = customtkinter.CTkButton(top, text="X", command=close_app, fg_color="red", text_color="#fff",
                                       width=30, hover_color="#e61919", anchor="center")
close_button.place(x=410, y=10)

my_tree = ttk.Treeview(root, show='headings', height=20)
style = ttk.Style()

placeholderArray = ['', '', '', '', '']
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for i in range(0, 5):
    placeholderArray[i] = tkinter.StringVar()


def read():
    cursor.connection.ping()
    sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks ORDER BY `id` DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def read_where(column):
    cursor.connection.ping()
    sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `name` LIKE '%{column}%' "
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()


def setph(word, num):
    for ph in range(0, 5):
        if ph == num:
            placeholderArray[ph].set(word)


def generateRand():
    itemId = ''
    for i in range(0, 3):
        randno = random.randrange(0, (len(numeric) - 1))
        itemId = itemId + str(numeric[randno])
    randno = random.randrange(0, (len(alpha) - 1))
    itemId = itemId + '-' + str(alpha[randno])
    # print("generated: " + itemId)
    setph(itemId, 0)
    return itemId


capitalize_first_letter = lambda word: word[0].upper() + word[1:]


# utilização de functor map
def capitalize_words(sentence):
    return ' '.join(map(capitalize_first_letter, sentence.split()))


# Monad que verifica se número é valido
def maybe_bind(x, y, f):
    if x is None:
        return None
    else:
        return f(x, y)


def maybe(x, y):
    return lambda f: maybe_bind(x, y, f)


def is_valid_number(number):
    return bool(re.match('[+]?\d*\.?\d+$', number))


def show_warning_if_invalid(qnt, price):
    if (not is_valid_number(qnt)) or (not is_valid_number(price)):
        messagebox.showwarning("", "Somente números positivos são aceitos para a quantidade e preço!")


def save():
    name = str(nameEntry.get())
    price = priceEntry.get()
    qnt = qntEntry.get()
    cat = str(categoryCombo.get())
    valid = True
    if not (name and name.strip()) or not (price and price.strip()) or not (
            qnt and qnt.strip()) or not (cat and cat.strip()):
        messagebox.showwarning("", "Todos os campos são obrigatórios!")
        return
    itemId = generateRand()
    if len(itemId) < 5:
        messagebox.showwarning("", "Item ID inválido!")
        return
    if (not (itemId[3] == '-')):
        valid = False
    for i in range(0, 3):
        if (not (itemId[i] in numeric)):
            valid = False
            break
    if (not (itemId[4] in alpha)):
        valid = False
    """ 
    try:
        isinstance(int(qnt), (int, float))
        isinstance(float(price), (int, float))
    except ValueError:
        messagebox.showwarning("", "Somente números positivos são aceitos para a quantidade e preço!")
    """
    maybe(qnt, price)(lambda q, p: show_warning_if_invalid(qnt, price))
    if not (valid):
        messagebox.showwarning("", "Item ID inválido!")
        return

    try:
        cursor.connection.ping()
        sql = f"SELECT * FROM stocks WHERE `item_id` = '{itemId}' "
        cursor.execute(sql)
        checkItemNo = cursor.fetchall()
        if len(checkItemNo) > 0:
            messagebox.showwarning("", "Item Id already used")
            return
        else:
            if float(price) >= 0 and int(qnt) >= 0:
                cursor.connection.ping()
                sql = f"INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `category`) VALUES " \
                      f"('{itemId}','{capitalize_words(name)}','{price}','{qnt}','{cat}')"
            if int(qnt) > 1000 or float(price) > 1000000000:
                messagebox.showwarning("", "A quantidade não pode ser maior que 1000 e "
                                               "o preço não pode ser maior que 1 bilhão!")
                return
            cursor.execute(sql)
            nameEntry.focus_set()
        conn.commit()
        conn.close()
        for num in range(0, 5):
            setph('', (num))
    except Exception as e:
        # print(e)
        # messagebox.showwarning("", "Error while saving ref: " + str(e))
        return
    refreshTable()


def update():
    selectedItemId = ''
    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])

        name = str(nameEntry.get())
        price = priceEntry.get()
        qnt = qntEntry.get()
        cat = str(categoryCombo.get())

        maybe(qnt, price)(lambda q, p: show_warning_if_invalid(qnt, price))

        if not (name and name.strip()) or not (price and price.strip()) or not (
                qnt and qnt.strip()) or not (cat and cat.strip()):
            messagebox.showwarning("", "Todos os campos são obrigatórios!")
            return
        try:
            if float(price) >= 0 and int(qnt) >= 0:
                cursor.connection.ping()
                sql = f"UPDATE stocks SET `name` = '{name}', `price` = '{price}', `quantity` = '{qnt}', `category` = '{cat}' WHERE `item_id` = '{selectedItemId}' "
                cursor.execute(sql)
                nameEntry.focus_set()
                conn.commit()
                conn.close()
                for num in range(0, 5):
                    setph('', (num))
            if int(qnt) > 1000 or float(price) > 1000000000:
                messagebox.showwarning("", "A quantidade não pode ser maior que 1000 e "
                                           "o preço não pode ser maior que 1 bilhão!")
                return
        except Exception as err:
            #messagebox.showwarning("", "Error occured ref: " + str(err))
            return
        refreshTable()
    except:
        messagebox.showwarning("", "Selecione um registro!")


def delete():
    try:
        if (my_tree.selection()[0]):
            decision = messagebox.askquestion("", "Deseja deletar o registro selecionado?")
            if (decision != 'yes'):
                return
            else:
                selectedItem = my_tree.selection()[0]
                itemId = str(my_tree.item(selectedItem)['values'][0])
                try:
                    cursor.connection.ping()
                    sql = f"DELETE FROM stocks WHERE `item_id` = '{itemId}' "
                    cursor.execute(sql)
                    nameEntry.focus_set()
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("", "Registro deletado!")
                except:
                    messagebox.showinfo("", "Desculpe, um erro ocorreu.")
                refreshTable()
                clear()
    except:
        messagebox.showwarning("", "Selecione um registro!")


def select():
    try:
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        cat = str(my_tree.item(selectedItem)['values'][4])
        setph(itemId, 0)
        setph(name, 1)
        setph(price, 2)
        setph(qnt, 3)
        setph(cat, 4)
    except:
        messagebox.showwarning("", "Selecione um registro!")


def find():
    name = str(nameEntry.get())
    cursor.connection.ping()
    if (name and name.strip()):
        sql = f"SELECT `item_id`, `name`, `price`, `quantity`, `category`, `date` FROM stocks WHERE `name` LIKE '%{name}%' "
    else:
        messagebox.showwarning("", "Pesquise pelo nome do item!")
        return
    cursor.execute(sql)
    try:
        ls = []
        for data in my_tree.get_children():
            my_tree.delete(data)
        for array in read_where(name):
            ls.append(array)
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
        my_tree.tag_configure('orow', background="#EEEEEE")
        my_tree.pack()
        conn.commit()
        conn.close()
        if len(ls) == 0:
            raise Exception
    except:
        messagebox.showwarning("", "Não há registros!")


# Definindo a função de alta ordem
create_clear_function = lambda func, placeholder_func, refresh_func: lambda: func(placeholder_func, refresh_func)

# Usando a função de alta ordem
clear = create_clear_function(
    lambda placeholder_func, refresh_func: (
        lambda: (
            [placeholder_func('', num) for num in range(5)],
            refresh_func()
        )
    ),
    setph,
    refreshTable

)

#Usando Y combinator, para criar uma função recursiva a partir de uma função lambda
def calculate_total_price():
    try:
        cursor.connection.ping()
        cursor.execute("SELECT price, quantity FROM stocks ORDER BY date DESC")
        stocks = cursor.fetchall()
        prices_quantities = [(stock[0], stock[1]) for stock in stocks]

        # Usar Y combinator para calcular a soma dos preços considerando as quantidades
        Y = (lambda f: (lambda x: x(x))(lambda x: f(lambda v: x(x)(v))))
        sum_prices = Y(lambda f: lambda lst: 0 if not lst else (lst[0][0] * lst[0][1]) + f(lst[1:]))

        total_price = sum_prices(prices_quantities)
        messagebox.showinfo("", f"O preço total dos produtos é: R$ {total_price:.2f}.")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao calcular o preço total: {str(e)}")


# Dicionário no escopo de uma função lambda
button_commands = lambda: {
    "SALVAR": save,
    "ALTERAR": update,
    "DELETAR": delete,
    "SELECIONAR": select,
    "PROCURAR": find,
    "LIMPAR": clear(),
    "TOTAL": calculate_total_price
}

button_commands_normal_user = lambda: {
    "SALVAR": save,
    "ALTERAR": update,
    "SELECIONAR": select,
    "PROCURAR": find,
    "LIMPAR": clear(),
    "TOTAL": calculate_total_price
}

frame = tkinter.Frame(root, bg="#eeeeee")  # cor do background
frame.pack()

btnColor = "#08613f"

manageFrame = tkinter.LabelFrame(frame, text="Ações", borderwidth=5)
manageFrame.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])


def generate_buttons(dic):
    for i, (button_text, command) in enumerate(dic.items()):
        button = Button(manageFrame, text=button_text, width=10, borderwidth=3, bg=btnColor, fg='white',
                        command=command)
        button.grid(row=0, column=i, padx=5, pady=5)


entriesFrame = tkinter.LabelFrame(frame, text="Formulário", borderwidth=6)
entriesFrame.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=[0, 20], ipadx=[6])

nameLabel = Label(entriesFrame, text="NOME", anchor="e", width=10)
priceLabel = Label(entriesFrame, text="PREÇO", anchor="e", width=10)
qntLabel = Label(entriesFrame, text="QNT", anchor="e", width=10)
categoryLabel = Label(entriesFrame, text="CATEGORIA", anchor="e", width=10)

nameLabel.grid(row=1, column=0, padx=10)
priceLabel.grid(row=2, column=0, padx=10)
qntLabel.grid(row=3, column=0, padx=10)
categoryLabel.grid(row=4, column=0, padx=10)

#Utilização de List Comprehension
categoryArray = ['Periféricos', 'Ferramentas de reparo', 'Gadgets']
create_category_values = lambda categoryArray: [category for category in categoryArray]

nameEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[1])
priceEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[2])
qntEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[3])
categoryCombo = ttk.Combobox(entriesFrame,
                             width=47,
                             textvariable=placeholderArray[4],
                             values=create_category_values(categoryArray),
                             state="readonly")

nameEntry.grid(row=1, column=2, padx=5, pady=5)
priceEntry.grid(row=2, column=2, padx=5, pady=5)
qntEntry.grid(row=3, column=2, padx=5, pady=5)
categoryCombo.grid(row=4, column=2, padx=5, pady=5)

style.configure(root)
my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=125)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=150)
my_tree.heading("Item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Nome", anchor=W)
my_tree.heading("Price", text="Preço", anchor=W)
my_tree.heading("Quantity", text="Quantidade", anchor=W)
my_tree.heading("Category", text="Categoria", anchor=W)
my_tree.heading("Date", text="Data de inserção", anchor=W)
my_tree.tag_configure('orow', background="#EEEEEE")
my_tree.pack()

refreshTable()
root.resizable(False, False)
root.withdraw()
root.mainloop()
