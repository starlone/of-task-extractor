import os

import uvicorn
from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import git_manager

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class ApiBody(BaseModel):
    project: str
    task: str


@app.get("/", response_class=HTMLResponse)
async def index():
    index_html_content = get_index_html()
    return HTMLResponse(content=index_html_content, status_code=200)


@app.post("/api")
async def api(payload: ApiBody):
    commits = git_manager.find_commits(payload.project, payload.task)
    result = git_manager.join_commits(commits)
    return {
        "files": [str(i) for i in result],
        "commits": [str(i) for i in commits]
    }


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
