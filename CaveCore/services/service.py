# cavecore/services/service.py
class Service:
    """
    Base class for all CaveCore services.
    Each service wraps a subsystem and exposes its API to CaveCore.
    """

    def __init__(self, core, name: str):
        self.core = core
        self.name = name

    def start(self):
        """
        Connect to or start the subsystem.
        """
        raise NotImplementedError

    def stop(self):
        """
        Stop or clean up the subsystem.
        """
        raise NotImplementedError


def rpc_method(func):
    """
    Marks a method to be exposed via JSON-RPC.
    """
    func._rpc_exposed = True
    return func