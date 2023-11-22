from tkinter import *
import sqlite3
import secrets
import string

#CORES DO TKINTER
cor_bg = 'white'
cor_botao = '#31a0e0'
cor_fonte = '#180F4A'
cor_entrada = '#BCE3F3'
cor_success = '#19087C'
cor_danger = '#8E0324'



#CONEXÃO AO BANCO DE DADOS
conexao = sqlite3.connect("senhas.db")
cursor = conexao.cursor()

#CRIAÇÃO DE UMA TABELA DO BANCO
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_aplicativo TEXT NOT NULL,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
''')

#EXECUÇÃO DO COMANDO PARA CRIAR
conexao.commit()

#FECHAR A CONEXÃO COM O BANCO
conexao.close()

#Crud - COMANDO CREATE
#CRIANDO A JANELA DE CADASTRO
def abrir_janela_cadastrar():
    janela_cadastrar = Toplevel()
    janela_cadastrar.geometry('400x400')
    janela_cadastrar.title('Cadastrar senha')
    janela_cadastrar.configure(background=f'{cor_bg}')

    #EXECUÇÃO DA FUNÇÃO PARA CADASTRAR A SENHA
    def cadastrar_senha():
        try:
            site_aplicativo = entrada_site_aplicativo.get()
            usuario = entrada_usuario.get()
            senha = entrada_senha.get()
            conexao = sqlite3.connect("senhas.db")
            cursor = conexao.cursor()
            cursor.execute(f"SELECT * FROM login WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}'")
            buscar_cadastro = cursor.fetchone()
            if buscar_cadastro:
                resultado.config(text="O usuário já existe no banco de dados.", fg=f'{cor_danger}', font=('Bold', 12))
            elif site_aplicativo == "" or usuario == "" or senha == "":
                resultado.config(text="Por favor, preencha todos os campos!",  fg=f'{cor_danger}', font=('Bold', 12))
            else:
                cursor.execute(f"INSERT INTO login (site_aplicativo, usuario, senha) VALUES ('{site_aplicativo}','{usuario}', '{senha}')")
                conexao.commit()
                conexao.close()
                resultado.config(text="Cadastro inserido com sucesso", fg=f'{cor_success}', font=('Bold', 12))
        except sqlite3.IntegrityError:
            resultado.config(text="Erro ao acessar o banco de dados.", fg=f'{cor_danger}', font=('Bold', 12))

    #ESPAÇO VAZIO PARA ORGANIZAR A JANELA
    Label(janela_cadastrar, bg=f'{cor_bg}').pack(pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_cadastrar, text='Site / Aplicativo', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_site_aplicativo = Entry(janela_cadastrar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_site_aplicativo.pack(padx=10, pady=5)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_cadastrar, text='Usuário', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_usuario = Entry(janela_cadastrar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_usuario.pack(padx=10, pady=5)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_cadastrar, text='Senha', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_senha = Entry(janela_cadastrar, width =50, show='*', bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_senha.pack(padx=10, pady=5)

    #EXECUTAR O BOTAO PARA CADASTRAR
    Button(janela_cadastrar, text='Cadastrar Senha', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=cadastrar_senha).pack(padx=10, pady=10)

    #EXIBIR O RESULTADO DA ALTERAÇÃO DO TEXTO DE FORMA DINÂMICA
    resultado = Label(janela_cadastrar, text='', bg=f'{cor_bg}')
    resultado.pack(padx=10, pady=5)

    #BOTAO PARA VOLTAR A JANELA ANTERIOR
    Button(janela_cadastrar, text='Voltar', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=janela_cadastrar.destroy).pack(padx=10, pady=5)

#cRud - COMANDO READ
#CRIANDO A JANELA PARA VERIFICAR A SENHA
def abrir_janela_verificar():
    janela_verificar = Toplevel()
    janela_verificar.geometry('400x400')
    janela_verificar.title('Verificar senha')
    janela_verificar.configure(background=f'{cor_bg}')

    #EXECUÇÃO DA FUNÇÃO PARA VERIFICAR A SENHA
    def verificar_senha():
        site_aplicativo = entrada_site_aplicativo.get()
        usuario = entrada_usuario.get()
        conexao = sqlite3.connect("senhas.db")
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM login WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}'")
        verificar_resultado = cursor.fetchone()
        if verificar_resultado:
            senha = verificar_resultado[3]
            resultado.config(text=f"A seguinte senha: '{senha}', foi encontrada para o usuário '{usuario}'")
        else:
            resultado.config(text=f"Nenhuma senha foi encontrada para as seguintes credenciais: {site_aplicativo} e {usuario}")
            conexao.close()
    
    #ESPAÇO VAZIO PARA ORGANIZAR A JANELA
    Label(janela_verificar, bg=f'{cor_bg}').pack(pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_verificar, text='Site / Aplicativo', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_site_aplicativo = Entry(janela_verificar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_site_aplicativo.pack(padx=10, pady=5)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_verificar, text='Usuário', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_usuario = Entry(janela_verificar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_usuario.pack(padx=10, pady=5)

    #ESPAÇO VAZIO PARA ORGANIZAR A JANELA
    Label(janela_verificar, bg=f'{cor_bg}').pack(pady=3)

    #EXECUTAR O BOTAO PARA VERIFICAR
    Button(janela_verificar, text='Verificar Senha', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=verificar_senha).pack(padx=10, pady=10)

    #EXIBIR O RESULTADO DA ALTERAÇÃO DO TEXTO DE FORMA DINÂMICA
    resultado = Label(janela_verificar, text='', bg=f'{cor_bg}')
    resultado.pack(padx=10, pady=5)

    #BOTAO PARA VOLTAR A JANELA ANTERIOR
    Button(janela_verificar, text='Voltar', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=janela_verificar.destroy).pack(padx=10, pady=5)
    

#crUd - COMANDO UPDATE
#CRIANDO A JANELA PARA MODIFICAR A SENHA
def abrir_janela_modificar():
    janela_modificar = Toplevel()
    janela_modificar.geometry('400x400')
    janela_modificar.title('Modificar senha')
    janela_modificar.configure(background=f'{cor_bg}')

    #EXECUÇÃO DA FUNÇÃO PARA MODIFICAR A SENHA DE FORMA DINÂMICA
    def modificar_senha():
        try:
            site_aplicativo = entrada_site_aplicativo.get()
            usuario = entrada_usuario.get()
            senha = entrada_senha.get()
            nova_senha = entrada_nova_senha.get()
            conexao = sqlite3.connect("senhas.db")
            cursor = conexao.cursor()
            cursor.execute(f"SELECT * FROM login WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}' AND senha='{senha}'")
            modificar_senha = cursor.fetchone()
            if modificar_senha and senha != nova_senha:
                cursor.execute(f"UPDATE login SET senha='{nova_senha}' WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}' AND senha='{senha}'")
                conexao.commit()
                conexao.close()
                resultado.config(text=f"A senha foi alterada com sucesso!", fg=f'{cor_success}', font=('Bold', 12))
            else:
                resultado.config(text="Não foi possível alterar a senha!\nVerifique os dados informados.", fg=f'{cor_danger}', font=('Bold', 12))
        except sqlite3.IntegrityError:
            resultado.config(text="Erro ao acessar o banco de dados.", fg=f'{cor_danger}', font=('Bold', 12))

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_modificar, text='Site / Aplicativo', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_site_aplicativo = Entry(janela_modificar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_site_aplicativo.pack(padx=10, pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_modificar, text='Usuário', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_usuario = Entry(janela_modificar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_usuario.pack(padx=10, pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_modificar, text='Senha', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_senha = Entry(janela_modificar, width =50, show='*', bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_senha.pack(padx=10, pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_modificar, text='Nova Senha', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_nova_senha = Entry(janela_modificar, width =50, show='*', bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_nova_senha.pack(padx=10, pady=3)

    #EXECUTAR O BOTAO PARA MODIFICAR
    Button(janela_modificar, text='Modificar Senha', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=modificar_senha).pack(padx=10, pady=5)

    #EXIBIR O RESULTADO DA ALTERAÇÃO DO TEXTO DE FORMA DINÂMICA
    resultado = Label(janela_modificar, text='', bg=f'{cor_bg}')
    resultado.pack(padx=10, pady=3)

    #BOTAO PARA VOLTAR A JANELA ANTERIOR
    Button(janela_modificar, text='Voltar', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=janela_modificar.destroy).pack(padx=10, pady=3)

#cruD - COMANDO DELETE
#CRIANDO A JANELA PARA APAGAR A SENHA
def abrir_janela_apagar():
    janela_apagar = Toplevel()
    janela_apagar.geometry('400x400')
    janela_apagar.title('Apagar senha')
    janela_apagar.configure(background=f'{cor_bg}')

    #EXECUÇÃO DA FUNÇÃO PARA APAGAR A SENHA DE FORMA DINÂMICA
    def apagar_senha():
        try:
            conexao = sqlite3.connect("senhas.db")
            cursor = conexao.cursor()
            site_aplicativo = entrada_site_aplicativo.get()
            usuario = entrada_usuario.get()
            senha = entrada_senha.get()
            cursor.execute(f"SELECT * FROM login WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}' AND senha='{senha}'")
            apagar_senha = cursor.fetchone()    
            if apagar_senha:
                cursor.execute(f"DELETE FROM login WHERE site_aplicativo='{site_aplicativo}' AND usuario='{usuario}' AND senha='{senha}'")
                conexao.commit()
                conexao.close()
                resultado.config(text=f"A senha foi deletada com sucesso.", fg=f'{cor_success}', font=('Bold', 12))
            else:
                resultado.config(text=f"Erro ao apagar a senha!\nVerifique os dados novamente.", fg=f'{cor_danger}', font=('Bold', 12))
        except sqlite3.IntegrityError:
            resultado.config(text=f"Erro ao acessar o banco de dados.", fg=f'{cor_danger}', font=('Bold', 12))

    #ESPAÇO VAZIO PARA ORGANIZAR A JANELA
    Label(janela_apagar, bg=f'{cor_bg}').pack(pady=3)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_apagar, text='Site / Aplicativo', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_site_aplicativo = Entry(janela_apagar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_site_aplicativo.pack(padx=10, pady=5)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_apagar, text='Usuário', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_usuario = Entry(janela_apagar, width =50, bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_usuario.pack(padx=10, pady=5)

    #VISUALIZAÇÃO DOS PARÂMETROS/ENTRADA DE DADOS
    Label(janela_apagar, text='Senha', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12)).pack(padx=10, pady=5)
    entrada_senha = Entry(janela_apagar, width =50, show='*', bg=f'{cor_entrada}', fg=f'{cor_fonte}', font=('Bold', 14))
    entrada_senha.pack(padx=10, pady=5)

    #EXECUTAR O BOTAO PARA APAGAR
    Button(janela_apagar, text='Apagar Senha', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=apagar_senha).pack(padx=10, pady=10)

    #EXIBIR O RESULTADO DA ALTERAÇÃO DO TEXTO DE FORMA DINÂMICA
    resultado = Label(janela_apagar, text='', bg=f'{cor_bg}')
    resultado.pack(padx=10, pady=5)

    #BOTAO PARA VOLTAR A JANELA ANTERIOR
    Button(janela_apagar, text='Voltar', bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=janela_apagar.destroy).pack(padx=10, pady=5)

#FUNÇÃO PARA GERAR UMA SENHA ALEATÓRIA
def gerar_nova_senha(quantidade=25):
    #ADICIONANDO LETRAS + DIGITOS + PONTUAÇÔES NA VARIAVEL CARACTERES
    caracteres = string.ascii_letters + string.digits + string.punctuation
    #GERANDO UMA SENHA ALEATÓRIA DE ACORDO COM A QUANTIDADE DE CARACTER PASSADO COMO PARÂMETRO
    senha_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(quantidade))
    #DANDO O RETORNO DA SENHA NA TELA PRINCIPAL
    resultado.config(text=f'{senha_aleatoria}', fg=f'{cor_success}', font=('Bold', 12))
    #REATIVAR O BOTAO DE COPIAR SENHA QUE ESTÁ OCULTO  
    copiar_senha.pack(padx=10, pady=5)
    copiar_senha['state'] = 'normal'

#FUNÇÃO PARA COPIAR A SENHA APÓS TER SIDO GERADA
def copiar_nova_senha():
    #METODO PARA COPIAR A SENHA GERADA, PARA A SUA ÁREA DE TRANFERÊNCIA
    janela_principal.clipboard_clear()
    janela_principal.clipboard_append(resultado.cget("text"))
    janela_principal.update()
    resultado.config(text='Senha copiada com sucesso!', fg=f'{cor_success}', font=('Bold', 12))
    copiar_senha['state'] = 'disabled'

#CRIANDO A JANELA PRINCIPAL DO SISTEMA
janela_principal = Tk()
janela_principal.geometry('400x400')
janela_principal.title("Gerenciador de Senhas")
janela_principal.configure(background=f'{cor_bg}')

#TITULO DA JANELA PRINCIPAL
Label(janela_principal, text='Olá, seja bem-vindo(a) ao sistema!\nEscolha uma opção.', width=35, bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 14)).pack(padx=10, pady=10)

#BOTAO DE ABERTURA DA JANELA PARA CADASTRAR
Button(janela_principal, text="Cadastrar Senha", bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=abrir_janela_cadastrar).pack(padx=10, pady=7)

#BOTAO DE ABERTURA DA JANELA PARA VERIFICAR
Button(janela_principal, text="Verificar Senha", bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=abrir_janela_verificar).pack(padx=10, pady=7)

#BOTAO DE ABERTURA DA JANELA PARA MODIFICAR
Button(janela_principal, text="Modificar Senha", bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=abrir_janela_modificar).pack(padx=10, pady=7)

#BOTAO DE ABERTURA DA JANELA PARA APAGAR
Button(janela_principal, text="Apagar Senha", bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=abrir_janela_apagar).pack(padx=10, pady=7)

#BOTAO PARA GERAR UMA SENHA
Button(janela_principal, text="Gerar Senha", bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=gerar_nova_senha).pack(padx=10, pady=7)

#RETORNO DO TEXTO 'RESULTADO', SENDO ALTERADO DE ACORDO COM O ANDAMENTO DO SISTEMA
resultado = Label(janela_principal, text='', bg=f'{cor_bg}', fg=f'{cor_fonte}', font=('Bold', 12))
resultado.pack(padx=10, pady=5)

#BOTAO PARA COPIAR SENHA
copiar_senha = Button(janela_principal, text="Copiar Senha",bg=f'{cor_botao}', fg=f'{cor_fonte}', font=('Bold', 12), bd=4, width=20, command=copiar_nova_senha)
copiar_senha['state'] = 'disabled'

#MANTER A JANELA PRINCIPAL ABERTA
janela_principal.mainloop()
