from services.CaveSense.service import CaveSenseService
from services.PrimeDrive.service import PrimeDriveService
from services.CaveMap.service import CaveMapService

cavesense = CaveSenseService()
primedrive = PrimeDriveService(hub_name="NSE_Pybricks")  # Change if needed
cavemap = CaveMapService()


