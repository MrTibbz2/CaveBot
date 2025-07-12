import { Link } from 'preact-router/match';
export default function NotFound() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-gray-600 flex items-center justify-center opacity-0 animate-[fadeIn_0.3s_ease-in-out_forwards]">
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
  )
}