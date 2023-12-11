#Impoetanto as bibliotecas:
from creds import usuario, senha
from time import sleep
import os
import random
import platform
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Introdução:
print('Bem vindo ao PersonalSafe!')
print('By: Arthur Speziali\n')
sleep(1)
print('Este cadastra usuários, senhas e textos dos usuários com segurança!')
print('PS: Coloque o seu e-mail e a senha dele no creds.py, funciona com Gmail.')
sleep(2)

#Função para mandar Emails com o SMTPLib:
def send_email(usuario, senha, destinatario, assunto, corpo):
    #O "error" define se teve algum erro no destinatário:
    error = False
    
    #Código retirado da documentação do SMTP:
    msg = MIMEMultipart()
    msg['From'] = usuario
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        #Tenta logar com o úsuario e senha do "creds.py", se não autenticar, imprime o acontecido e sai do programa:
        server.login(usuario, senha)
        
    except smtplib.SMTPAuthenticationError:
        print('\nÚsuario/Senha incorreta. Edite o arquivo "creds.py" para o seu úsuario e senha corretos!')
        print('Saindo, depois de alterar o úsuario e senha, inicie o programa!')
        exit()
        
    text = msg.as_string()
    try:
        #Tenta mandar para um Email "válido", que no minímo termine com "@gmail.com", se não autenticar, define "error" para True:
        server.sendmail(usuario, destinatario, text)
    
    except smtplib.SMTPRecipientsRefused:
        error = True 
    
    #No fim, ele fecha o servidor SMTP e retorna se teve erro, ou não:
    server.quit()
    return error


#Função para identificar o OS do úsuario, e limpar o terminal da maneira correta:
def clear_os():
    sys_os = platform.system()
    
    #Se for Windows, ele limpa o terminal com "cls":
    if sys_os == 'Windows': 
        os.system('cls')
    
    #Se for Linux ou Mac, limpa o terminal com "clear":
    else:
        os.system('clear')

#Função para salvar um dicionário em um .json:
def salvar_json(users: dict):
    os.chmod('users.json', 0o777)
    with open('users.json', 'w') as users_json:
        json.dump(users, users_json)        
    os.chmod('users.json', 0o770)

#Defini as permisões ao máximo, do arquivo.
#Feito para quando o usuário não tem permisão para abrir "users.json".
#Já que o Python utiliza das mesmas permisões que o usuário tem.
os.chmod('users.json', 0o777)

#Abre o .json, como um dicionário:
with open('users.json') as users_json:
    user_data = json.load(users_json)

#Volta as permisões a 0, para o usuário não ter acesso ao banco de dados:
os.chmod('users.json', 0o770)

#Um ciclo While para nunca sair do programa, somente quando pressionado CTRL + C:
while True:
    clear_os()
    print('Quer fazer Login, se cadastrar, ver todos os usuários ou mandar um E-mal para recuperar a senha? [L/R/V/E]. Digite ".." para sair:\n')

    while True:
        #Calcula se a opção está correta:
        opção = input('> ').strip().lower()
        
        if opção != 'l' and opção != 'r' and opção != 'v' and opção != 'e' and opção != '..':
            print('\nOpção inválida, tente novamente!\n')
        
        else:
            break
    
    #Usa o ".." para quebrar ciclos Whiles, e voltar no menu anterior:
    if opção == '..':
        print('Saindo... Volte sempre!')
        break
    
    elif opção == 'v':
        clear_os()
        print('Mostrando os usuários:\n')
        
        #Passa por cada item de user_data e atribui a "u":
        contador = 1
        for u, cont in user_data.items():
            print(f'{contador}-> {u}')
            
        print('\nConcluido!')
        enter = input('Pressine ENTER para continuar!')
    
    elif opção == 'l':
        #Detecta se o banco de dados (users.json) está vazio, se tiver ele fecha o programa:
        if user_data == {}:
            clear_os()
            print('Nenhum login encontrado, selecione cadastrar novo úsuario. Saindo!\n')
            break
        
        while True:
            clear_os()
            print('Logue com usuario e senha! Digite ".." para voltar ao menu anterior!\n')

            while True:
                print('Digite seu nome de úsuario:')

                user_name = input('> ').strip().lower()
                if user_name == '..':
                    break
                    
                print('Digite sua senha')
                user_pwd = input('> ').strip()
                
                #Verifica se tanto o úsuario, como a senha estão no banco de dados:
                if user_name in user_data and user_pwd in user_data[user_name]['pwd']:
                    clear_os()
                    print('\nLogin com sucesso!')
                    break
                        
                                                
                else:
                    #Espera um tempo antes de tentar novamente, para evitar Brute Force:
                    print('\nÚsuario/Senha inválidas, tente novamente em 3 segundos!\n')
                    sleep(5)
                    clear_os()

            if user_name == '..':
                break
            
            while True:
                clear_os()
                
                #Depois de atribuir o valor nos grupos, adiciona em uma lista.
                #Se o usuário digitar um número, constará que não existe este item, depois vai para outra verificação.
                #Vai verificar se ele cabe dentro da lista, e atribui-lo ao item no index do número:
                print('Qual grupo escolher? Digite ".." para voltar ao menu anterior:')    
                contador = 1
                group_list = list()
                for group, cont in user_data[user_name]['cont'].items():
                    print(f'{contador}=> {group}')
                    contador += 1
                    group_list.append(group)
                
                while True:
                    group = input('\n> ').strip()
                    
                    if group == '..':
                        break
                    
                    if group in user_data[user_name]['cont']:
                        content = user_data[user_name]['cont'][group]
                        clear_os()
                        break
                    
                    else:
                        if group.isnumeric():
                            group = int(group)
                            group = group_list[group - 1]
                            
                            if group in user_data[user_name]['cont']:
                                
                                #O "content" é todo conteúdo de um grupo, de um usuário:
                                content = user_data[user_name]['cont'][group]
                                break
                            
                            else:    
                                print('\nGrupo inválido, tente novamente!\n')
                        
                        else:
                            print('\nGrupo inválido, tente novamente!\n')
                            
                        
                if group == '..':
                    break
                        
                while True:
                    clear_os()
                    print('Deseja escrever, visualizar, excluir, editar ou manipular grupos? [W/R/X/E/G]. Digite ".." para voltar ao menu anterior!\n')

                    while True:
                        opção = input('> ').strip().lower()
                        
                        if opção != 'w' and opção != 'r' and opção != 'x' and opção != 'e' and opção != 'g' and opção != '..':
                            print('\nOpção inválida, tente novamente!\n')
                            
                        else:
                            break
                    
                    if opção == '..':
                        break
                    
                    elif opção == 'g':                        
                        while True:                            
                            clear_os()
                            print('Deseja excluir, criar, editar ou visualizar? [X/C/E/V]. Digite ".." para voltar ao menu anterior!\n')
                            opção = input('> ').strip().lower()
                            
                            if opção != 'x' and opção != 'c' and opção != 'e' and opção != 'v' and opção != '..':
                                print('\nOpção inválida, tente novamente!\n')

                            else:
                                if opção == '..':
                                    break
                                
                                elif opção == 'x':
                                    clear_os()
                                    
                                    if len(user_data[user_name]['cont']) > 1:
                                        print('Digite o nome do grupo:\n')
                                        
                                        while True:
                                            group = input('> ').strip().lower()
                                            
                                            #Verifica se existe esse grupo, e usa o .pop, para exclui-lo:
                                            if group in user_data[user_name]['cont']:
                                                user_data[user_name]['cont'].pop(group)
                                                salvar_json(user_data)
                                                print('\nConcluido!')
                                                enter = input('Pressine ENTER para continuar!')
                                                break
                                                
                                            else:
                                                print('\nGrupo não encontrado, tente novamente!\n')
                                                
                                    else:
                                        #Se o usuário ficar sem nenhum grupo, não consiguiria nem passar da tela de escolher um grupo.
                                        #Tendo que criar um novo usuário, por isto esta verificação:
                                        clear_os()
                                        print('Você não pode excluir o unico grupo que tem, edite ele!')    
                                
                                elif opção == 'c':
                                    clear_os()
                                    print('Digite o nome do novo grupo:\n')
                                    
                                    while True:
                                        group = input('> ').strip().lower()
                                        
                                        if group == '..':
                                            break
                                        
                                        if group != '' and group != ' ' and group != '..':
                                        
                                            #Verifica se não existe um grupo com este mesmo nome, depois cria ele com o .update:
                                            if not group in user_data:
                                                user_data[user_name]['cont'].update({group: {}})
                                                salvar_json(user_data)
                                                print('\nConcluído!')
                                                enter = input('Pressine ENTER para continuar!')
                                                clear_os()
                                                break
                                            
                                            else:
                                                print('\nGrupo já existente, tente novamente!\n')
                                                
                                        else:
                                            print('\nEsses caracteres são inválidos, tente novamente!\n')
                                            
                                elif opção == 'e':
                                    while True:
                                        clear_os()
                                        print('Digite o nome do grupo:\n')
                                        
                                        while True:
                                            group = input('> ').strip().lower()
                                            
                                            if group == '..':
                                                break
                                            
                                            #Verifica se o grupo existe, depois cria um novo com os mesmo itens, e exclui o anterior:
                                            if group in user_data[user_name]['cont']:
                                                break
                                            
                                            else:
                                                print('\nGrupo não encontrado, tente novamente!\n')
                                                
                                        if group == '..':
                                            break
                                                                                                                    
                                        while True:
                                            clear_os()
                                            print('Digite o novo nome do grupo:\n')
                                            
                                            while True:
                                                group_rename = input('> ').strip().lower()
                                                
                                                if group_rename == '..':
                                                    break
                                                
                                                if group_rename != '' and group_rename != ' ' and group_rename != '..':                                                    
                                                    user_data[user_name]['cont'].update({group_rename:content})
                                                    user_data[user_name]['cont'].pop(group)
                                                    salvar_json(user_data)
                                                    print('\nConcluido!')
                                                    enter = input('Pressine ENTER para continuar!')
                                                    clear_os()
                                                    break
                                                
                                                else:
                                                    print('\nEsses caracteres são inválidos, tente novamente!\n')
                                                    
                                            if group_rename == '..':
                                                break
                                            
                                elif opção == 'v':
                                    clear_os()
                                    print('Os grupos criados foram:\n')
                                    
                                    contador = 1
                                    for group, cont in user_data[user_name]['cont'].items():
                                        print(f'{contador}=> {group}')
                                        contador += 1
                                        
                                    print('\nConcluido!')
                                    enter = input('Pressine ENTER para continuar!')
                                    clear_os()
                                    break
                                                                        
                    
                    elif opção == 'w':
                        while True:
                            
                            clear_os()
                            print('Escreva uma tag e com chave. Digite ".." para voltar ao menu anterior!\n')
                            
                            while True:
                                print('Digite o nome da tag:')
                                tag = input('> ').strip()
                                if tag == '..':
                                    break
                                
                                elif tag in content:
                                    print('\nTag ja existente, ecolha outra!\n')
                                    
                                else:
                                    if tag != '' and tag != ' ':
                                        print('Digite a chave da tag:')
                                        
                                        while True:
                                            chave = input('>').strip()
                                            if chave != '' and chave != ' ' and chave != '..':
                                                content.update({tag: chave})
                                                salvar_json(user_data)
                                                print('\nConcluido!')
                                                enter = input('Pressine ENTER para continuar!')                                                
                                                clear_os()
                                                break
                                            
                                            else:
                                                print('\nA chave não pode conter esses caracteres!\n')
                                                
                                        break
                                    
                                    else:
                                        print('\nA tag não pode conter estes caracteres!\n')
                                
                            if tag == '..':
                                break
                    
                    elif opção == 'e':
                        while True:
                            
                            clear_os()
                            print('Edite uma tag/chave. Digite ".." para voltar ao menu anterior!\n')
                            
                            print('Deseja editar uma tag ou uma chave? [T/K]')
                            while True:
                                opção = input('> ').strip().lower()
                                
                                if opção != 't' and opção != 'k' and opção != '..':
                                    print('\nOpção inválida, tente novamente!\n')
                                
                                else:
                                    clear_os()
                                    break
                            
                            if opção == '..':
                               break
                            
                            elif opção == 't':
                                while True:
                                    clear_os()
                                    print('Edita o nome de uma tag. Digite ".." para voltar ao menu anterior!')
                                    
                                    print('Qual o nome da tag?\n')                                
                                    while True:                                    
                                        tag = input('> ').strip()
                                        if tag == '..':
                                            break
                                        
                                        if tag in content:
                                            
                                            chave = user_data[user_name]['cont'][group][tag]
                                            clear_os()
                                            
                                            while True:
                                                print('Digite o novo nome da tag\n')
                                                tag_rename = input('> ')
                                                
                                                if tag_rename != '' and tag_rename != ' ' and tag_rename != '..':
                                                    content.update({tag_rename: chave})
                                                    
                                                    content.pop(tag)
                                                    salvar_json(user_data)
                                                    print('\nConcluido!')
                                                    enter = input('Pressine ENTER para continuar!')
                                                    break
                                                
                                                else:
                                                    print('\nEsses caracteres são inválidos, tente novamente!\n')
                                                    
                                            break
                                                
                                        else:
                                            print('\nTag não encontrada, tente novamente!\n')
                                            
                                    if tag == '..':
                                        break
                                    
                            elif opção == 'k':
                                while True:
                                    clear_os()
                                    print('Edita o nome de uma chave. Digite ".." para voltar ao menu anterior!')
                                    
                                    print('Qual o nome da tag?\n')                                
                                    while True:                                    
                                        tag = input('> ').strip()
                                        if tag == '..':
                                            break
                                        
                                        if tag in content:
                                            break
                                        
                                        else:
                                            print('\nTag não encontrada, tente novamente!\n')
                                    
                                    if tag == '..':
                                        break
                                    
                                    
                                    clear_os()
                                    print('Digite o novo nome da chave:\n')                                        
                                    while True:
                                        chave_rename = input('> ').strip().lower()
                                        if chave_rename != '' and chave_rename != ' ' and chave_rename != '..':

                                            content.update({tag: chave_rename})
                                            salvar_json(user_data)
                                            print('\nConcluido!')
                                            enter = input('Pressine ENTER para continuar!')
                                            break
                                        
                                        else:
                                            print('\nEsses caracteres são inválidos, tente novamente!\n')
  
                    elif opção == 'x':
                        while True:

                            clear_os()
                            print('Exclua uma tag junto com a chave. Digite ".." para voltar ao menu anterior!\n')
                            
                            print('Digite a tag da chave a ser excluída:')
                            while True:
                                
                                tag = input('> ').strip()
                                if tag == '..':
                                    break
                                
                                if tag in content:
                                    content.pop(tag)
                                    salvar_json(user_data)
                                    print('\nConcluido!')
                                    enter = input('Pressine ENTER para continuar!')
                                    break
                                
                                else:
                                    print('\nTag não encontrada, tente novamente!\n')
                                    
                            if tag == '..':
                                break
                            
                    elif opção == 'r':
                        while True:
                    
                            clear_os()
                            print('Exibe chaves dentro de tags. Digite ".." para voltar ao menu anterior!\n')
                            
                            print('\nDeseja fazer uma busca pela tag ou exibir tudo? [K/S]')
                            
                            while True:
                                opção = input('> ').strip().lower()
                                
                                if opção != 'k' and opção != 's' and opção != '..':
                                    print('\nOpção inválida, tente novamente!\n')
                                    
                                else:
                                    break
                            
                            if opção == '..':
                                break
                            
                            elif opção == 'k':
                                while True:
                                    clear_os()
                                    
                                    while True:
                                        print('\nQual será a tag? Digite ".." para voltar ao menu anterior!')
                                        key = input('> ').strip()
                                        
                                        if key == '..':
                                            print('Saindo...')
                                            break
                                        
                                        clear_os()
                                        print('Chaves encontradas: ')
                                        for e, i in enumerate(content):
                                            if key in i:
                                                print(f'{e + 1}-> {i} == {content[i]}')
                                                
                                    if key == '..':
                                        break

                            
                            elif opção == 's':
                                while True:
                                    
                                    clear_os()
                                    print('Mostra todas as tags com chaves registradas.')
                                    
                                    print('Todos as chaves registradas:\n')
                                    
                                    for e, i in enumerate(content):
                                        print(f'{e + 1}-> {i} == {content[i]}')
                                    
                                    print('\nConcluido!')
                                    enter = input('Pressine ENTER para continuar!')
                                    clear_os()
                                    break
                     
                        
    elif opção == 'r':
        clear_os()
        while True:
            print('Digite seu novo nome de úsuario:')
            register_name = input('> ').strip().lower()
            
            if register_name == '..':
                break
            
            #Verifica se existe já este mesmo nome de usuário.
            #O programa evita de colocar esses 3 tipos de caracteres:
            if not register_name in user_data:                
                if register_name != '' and register_name != ' ' and register_name != '..':
                    
                    print('Digite sua nova senha de úsuario:')
                    while True:
                        register_pwd = input('> ').strip()
                        
                        if register_pwd != '' and register_pwd != ' ' and register_pwd != '..':
                            clear_os()
                            print('Digite um E-mail para recuperação caso perca a senha:\n')
                            
                            #Prepara o assunto e corpo do Email de boas vindas:
                            ass_welcome = 'Seja bem-vindo ao PersonalSafe!'
                            body_welcome = f'''
Olá {register_name.capitalize()}! Seja bem vindo ao PersonalSafe!
Venho por este E-mail, lhe desejar boas vindas ao meu programa em Python.

Não se esqueça de conferir a página do projeto (https://github.com/ArthurSpeziali/PersonalSafe)

**Caso não tenha se registrado neste programa, ignore este E-mail**
'''
                            
                            while True:
                                email = input('> ').strip().lower()

                                #Se conseguir mandar o Email com destinário correto, ele salva os dados do úsuario no banco de dados:                                                                
                                if send_email(usuario, senha, email, ass_welcome, body_welcome):
                                    print('\nDestinatário incorreto, tente novamente!\n')
                                    
                                else:
                                    break
                            
                            #Salvando deste jeito, para o grupo ser previamente definido:
                            user_data.update({register_name: {'pwd': register_pwd,'email': email, 'cont': {'standard_group': {}}}})
                            salvar_json(user_data)        

                            clear_os()
                            print('Cadastro realizado com êxito, reinicie e logue na sua conta!')
                            enter = input('Pressine ENTER para continuar!')
                            break                                                    
                            
                        else:
                            print('\nEsses caracteres são inválidos, tente novamente!\n')
                
                else:
                    print('\nEsses caracteres são inválidos, tente novamente!\n')

            else:
                print('\nNome de úsuario ja existe, tente novamente!\n')
                
    
    elif opção == 'e':
        while True:
            clear_os()
            print('Digite seu nome de úsuario. Digite ".." para voltar ao menu anterior!\n')
            
            while True:
                user_name = input('> ').strip().lower()
                
                if user_name == '..':
                    break
                
                if user_name in user_data:
                    break
                
                
                else:
                    print('\nÚsuario não encontrado, tente novamente!\n')
                    
            if user_name == '..':
                break
                
            #Gerando um código aleatório de 6 digítos (1000 - 9999):
            cod_random = random.randint(10**5, 10**6 - 1)
            
            #Preparando o Email de recuperação de senha:
            ass_recovery = 'Recuperação da sua senha!'
            body_recovery = f'''
Olá {user_name}! Recupere sua senha agora!
Recebemos uma solicitação para redefinir sua senha do PersonalSafe.

Recupere via este código:

--- {cod_random} ---

So coloque este código de 6 números no programa, e recupere sua senha.

**Caso desconheça desta solicitação, ignore este E-mail!**
'''
            
            #A aréa do usuario é dividido em 3 "containers".
            #O "pwd" guarda a senha do usuário.
            #O "email" guarda o Email de recuperação do usuário.
            #O "cont" guarda os grupos, que guarda as tag com as chaves.
            
            email = user_data[user_name]['email']
            
            #Manda o Email, tendo certeza que o destinário existe:
            send_email(usuario, senha, email, ass_recovery, body_recovery)
            
            clear_os()
            print('E-mail enviado. Digite o código correspondente do E-mail:\n')
            while True:
                cod = input('> ').strip()
                
                #Verifica se o código dado pelo usuário, é o mesmo do Email:
                if cod == str(cod_random):
                    clear_os()
                    print('Código válidado com sucesso!\n')
                    break
                
                else:
                    print('\nCódigo inválido, tente novamente em 10 segundos!\n')
                    sleep(10)
                    
                    
            while True:
                print('Digite sua nova senha de úsuario:\n')
                user_pwd = input('> ').strip().lower()
                
                #Usa os requísitos de caracteres para certificar que a senha não dara problemas, e salva no banco de dados:                                                                            
                if user_pwd != '' and user_pwd != ' ' and user_pwd != '..':
                    user_data[user_name].update({'pwd': user_pwd})
                    salvar_json(user_data)
                    print('\nSenha alterada com sucesso!')
                    enter = input('Pressine ENTER para continuar!')
                    break

                else:
                    print('\nEsses caracteres são inválidos, tente novamente!\n')
