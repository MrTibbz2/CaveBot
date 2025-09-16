# CaveCore/core.py
""" 
Core module for CaveCore framework. 
definses the Core class that manages services and configurations.
"""
from jsonrpc import method
class Core:
    def __init__(self):
        
        self.services = []

    def init():
        pass

    def run():
        pass

    def register_service(self, service):
        self.services.append(service)
        service_name = service.__class__.__name__

        for attr_name in dir(service):
            func = getattr(service, attr_name)
            # Register only methods marked with @rpc_method
            if callable(func) and getattr(func, "_rpc_exposed", False):
                method_name = f"{service_name}.{attr_name}"
                method(func, name=method_name)
                print(f"[CaveCore] Registered {method_name}")