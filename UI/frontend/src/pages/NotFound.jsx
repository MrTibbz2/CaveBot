import { Link } from 'preact-router/match';
import Particles from '../components/backgrounds/Particles/Particles';
export default function NotFound() {
  return (
    <div className="relative w-full min-h-[calc(100vh-64px)]">
      <div className="absolute inset-0">
        <Particles
          particleColors={['#4244b3', '#4104d9']}
          particleCount={1200}
          particleSpread={10}
          speed={0.1}
          particleBaseSize={100}
          moveParticlesOnHover={true}
          alphaParticles={false}
          disableRotation={false}
        />
      </div>
      <div className="absolute inset-0 flex items-center justify-center opacity-0 animate-[fadeIn_0.3s_ease-in-out_forwards]">
        <div className="text-center">
          <div className="text-9xl font-bold text-gray-800 mb-4">404</div>
          <h1 className="text-4xl font-bold text-white mb-4">Page Not Found</h1>
          <p className="text-xl text-gray-300 mb-8">The page you're looking for doesn't exist.</p>
          <Link 
            href="/" 
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300"
          >
            Go Home
          </Link>
        </div>
      </div>
    </div>
  )
}
