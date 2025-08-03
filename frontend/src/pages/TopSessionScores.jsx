import { useEffect, useState } from "react";
import { getTopSessionScores } from "../api/apiService";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button"

export default function TopSessionScores() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    getTopSessionScores()
      .then((data) => {
        setSessions(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error("Error loading leaderboard:", err)
        setLoading(false)
      })
  }, [])

  const handleRestart = () => {
    localStorage.removeItem("sessionId");
    localStorage.removeItem("questions");
    localStorage.removeItem("currentIndex");
    navigate("/");  // Back to StartPage
  };

  if (loading) return <div className="p-4 text-center" >Loading leaderboard...</div>

  return (
    <>
      <div className="max-w-4xl mx-auto mt-16 bg-white shadow-2xl rounded-3xl p-8 border border-blue-100 animate-fade-in">
        <h1 className="text-4xl font-extrabold text-center text-blue-800 mb-8 tracking-wide">
          🏆 Top Session Scores
        </h1>

        <div className="overflow-x-auto">
          <table className="w-full text-sm sm:text-base text-left border-collapse">
            <thead>
              <tr className="bg-blue-50 border-b border-blue-200">
                <th className="py-3 px-4 font-semibold text-blue-700">#</th>
                <th className="py-3 px-4 font-semibold text-blue-700">Player</th>
                <th className="py-3 px-4 font-semibold text-blue-700">Score</th>
                <th className="py-3 px-4 font-semibold text-blue-700">Answered</th>
                <th className="py-3 px-4 font-semibold text-blue-700">Date</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((s, index) => (
                <tr key={s.session_id} className="border-b hover:bg-gray-50 transition duration-150">
                  <td className="py-2 px-4 font-bold text-blue-600">{index + 1}</td>
                  <td className="py-2 px-4">{s.player_name}</td>
                  <td className="py-2 px-4">{s.score}</td>
                  <td className="py-2 px-4">{s.questions_answered}</td>
                  <td className="py-2 px-4">{new Date(s.start_time).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex justify-center mt-8 animate-fade-in">
        <Button onClick={handleRestart}>🔁 Play Again</Button>
      </div>
    </>
  )
}
