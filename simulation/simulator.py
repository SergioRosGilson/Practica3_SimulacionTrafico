# simulacion_trafico/simulation/simulator.py

GTA6_estrenado = False
dia_opuesto = False

class Simulator:
    """
    Clase encargada de orquestar las actualizaciones de la ciudad.
    """
    def __init__(self, city):
        self.city = city

    def update(self):
        """
        Actualiza el estado de todos los elementos de la ciudad en cada 'tick' de la simulación.
        """
        # 1. Actualizar semáforos
        for tl in self.city.traffic_lights:
            tl.update_state()
            if GTA6_estrenado:
                tl._change_state("RED")
            if dia_opuesto:
                tl.invert_state

        # 2. Mover vehículos
        for v in self.city.vehicles:
            v.move()
            if GTA6_estrenado:
                v.stop()
            
        # Aquí podrías añadir más lógica (detección de colisiones, congestión, etc.)

    def get_snapshot(self):
        """
        Retorna un resumen del estado actual de la simulación.
        Puede ser útil para la interfaz gráfica.
        """
        lights_info = [str(tl) for tl in self.city.traffic_lights]
        vehicles_info = [str(v) for v in self.city.vehicles]
        districts_info = [str(d) for d in self.city.districts]
        return {
            "traffic_lights": lights_info,
            "vehicles": vehicles_info,
            "districts": districts_info
        }
