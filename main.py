from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def hello():
    return "Hello there!"

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)