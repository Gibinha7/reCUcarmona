import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


def conectar():
    conn = mysql.connector.connect(
        host='localhost',        
        user='root',   
        password='',   
        database='cidades2'    
    )
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cidades (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        estado VARCHAR(255) NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Inserir, editar, excluir e consultar cidades
def inserir_cidade(nome, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cidades (nome, estado) VALUES (%s, %s)', (nome, estado))
    conn.commit()
    conn.close()

def editar_cidade(id, novo_nome, novo_estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE cidades SET nome = %s, estado = %s WHERE id = %s', (novo_nome, novo_estado, int(id)))
    conn.commit()
    conn.close()

def excluir_cidade(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cidades WHERE id = %s', (int(id),))
    conn.commit()
    conn.close()

def consultar_cidades():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cidades')
    cidades = cursor.fetchall()
    conn.close()
    return cidades

def consultar_cidade_por_id(cidade_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cidades WHERE id = %s', (cidade_id,))
    cidade = cursor.fetchone()
    conn.close()
    return cidade

# Funções para a Interface Gráfica
def adicionar_cidade():
    nome = nome_entry.get()
    estado = estado_entry.get()
    if nome and estado:
        inserir_cidade(nome, estado)
        messagebox.showinfo("Sucesso", "Cidade adicionada com sucesso!")
        limpar_campos()
        atualizar_lista()
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

def buscar_cidade_por_id():
    cidade_id = buscar_id_entry.get()
    if cidade_id:
        cidade = consultar_cidade_por_id(cidade_id)
        if cidade:
            nome_entry.delete(0, tk.END)
            nome_entry.insert(tk.END, cidade[1])
            estado_entry.delete(0, tk.END)
            estado_entry.insert(tk.END, cidade[2])
            id_label.config(text=f"ID Selecionado: {cidade[0]}")
        else:
            messagebox.showwarning("Erro", "Cidade não encontrada!")
    else:
        messagebox.showwarning("Erro", "Informe o ID para buscar.")

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    cidades = consultar_cidades()
    for cidade in cidades:
        tree.insert('', tk.END, values=(cidade[0], cidade[1], cidade[2]))

def editar_cidade_selecionada():
    cidade_id = id_label.cget("text").split(":")[1].strip()
    if cidade_id != "Nenhum":
        novo_nome = nome_entry.get()
        novo_estado = estado_entry.get()
        if novo_nome and novo_estado:
            editar_cidade(cidade_id, novo_nome, novo_estado)
            messagebox.showinfo("Sucesso", "Cidade editada com sucesso!")
            atualizar_lista()
            limpar_campos()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
    else:
        messagebox.showwarning("Erro", "Selecione uma cidade para editar.")

def excluir_cidade_selecionada():
    cidade_id = id_label.cget("text").split(":")[1].strip()
    if cidade_id != "Nenhum":
        excluir_cidade(cidade_id)
        messagebox.showinfo("Sucesso", "Cidade excluída com sucesso!")
        atualizar_lista()
        limpar_campos()
    else:
        messagebox.showwarning("Erro", "Selecione uma cidade para excluir.")

def selecionar_cidade_na_tabela(event):
    try:
        item_selecionado = tree.selection()[0]
        valores = tree.item(item_selecionado, 'values')
        cidade_id, nome, estado = valores[0], valores[1], valores[2]

        nome_entry.delete(0, tk.END)
        nome_entry.insert(tk.END, nome)
        estado_entry.delete(0, tk.END)
        estado_entry.insert(tk.END, estado)
        id_label.config(text=f"ID Selecionado: {cidade_id}")
    except IndexError:
        pass

def limpar_campos():
    nome_entry.delete(0, tk.END)
    estado_entry.delete(0, tk.END)
    buscar_id_entry.delete(0, tk.END)
    id_label.config(text="ID Selecionado: Nenhum")

def centralizar_janela(root):
    root.update_idletasks()
    largura_janela = root.winfo_width()
    altura_janela = root.winfo_height()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    root.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

# Interface Gráfica
root = tk.Tk()
root.title("Cadastro de Cidades")
root.geometry("500x600")
root.minsize(500, 600)

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Campos de entrada e labels
ttk.Label(main_frame, text="Nome da Cidade:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
nome_entry = ttk.Entry(main_frame)
nome_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(main_frame, text="Estado:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
estado_entry = ttk.Entry(main_frame)
estado_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(main_frame, text="Buscar Cidade por ID:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
buscar_id_entry = ttk.Entry(main_frame)
buscar_id_entry.grid(row=2, column=1, padx=10, pady=10)

ttk.Button(main_frame, text="Buscar Cidade", command=buscar_cidade_por_id).grid(row=3, column=0, columnspan=2, padx=10, pady=5)

id_label = ttk.Label(main_frame, text="ID Selecionado: Nenhum")
id_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

ttk.Button(main_frame, text="Adicionar Cidade", command=adicionar_cidade).grid(row=5, column=0, columnspan=2, padx=10, pady=5)
ttk.Button(main_frame, text="Editar Cidade", command=editar_cidade_selecionada).grid(row=6, column=0, columnspan=2, padx=10, pady=5)
ttk.Button(main_frame, text="Excluir Cidade", command=excluir_cidade_selecionada).grid(row=7, column=0, columnspan=2, padx=10, pady=5)

tree = ttk.Treeview(main_frame, columns=('ID', 'Nome', 'Estado'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Estado', text='Estado')
tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

tree.bind('<<TreeviewSelect>>', selecionar_cidade_na_tabela)

# Inicializar banco de dados e carregar a lista de cidades
criar_tabela()
atualizar_lista()

# Centralizar a janela
centralizar_janela(root)

# Executar a interface gráfica
root.mainloop()
