# simulacion_trafico/main.py

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from environment.City import City
from environment.Vehicle import Vehicle
from environment.TrafficLight import TrafficLight
from simulation.simulator import Simulator, GTA6_estrenado, dia_opuesto
from concurrency.tasks import simulation_loop
from concurrency.tasks import run_simulation_tasks
from ui.gui_pygame import launch_pygame_gui
from distribution.rabbit_client import start_rabbitmq_messaging
from performance.metrics import log_simulation_state

#En heavy_computation ponemos los calculos de los eventos
#En run_simulation_tasks iria la función con dichos calculos
#En main llamamos a las funciones


def start_simulation(simulator, interval):
    asyncio.run(simulation_loop(simulator, interval))

def heavy_task_runner(executor, simulator):
    # Ejecuta una tarea pesada utilizando concurrent.futures
    result = executor.submit(lambda: heavy_computation(simulator)).result()
    print(result)

def verificar_estreno_GTA6(estreno, estreno_previsto, espera):
    GTA6_estrenado = False
    while estreno_previsto != estreno:
        print(f"Esperando que el estreno previsto coincida con el estreno en {estreno} dias")
        time.sleep(espera)
        estreno_previsto += 1
    print(f"El estreno previsto coincide con el estreno en {estreno} dias")
    GTA6_estrenado = True
    return GTA6_estrenado

def verificar_dia_opuesto(fecha_actual, fecha_celebracion, espera):
    dia_opuesto = False
    while fecha_celebracion != fecha_actual:
        print(f"Esperando que la fecha actual coincida con la de la celebración en {fecha_celebracion} dias")
        time.sleep(espera)
        fecha_actual += 1
    print(f"La fecha actual coincide con la de la celebración en {fecha_celebracion} dias")
    dia_opuesto = True
    return dia_opuesto

def heavy_computation(simulator):
    # Simula un cómputo pesado
    verificar_estreno_GTA6(190, 180, 1)

    verificar_dia_opuesto(365, 0, 1)

    return f"Heavy task result: {simulator.get_snapshot()}"

def log_loop(simulator):
    while True:
        log_simulation_state(simulator)
        time.sleep(1)

def main():
    # 1. Configurar el entorno de simulación
    city = City("Ciudad Ejemplo")
    tl1 = TrafficLight("T1", green_time=4, yellow_time=1, red_time=3)
    tl2 = TrafficLight("T2", green_time=5, yellow_time=1, red_time=4)
    veh1 = Vehicle("V1", position=(100, 300), speed=2.0, direction="NORTE")
    veh2 = Vehicle("V2", position=(200, 300), speed=3.0, direction="OESTE")
    city.add_traffic_light(tl1)
    city.add_traffic_light(tl2)
    city.add_vehicle(veh1)
    city.add_vehicle(veh2)
    simulator = Simulator(city)

    # 2. Iniciar la simulación en un hilo separado (se ejecuta con asyncio)
    sim_thread = threading.Thread(target=start_simulation, args=(simulator, 0.1), daemon=True)
    sim_thread.start()

    # 3. Iniciar RabbitMQ (mensajería distribuida) en otro hilo
    rabbit_thread = threading.Thread(target=start_rabbitmq_messaging, daemon=True)
    rabbit_thread.start()

    # 4. Ejecutar tareas pesadas usando concurrent.futures
    with ThreadPoolExecutor() as executor:
        heavy_task_thread = threading.Thread(target=heavy_task_runner, args=(executor, simulator), daemon=True)
        heavy_task_thread.start()

    # 5. Iniciar logging periódico de métricas
    log_thread = threading.Thread(target=log_loop, args=(simulator,), daemon=True)
    log_thread.start()

    # 6. Lanzar la GUI de Pygame (debe ir en el hilo principal)
    launch_pygame_gui(simulator)

if __name__ == "__main__":
    main()

