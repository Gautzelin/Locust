#API generica para pruebas de carga y de estres
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()

class Datitos(BaseModel):
    num1: int
    num2: int

#Funcionalidad para manejo de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

#Endpoint que simula un ping al servidor de tipo get
@app.get("/ping")
def ping():
    return {"message": "pong"}

#Endpoint que realiza una suma que recibe parametros y es de tipo post
@app.post("/calcular")
def calcular(numeros: Datitos):
    result = numeros.num1 + numeros.num2
    print(result)
    #Condicion que verifica si es multiplo de 3 para generar un excepcion del lado del servidor
    if result % 3 == 0:
        raise HTTPException(status_code=400, detail="error en calculo")
    return {"result": result}

#Endpoint  para simular la recuperacion de informacion de un item
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    #Condicion que valida si el item es ih¿gual a 5 manda una excepcion
    if item_id == 5:
        raise HTTPException(status_code=400, detail="Item not found")
    return {"item_id": item_id}

#Inicializar el api
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")  