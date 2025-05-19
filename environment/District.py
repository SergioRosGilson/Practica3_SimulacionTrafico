# simulacion_trafico/environment/district.py

class District:
    """
    Clase que modela el comportamiento de un distrito.
    """
    def __init__(self, id_, position=(0, 0)):
        self.id_ = id_
        self.position = position

    def __str__(self):
        return f"District {self.id_} at position {self.position}"