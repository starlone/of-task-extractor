#!/usr/bin/python3

import sys

import git

from request_of import OfManagerRequest


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
        commits.reverse()
        return commits

    def join_commits(self, **params):
        commits = self.find_commits(**params)
        return self._join_commits(commits)

    def _join_commits(self, commits):
        files = []
        paths = {}
        for ofcommit in commits:
            for offile in ofcommit.files:
                if offile.path not in paths:
                    if offile.type == 'R' and offile.path_old in paths:
                        old = paths.get(offile.path_old)
                        files.remove(old)
                    paths[offile.path] = offile
                    files.append(offile)
        files.sort(key=lambda x: x.path)
        files.sort(key=lambda x: x.type)
        return files

    def get_path(self, offile):
        return self.name + '/' + offile.path

    def file_to_str(self, offile, complexidade=None):
        result = self.name + '/' + offile.path
        if complexidade:
            result = result + ' ' + complexidade
        if offile.type != 'M':
            result = offile.type + ' ' + result
        return result + '#' + offile.commit.hexsha[0:10]


class OfCommit:
    def __init__(self, commit):
        self.files = []

        self.commit = commit
        self.message = commit.message

        parent = self.commit.parents[0]
        diffs = parent.diff(self.commit)
        for diff in diffs:
            offile = OfFile(self.commit, diff)
            self.files.append(offile)

        self.files.sort(key=lambda x: x.path)
        self.files.sort(key=lambda x: x.type)


class OfFile:
    def __init__(self, commit, diff):
        self.type = diff.change_type
        self.path = diff.b_path
        self.path_old = diff.a_path
        self.commit = commit

    def __str__(self):
        if self.type == 'R':
            return self.type + " (" + self.path + " <- " + self.path_old + ")"
        return self.type + " " + self.path


def obter_complexidade_of_manager():
    print("Login OF Manager")
    request = OfManagerRequest()
    user = request.autenticar_line_command()
    if user:
        return request.obter_complexidades()


if __name__ == "__main__":
    projects = ['/kdi_nia/git/nia-cognitivo-api']
    task = '1384766'
    BUSCAR_COMPLEXIDADE = False

    arquivos = {}
    if BUSCAR_COMPLEXIDADE:
        arquivos = obter_complexidade_of_manager()

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
                print('\n ' + commit.commit.hexsha[0:10] + ' - ' + str(
                    commit.commit.authored_datetime) + " - " + commit.message)
                # for offile in commit.files:
                #     path = manager.get_path(offile)
                #     complexidade = arquivos.get(path)
                #     print(manager.file_to_str(offile, complexidade))

            print("\n\nJoin Commits\n")
            for offile in manager.join_commits(**params):
                path = manager.get_path(offile)
                complexidade = arquivos.get(path)
                print(manager.file_to_str(offile, complexidade))
