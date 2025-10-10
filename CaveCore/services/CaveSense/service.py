from ..service import Service
from .cavesense import CaveSense

class CaveSenseService(Service):
    def __init__(self):
        super().__init__("CaveSenseService")
        self.cavesense = None

    def init(self):
        self.cavesense = CaveSense()
        self.cavesense.start()
        print("CaveSenseService started.")

    def kill(self):
        if self.cavesense:
            self.cavesense.close()
        print("CaveSenseService stopped.")
    
    def begin_scan(self):
        if self.cavesense:
            self.cavesense.begin_scan()
    
    def end_scan(self):
        if self.cavesense:
            self.cavesense.end_scan()
    
    def get_sensor_data(self):
        return self.cavesense.sensor_data if self.cavesense else {}
    
    def get_status(self):
        return self.cavesense.status if self.cavesense else "UNKNOWN"