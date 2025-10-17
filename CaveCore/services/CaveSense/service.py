from ..service import Service
from .cavesense import CaveSense

class CaveSenseService(Service):
    def __init__(self):
        super().__init__("CaveSenseService")
        self.cavesense = None
        self.cavemap = None

    def init(self, cavemap=None):
        self.cavemap = cavemap
        try:
            self.cavesense = CaveSense()
            self.cavesense.start(callback=self._on_sensor_data)
            print("CaveSenseService started.")
        except RuntimeError as e:
            print(f"CaveSenseService failed to start: {e}")
    
    def _on_sensor_data(self, data):
        print(f"Sensor scan: {data}")
        if self.cavemap:
            points = [{"sensor": k, "distance": v} for k, v in data.items()]
            self.cavemap.plot_points(points)

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