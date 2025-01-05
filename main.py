from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return {"root": "How are you doing?"}

@app.get("/hello")
def hello():
    return {"Hello": "How are you doing?"}