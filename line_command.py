#!/usr/bin/python3

import sys

import git_manager


def file_to_str(name, offile, complexidade=None):
    result = name + '/' + offile.path
    if complexidade:
        result = result + ' ' + complexidade
    if offile.type == 'A':
        result = '+' + result
    elif offile.type != 'M':
        result = offile.type + ' ' + result
    return result + '#' + offile.commit.hexsha[0:10]


if __name__ == "__main__":
    projects = ['/kdi_nia/git/nia-triton-manager']
    task = '570346'

    arquivos = {}

    if len(sys.argv) > 1:
        task = sys.argv[1]
        if len(sys.argv) > 2:
            projects = sys.argv[2:]

    for project in projects:

        name = project.split('/')[-1]

        commits = git_manager.find_commits(project, task)
        joins = git_manager.join_commits(commits)

        print('\n ##' + project)
        print("Commits\n")
        for commit in commits:
            print(str(commit))

        print("\n\nJoin Commits\n")
        for offile in joins:
            print(str(offile))
