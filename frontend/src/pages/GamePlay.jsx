import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { submitAnswer, updateGameSession, getProfileByPlayerId, getGameSessionById } from "../api/apiService";
import Button from "../components/Button";

function GamePlay() {
  const location = useLocation();
  const navigate = useNavigate();


  const [questions] = useState(() => {
    const localQs = localStorage.getItem("questions");
    return localQs ? JSON.parse(localQs) : [];
  });

  const sessionId = localStorage.getItem("sessionId");
  const [currentIndex, setCurrentIndex] = useState(() => {
    const savedIndex = localStorage.getItem("currentIndex");
    return savedIndex ? parseInt(savedIndex, 10) : 0;
  });
  const [userAnswer, setUserAnswer] = useState("");
  const [error, setError] = useState("");
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const correctCountRef = useRef(0);

  const playerId = localStorage.getItem("playerId")
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    if (playerId) {
      getProfileByPlayerId(playerId)
        .then(setProfile)
        .catch(() => console.warn("⚠️ Could not load profile"))
    }
  }, [playerId])

  useEffect(() => {
    if (!sessionId || questions.length === 0) {
      navigate("/");
    }
  }, [sessionId, questions, navigate]);

  useEffect(() => {
    if (sessionId) {
      getGameSessionById(sessionId)
        .then(data => {
          correctCountRef.current = data.score;
          setCurrentIndex(data.questions_answered);
          localStorage.setItem("currentIndex", data.questions_answered);
        })
        .catch(() => {
          console.warn("⚠️ Could not restore session score");
        });
    }
  }, [sessionId]);

  const currentQuestion = questions[currentIndex];

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (hasSubmitted || !userAnswer.trim()) {
      setError("🚫 Mission input required, Commander.");
      return;
    }

    setHasSubmitted(true);
    setIsSubmitting(true);
    setError("");
    setShowFeedback(false);

    try {
      const sessionBefore = await getGameSessionById(sessionId);
      const scoreBefore = sessionBefore.score;

      await submitAnswer({
        session_id: sessionId,
        question_id: currentQuestion.id,
        player_answer: userAnswer,
      });

      const sessionAfter = await getGameSessionById(sessionId);
      const scoreAfter = sessionAfter.score;

      const wasCorrect = scoreAfter > scoreBefore;
      setIsCorrect(wasCorrect);
      setShowFeedback(true);

      if (wasCorrect) correctCountRef.current += 1;

      setTimeout(async () => {
        const nextIndex = currentIndex + 1;

        if (nextIndex >= 10 || nextIndex >= questions.length) {
          localStorage.removeItem("currentIndex");
          localStorage.removeItem("questions");
          localStorage.removeItem("sessionId");

          await updateGameSession(sessionId, correctCountRef.current, questions.length);

          navigate("/summary", { state: { sessionId } });
        } else {
          setCurrentIndex(nextIndex);
          localStorage.setItem("currentIndex", nextIndex);
          setUserAnswer("");
          setIsCorrect(null);
          setShowFeedback(false);
          setHasSubmitted(false);
          setIsSubmitting(false);
        }
      }, 1500);
    } catch {
      setError("Failed to submit answer.");
      setHasSubmitted(false);
      setIsSubmitting(false);
    }
  };


  const difficultyColors = {
    Easy: {
      bg: "bg-green-700",
      border: "border-green-300",
      text: "text-green-100",
      accent: "text-green-300",
    },
    Medium: {
      bg: "bg-blue-800",
      border: "border-blue-300",
      text: "text-blue-100",
      accent: "text-blue-300",
    },
    Hard: {
      bg: "bg-red-800",
      border: "border-red-300",
      text: "text-red-100",
      accent: "text-red-300",
    },
    default: {
      bg: "bg-gray-700",
      border: "border-gray-300",
      text: "text-gray-100",
      accent: "text-white",
    },
  };

  const style = difficultyColors[profile?.preferred_difficulty] || difficultyColors.default;

  return (
    <>
      <div className="game-play max-w-xl mx-auto mt-16 p-4">
        <h2 className="text-xl font-bold text-blue-800 mb-2">
          🎯 Target {currentIndex + 1} of 10
        </h2>
        <div className="text-sm text-gray-600 mb-4 space-y-1">
          <p>
            🗂️ <span className="font-medium">Category:</span> {currentQuestion.category}
          </p>
          <p>
            🔥 <span className="font-medium">Difficulty:</span> {currentQuestion.difficulty}
          </p>
        </div>
        <p>{currentQuestion.text}</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Type your intel here..."
            disabled={hasSubmitted}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-2 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          />
          <Button type="submit" disabled={hasSubmitted}>
            {isSubmitting ? (
              <div className="flex items-center gap-2">
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                <span>Submitting...</span>
              </div>
            ) : (
              "Submit Answer"
            )}
          </Button>
          {error && <p className="text-red-600 text-sm font-semibold mt-1">{error}</p>}
        </form>

        {showFeedback && (
          <div className="mt-4 space-y-2 transition-opacity duration-300 ease-in-out opacity-100">
            <p className={isCorrect ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
              {isCorrect ? "✅ Bullseye!" : "❌ Off Target"}
            </p>
            {!isCorrect && (
              <p className="text-gray-700 italic">
                Mission logged. You'll crush the next one.
              </p>
            )}
          </div>
        )}
      </div>
      {profile && (
        <div className={`fixed top-4 right-4 z-50 ${style.bg} ${style.text} rounded-xl shadow-lg p-4  ${style.border} border-2`}>
          <div className="flex items-center gap-3">
            {profile.avatar && (
              <img
                src={`https://robohash.org/${profile.player_id}?set=set5&size=80x80`}
                alt="Avatar"
                className="w-10 h-10 rounded-full border border-white"
              />
            )}
            <div>
              <p className="text-sm font-semibold">{profile.avatar}</p>
              <p className="text-xs">ID #{profile.player_id}</p>
            </div>
          </div>
          <hr className="my-2 border-white opacity-20" />
          <p className="text-xs opacity-80">🧭 Difficulty:</p>
          <p className={`font-bold ${style.accent}`}>{profile.preferred_difficulty}</p>
        </div>
      )}

    </>
  );
}

export default GamePlay;
