# of-task-extractor

## Requeriments
### Download the project
```
git clone https://github.com/starlone/of-task-extractor.git
cd ok-task-extractor
```

### pipenv
```
sudo pip3 install pipenv
```

### Intall dependencies
```
pipenv install
```

## Run
### Arguments
```
pipenv run python app.py <task> <path-project>
```

#### Example
```
pipenv run python app.py 1234 ~/projects/my-project
```

#### Multiple Projects
```
pipenv run python app.py 1234 ~/projects/my-project1 ~/projects/my-project2
```

## Contribute
### Intall dev dependencies
```
pipenv install --dev
```
