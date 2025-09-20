from fastapi import FastAPI
from routes import hello

app = FastAPI(title="My FastAPI Project")

# include routes
app.include_router(hello.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI 🚀"}
