# the base service used by all services.
class Service:
    def __init__(self, name: str):
        self.name = name

    def init(self):
        print(f"ERROR: Service {self.name} has no start implementation.")

    def kill(self):
        print(f"ERROR: Service {self.name} has no stop implementation.")