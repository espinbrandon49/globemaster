import { useNavigate } from "react-router-dom"
import Button from "../components/Button"

function StartPage() {
    const navigate = useNavigate()

    const handleStart = () => {
        navigate("/create-player")
    }

    return (
        <div className="start-page text-center space-y-6 bg-gradient-to-b from-black via-gray-900 to-blue-900 text-white min-h-screen flex flex-col items-center justify-center px-4">
            <h1 className="text-3xl font-bold text-blue-300 animate-pulse">
                🛰️ Welcome, Commander. GlobeMaster awaits.
            </h1>

            <p className="text-blue-100 text-lg font-medium">
                📍 Objective: Identify capitals, landmarks, and other intel.
            </p>

            <Button onClick={handleStart}>
                Begin Mission
            </Button>
        </div>
    );
}

export default StartPage;