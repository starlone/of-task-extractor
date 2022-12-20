import os
from typing import List
import glob

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import git_manager

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class ApiBody(BaseModel):
    project: str
    tasks: List[str]


@app.get("/", response_class=HTMLResponse)
async def index():
    index_html_content = get_index_html()
    return HTMLResponse(content=index_html_content, status_code=200)


@app.post("/api")
def api(payload: ApiBody):
    tasks = []
    resp = {'tasks': tasks}
    projects = glob.glob(payload.project)
    for task in payload.tasks:
        commits = []
        for project in projects:
            comms = git_manager.find_commits(project, task)
            commits.extend(comms)
        result = git_manager.join_commits(commits)
        tasks.append({
            "files": [str(i) for i in result],
            "commits": [str(i) for i in commits],
            "task": task
        })
    return resp


def get_index_html():
    index_html_content = ""
    with open("templates/index.html", mode="r") as f:
        index_html_content = f.read()
    return index_html_content


DEV = os.getenv("DEV", "false") == 'true'

if __name__ == "__main__":
    if DEV:
        uvicorn.run('main:app', host="0.0.0.0", port=8000,
                    log_level="info", reload=True, debug=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
