import random
from locust import HttpUser, task, between

class PruebaEstres(HttpUser):
    #definir el tiempo de espera en segundos entre cada tarea que realiza un usuario virtual
    wait_time = between(1, 5)

    # Tarea para simular una peticion al servidor de apirest
    @task
    def getTask1(self):
        self.client.get("/ping")

    # Tarea que simula dos peticiones al servidor
    @task
    def getTask2(self):
        self.client.get("/ping")
        itemUrl = f"/items/{random.randint(1,10)}"
        for _ in range(10): #Simula que trae 10 items
            self.client.get(itemUrl)

    # Tarea que simula una peticion de tipo post con manejo de excepciones
    @task
    def errorTask(self):
        payload = {
            'num1': random.randint(1,15),
            'num2': random.randint(16,30)
            }
        headers = {"Content-Type": "application/json"}
        #Hace la peticion tipo post
        with self.client.post("/calcular", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code != 200: 
                #Valida si la peticion es erronea
                response.failure(f"Request failed with status code {response.status_code}")

'''
Comandos para las pruebas de estres
spawn-rate: controlar la velocidad a la que se crean los usuarios virtuales

Escenario1: simula 20 usuarios conectados simultaneamente a 1 usuario por segundo
locust --users 20 --spawn-rate 1 -H http://127.0.0.1:5000

Escenario2: simula 50 usuarios conectados simultaneamente a 5 usuarios concurrentes por segundo
locust --users 50 --spawn-rate 5 -H http://127.0.0.1:5000

Escenario3: simula 100 usuarios conectados simultaneamente a 20 usuarios por segundo
locust --users 100 --spawn-rate 20 -H http://127.0.0.1:5000

 http://127.0.0.1:5000 URL del apirest
'''





