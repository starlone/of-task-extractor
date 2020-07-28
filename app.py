#!/usr/bin/python3

import sys

import git


class OfManager:
    def __init__(self, path):
        self.repo = git.Repo(path)
        self.files = []

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
                if not old:
                    if offile.type == 'R':
                        paths[offile.path_old] = offile
                    paths[offile.path] = offile
                    files.append(offile)
        return files


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
        print(project)
        manager = OfManager(project)

        params = {
            'grep': task,
            'no_merges': True
        }

        print("Commits")
        for commit in manager.find_commits(**params):
            print(commit.message)
            for offile in commit.files:
                print(offile)

        print("\n\nJoin Commits")
        for offile in manager.join_commits(**params):
            print(offile)
