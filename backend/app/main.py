from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Raíz de la API que retorna un mensaje de bienvenida."""
    return {"message": "Hello World"}


# punto de entrada cuando se ejecuta directamente
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
