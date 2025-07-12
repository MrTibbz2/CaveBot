import Sidebar from '../components/Sidebar'
import MapContainer from '../components/MapContainer'

export default function MapWindow({logs}) {
    return (
        <div className="bg-gray-600 flex flex-row w-full min-h-[calc(100vh-64px)] h-[calc(100vh-64px)] opacity-0 animate-[fadeIn_0.4s_ease-in-out_forwards]">
                  <Sidebar logs={logs} />
                  <MapContainer />
                </div>
    );
};