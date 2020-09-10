#!/usr/bin/python3

import sys
from datetime import datetime

import git

import request_of
from request_of import OfManagerRequest


def of_sort_files_type(file):
    return file.type


def of_sort_files_path(file):
    return file.path


class OfManager:
    def __init__(self, path):
        self.repo = git.Repo(path)
        self.files = []

        name = self.repo.git.working_dir
        self.name = name.split('/')[-1]

    def find_commits(self, **params):
        commits = []
        for commit in self.repo.iter_commits(**params):
            ofcommit = OfCommit(commit)
            commits.append(ofcommit)

        return commits

    def join_commits(self, **params):
        commits = self.find_commits(**params)
        return self._join_commits(commits)

    def _join_commits(self, commits):
        files = []
        paths = {}
        for ofcommit in commits:
            for offile in ofcommit.files:
                old = paths.get(offile.path)
                if old:
                    if offile.type == 'A':
                        files.remove(old)
                        files.append(offile)
                        paths[offile.path] = offile
                else:
                    if offile.type == 'R':
                        paths[offile.path_old] = offile
                    paths[offile.path] = offile
                    files.append(offile)
        files.sort(key=of_sort_files_path)
        files.sort(key=of_sort_files_type)
        return files

    def get_path(self, offile):
        return self.name + '/' + offile.path

    def file_to_str(self, offile, complexidade=None):
        result = self.name + '/' + offile.path
        if complexidade:
            result = result + ' ' + complexidade
        if offile.type != 'M':
            result = offile.type + ' ' + result
        return result


class OfCommit:
    def __init__(self, commit):
        self.files = []

        self.commit = commit
        self.message = commit.message

        parent = self.commit.parents[0]
        diffs = parent.diff(self.commit)
        for diff in diffs:
            offile = OfFile(diff)
            self.files.append(offile)

        self.files.sort(key=of_sort_files_path)
        self.files.sort(key=of_sort_files_type)


class OfFile:
    def __init__(self, diff):
        self.type = diff.change_type
        self.path = diff.a_path
        self.path_old = diff.b_path

    def __str__(self):
        if self.type == 'R':
            return self.type + " (" + self.path + " <- " + self.path_old + ")"
        return self.type + " " + self.path


def subtrair_buscar_arquivos(request, year, month):
    if (month == 1):
        month = 12
        year -= 1
    else:
        month -= 1
    vigencia = {'vigencia': {'mes': month, 'ano': year}}
    return request.get_ofs_files(vigencia)


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
    projects = ['/kdi_nia/git/nia-cognitivo-api']
    task = '1384766'

    print("Login OF Manager")
    request = OfManagerRequest()
    user = request.autenticar_line_command()
    arquivos = {}
    if user:
        now = datetime.now()
        month = now.month -1
        year = now.year

        qtd_meses = 3

        data = subtrair_mes(year, month, qtd_meses)
        for i in range(qtd_meses + 1):
            arquivos.update(request.get_ofs_files({'vigencia': data}))
            data = somar_mes(data['ano'], data['mes'], 1)

        print('# Arquivos OF Manager')
        for path in arquivos:
            print(path + " " + arquivos.get(path))

    if len(sys.argv) > 1:
        task = sys.argv[1]
        if len(sys.argv) > 2:
            projects = sys.argv[2:]

    for project in projects:
        manager = OfManager(project)

        params = {
            'grep': task,
            'no_merges': True
        }

        commits = manager.find_commits(**params)
        if commits:
            print('\n ##' + project)
            print("Commits\n")
            for commit in commits:
                print(commit.message)
                for offile in commit.files:
                    path = manager.get_path(offile)
                    complexidade = arquivos.get(path)
                    print(manager.file_to_str(offile, complexidade))

            print("\n\nJoin Commits\n")
            for offile in manager.join_commits(**params):
                path = manager.get_path(offile)
                complexidade = arquivos.get(path)
                print(manager.file_to_str(offile, complexidade))
