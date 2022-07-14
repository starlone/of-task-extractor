import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

index_html_content = ""
with open("templates/index.html", mode="r") as f:
    index_html_content = f.read()


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=index_html_content, status_code=200)

DEV = os.getenv("DEV", "false") == 'true'

if __name__ == "__main__":
    if DEV:
        uvicorn.run('main:app', host="0.0.0.0", port=8000,
                    log_level="info", reload=True, debug=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
