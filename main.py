from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def screen_1():
    return FileResponse("static/index.html")

@app.get("/screen2")
def screen_2():
    return FileResponse("static/index2.html")

@app.get("/screen3")
def screen_3():
    return FileResponse("static/index3.html")

@app.get("/screen4")
def screen_4():
    return FileResponse("static/index4.html")

@app.get("/api/ping")
def test_api():
    return {"status": "FastAPI is connected!"}