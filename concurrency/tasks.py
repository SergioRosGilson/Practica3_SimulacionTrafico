# simulacion_trafico/concurrency/tasks.py

import asyncio
from distribution.rabbit_client import send_message

async def simulation_loop(simulator, interval):
    """
    Bucle que actualiza periódicamente la simulación.
    """
    while True:
        simulator.update()
        await asyncio.sleep(interval)

def vehicle_Behaviour():
    for v in simulator.city.vehicles:
        for tl in simulator.city.traffic_lights:
            if tl.current_state == "RED":
                if v.position == tl.position:
                    v.stop
                else:
                    v.move
        for d in simulator.city.districts:
            x, y = d.position
            if v.position > x and v.position < x + d.width and v.position > y and v.position < y + d.height:
                send_message()
            

def run_simulation_tasks(simulator, update_interval=1.0):
    """
    Crea y devuelve una lista de tareas asíncronas necesarias para la simulación:
    - Bucle de actualización de la ciudad
    - En un caso complejo, aquí se podrían añadir más tareas.
    """
    tasks = [asyncio.create_task(vehicle_Behaviour())]
    tasks.append(asyncio.create_task(simulation_loop(simulator, update_interval)))
    return tasks
