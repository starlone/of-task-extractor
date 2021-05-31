#!/usr/bin/python3

import getpass
import json
from datetime import datetime

import requests

url = 'https://manager-api.bbts.com.br/api/'

url_login = url + 'auth/login'

url_ofs = url + 'of/listar'

url_of = url + 'of/findOne'


class OfManagerRequest:
    def __init__(self):
        self.session = requests.Session()

    def autenticar(self, username, password):
        data = {'username': username, 'password': password}
        r = self.session.post(url_login, data=data)
        if r.status_code in (200, 201):
            user = r.json()
            token = 'Bearer ' + user.get('token')
            self.session.headers.update({'Authorization': token})
            self.session.headers.update({'Content-Type': 'application/json'})
            return user
        return None

    def get_ofs_files(self, vigencia):
        files = {}
        print('## OFs encontradas:')
        for of in self.get_ofs(vigencia):
            if of.get('ativo'):
                print("num: " + str(of.get('numOF')) + " - " + of.get('resumo'))
                obj = self.get_of_detail(of)
                if obj:
                    arqs = self.extract_files(obj)
                    files.update(arqs)
        return files

    def get_ofs(self, payload):
        r = self.session.post(url_ofs, data=json.dumps(payload))
        if r.status_code == 200:
            return r.json()
        return []

    def get_of_detail(self, of):
        payload = {"_id": of.get('_id')}
        r = self.session.post(url_of, data=json.dumps(payload))
        if r.status_code == 200:
            return r.json()
        return None

    def extract_files(self, obj):
        files = {}
        for tarefa in obj.get('tarefas'):
            for arquivo in tarefa.get('arquivos'):
                nome = arquivo.get('nome', '')
                nome = nome.lstrip().rstrip()
                if len(nome) and nome[0] == '/':
                    nome = nome[1:]
                guia = arquivo.get('guiaMetrica')
                complexidade = guia and guia.get('complexidade') or ''
                files.update({nome: complexidade})
        return files

    def autenticar_line_command(self):
        username = input("Username: ")
        if username:
            password = getpass.getpass('Password: ')
            user = self.autenticar(username, password)
            return user
        else:
            print('Uninformed user')

    def obter_complexidades(self, qtd_meses=3):
        arquivos = {}
        now = datetime.now()
        month = now.month - 1
        year = now.year
        data = subtrair_mes(year, month, qtd_meses)
        for i in range(qtd_meses + 1):
            arquivos.update(self.get_ofs_files({'vigencia': data}))
            data = somar_mes(data['ano'], data['mes'], 1)
        #     print(path + " " + arquivos.get(path))
        # for path in arquivos:
        # print('# Arquivos OF Manager')
        return arquivos


def subtrair_mes(ano, mes, qtd):
    for i in range(qtd):
        if (mes == 1):
            mes = 12
            ano -= 1
        else:
            mes -= 1
    return {'ano': ano, 'mes': mes}


def somar_mes(ano, mes, qtd):
    for i in range(qtd):
        if (mes == 11):
            mes = 0
            ano += 1
        else:
            mes += 1
    return {'ano': ano, 'mes': mes}


if __name__ == "__main__":
    print("Login OF Manager")
    manager = OfManagerRequest()
    user = manager.autenticar_line_command()
    if user:
        now = datetime.now()
        vigencia = {'vigencia': {'mes': now.month - 1, 'ano': now.year}}
        files = manager.get_ofs_files(vigencia)
        # print(files)
    else:
        print('Erro')
