# simulacion_trafico/environment/city.py

class City:
    """
    Clase que representa la ciudad que contiene semáforos, vehículos y
    cualquier otro elemento urbano (calles, intersecciones, etc.).
    """
    def __init__(self, name: str):
        self.name = name
        self.traffic_lights = []
        self.vehicles = []
        self.districts = []

    def add_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_district(self, district):
        self.districts.append(district)

    def __str__(self):
        return f"City: {self.name}, TrafficLights: {len(self.traffic_lights)}, Vehicles: {len(self.vehicles)}, Districts: {len(self.districts)}"
