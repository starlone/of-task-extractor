import git


def find_commits(project, task):
    repo = git.Repo(project)
    params = {
        'grep': task,
        'no_merges': True
    }
    commits = []
    for commit in repo.iter_commits(**params):
        ofcommit = OfCommit(commit)
        commits.append(ofcommit)
    commits.reverse()
    return commits


def join_commits(commits):
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


class OfCommit:
    def __init__(self, commit):
        project = commit.repo.working_dir.split('/')[-1]

        self.files = []

        self.commit = commit
        self.message = commit.message
        self.hash = commit.hexsha[0:10]
        self.date = commit.authored_datetime

        parent = self.commit.parents[0]
        diffs = parent.diff(self.commit)
        for diff in diffs:
            offile = OfFile(project, self, diff)
            self.files.append(offile)

        self.files.sort(key=lambda x: x.path)
        self.files.sort(key=lambda x: x.type)

    def __str__(self):
        return self.hash + ' - ' + str(self.date) + " - " + self.message


class OfFile:
    def __init__(self, project, parent, diff):
        self.project = project
        self.parent = parent

        self.type = diff.change_type
        self.path = diff.b_path
        self.path_old = diff.a_path

    def __str__(self, complexidade=None):
        result = self.project + '/' + self.path
        if complexidade:
            result = result + ' ' + complexidade
        if self.type == 'A':
            result = '+' + result
        elif self.type != 'M':
            result = self.type + ' ' + result
        return result + '#' + self.parent.hash
