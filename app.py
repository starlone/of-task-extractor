#!/usr/bin/python3

import sys

import git


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

    def file_to_str(self, offile):
        if offile.type == 'M':
            return self.name + '/' + offile.path
        return offile.type + ' ' + self.name + '/' + offile.path


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


if __name__ == "__main__":
    projects = ['/kdi_nia/git/nia-cognitivo-api']
    task = '1384766'

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
                    print(manager.file_to_str(offile))

            print("\n\nJoin Commits\n")
            for offile in manager.join_commits(**params):
                print(manager.file_to_str(offile))
