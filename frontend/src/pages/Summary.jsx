import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getGameSessionById } from "../api/apiService";
import BadgeDisplay from "../components/BadgeDisplay";

import Button from "../components/Button";

function Summary() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const sessionId = state?.sessionId || localStorage.getItem("sessionId")
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!sessionId) {
      setError("Session ID not found.")
      setTimeout(() => navigate("/"), 1500)
      return
    }

    const fetchSummary = async () => {
      try {
        const data = await getGameSessionById(sessionId)
        setSummary(data)
      } catch (err) {
        setError("Failed to load game summary")
      }
    }

    fetchSummary()
  }, [sessionId, navigate])

  const handleRestart = () => {
    localStorage.removeItem("sessionId");
    localStorage.removeItem("questions");
    localStorage.removeItem("currentIndex");
    navigate("/");  // Back to StartPage
  };


  if (error) {
    return (
      <div className="text-center mt-32 text-red-600 text-xl font-semibold">
        🚫 {error}
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mb-4"></div>
        <p className="text-blue-700 font-medium text-lg tracking-wide">
          📡 Retrieving debrief...
        </p>
      </div>
    );
  }

  const { score, questions_answered, player_id } = summary;
  const accuracy = questions_answered
    ? Math.round((score / questions_answered) * 100)
    : 0;

  return (
    <div className="max-w-xl mx-auto mt-20 text-center space-y-8">
      <h2 className="text-3xl font-bold text-blue-800 animate-pulse">
        🧭 Mission Debrief
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 animate-fade-in">
        <div className="bg-white shadow-md rounded-lg p-4 border border-blue-200">
          <p className="text-sm text-gray-500">📋 Questions Answered</p>
          <p className="text-2xl font-bold text-blue-700">{questions_answered}</p>
        </div>

        <div className="bg-white shadow-md rounded-lg p-4 border border-green-200">
          <p className="text-sm text-gray-500">🎯 Correct Answers</p>
          <p className="text-2xl font-bold text-green-600">{score}</p>
        </div>

        <div className="bg-white shadow-md rounded-lg p-4 border border-yellow-200">
          <p className="text-sm text-gray-500">🧠 Accuracy</p>
          <p className="text-2xl font-bold text-yellow-600">{accuracy}%</p>
        </div>
      </div>

      <BadgeDisplay playerId={player_id}/>
      <p className="text-yellow-500 italic text-sm tracking-wide">
        Intelligence archived. Awaiting next assignment.
      </p>
      <Button onClick={handleRestart} className="mt-6 animate-fade-in">
        Play Again
      </Button>
      <Button onClick={() => navigate("/leaderboard")} className="mt-3">🏆 View Top Scores</Button>
    </div>
  );
}

export default Summary;