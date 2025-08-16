import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { startGameSession } from "../api/apiService";

export default function GameInit() {
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const hasInitialized = useRef(false);

  useEffect(() => {
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    const init = async () => {
      const playerId = localStorage.getItem("playerId");
      if (!playerId) {
        navigate("/");
        return;
      }

      const existingSession = localStorage.getItem("sessionId");
      const storedQuestions = localStorage.getItem("questions");

      // ✅ Resume if session + questions already exist
      if (existingSession && storedQuestions) {
        navigate("/play");
        return;
      }

      try {
        const rawCategory = localStorage.getItem("playerCategory") || "preferred-difficulty";
        const payload = {
          player_id: parseInt(playerId, 10),
          use_difficulty: true, // always honor profile difficulty
          ...(rawCategory !== "preferred-difficulty" ? { category: rawCategory } : {})
        };

        const session = await startGameSession(payload);

        const questions = session.questions;
        if (!questions || questions.length === 0) {
          throw new Error("No questions received from server.");
        }

        localStorage.setItem("sessionId", session.id);
        localStorage.setItem("questions", JSON.stringify(questions));
        localStorage.setItem("currentIndex", "0");

        navigate("/play");
      } catch (err) {
        setError(err.message || "Failed to start session.");
      }
    };

    init();
  }, [navigate]);

  if (error) {
    return (
      <div className="text-center mt-32 text-red-600 text-xl font-semibold">
        🚫 Mission failed to initialize: {error}
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mb-4"></div>
      <p className="text-blue-700 font-semibold text-lg tracking-wide animate-pulse">
        🛰️ Syncing orbital data... Stand by.
      </p>
    </div>
  );
}
