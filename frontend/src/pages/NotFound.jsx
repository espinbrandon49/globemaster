import { useNavigate } from "react-router-dom"
import Button from "../components/Button"

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center bg-gradient-to-b from-black via-gray-900 to-blue-900 text-white px-4 space-y-6">
      <h1 className="text-4xl font-bold text-red-500 animate-pulse">
        🚫 Coordinates not found, Commander.
      </h1>
      <p className="text-gray-300 text-lg">
        Navigation system failed to lock onto target.
      </p>
      <Button onClick={() => navigate("/")} className="animate-fade-in delay-300">
        Return to Base
      </Button>
    </div>
  )
}