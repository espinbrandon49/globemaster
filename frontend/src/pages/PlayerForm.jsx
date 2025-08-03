import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { createPlayer, createOrUpdateProfile, getPlayerByEmail } from "../api/apiService";
import { generateCodename } from "../utils/generateCodenameRoulette";

import Button from "../components/Button";

function PlayerForm() {
  const [name, setName] = useState(localStorage.getItem("playerName") || "")
  const [difficulty, setDifficulty] = useState("Easy")
  const [category, setCategory] = useState("preferred-difficulty")
  const [error, setError] = useState(null)
  const [avatar, setAvatar] = useState(generateCodename())
  const navigate = useNavigate()

  // Skip if already in localStorage
  // useEffect(() => {
  //   const playerId = localStorage.getItem("playerId")
  //   const playerName = localStorage.getItem("playerName")

  //   if (playerId && playerName) {
  //     navigate("/init")
  //   }
  // }, [navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    const trimmedName = name.trim()
    if (!trimmedName) {
      setError("🚫 Commander identity missing.");
      return
    }

    try {
      const email = `${trimmedName.toLowerCase().replace(/\s+/g, "")}@example.com`

      let player;
      try {
        player = await getPlayerByEmail(email);
      } catch (err) {
        if (err.status === 404) {
          player = await createPlayer({ name: trimmedName, email });
        } else {
          throw err; // surface other errors (e.g. network, 500, etc)
        }
      }

      localStorage.setItem("playerId", player.id)
      localStorage.setItem("playerName", trimmedName)
      localStorage.setItem("playerDifficulty", difficulty)
      localStorage.setItem("playerCategory", category)

      await createOrUpdateProfile({
        player_id: player.id,
        avatar,
        preferred_difficulty: difficulty,
      })

      navigate("/init")
    } catch (err) {
      setError(err.message || "⚠️ System failure. Try again.");
    }
  }

  return (
    <div className="player-form max-w-md mx-auto mt-20 bg-white shadow-md rounded-lg p-8 text-center space-y-6 border border-blue-100">
      <h2 className="text-2xl font-bold text-blue-800 animate-pulse">
        🪪 Mission Prep: Identify Yourself
      </h2>

      {error && (
        <p className="text-red-600 text-sm font-semibold">{error}</p>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <label className="block text-left">
          <span className="text-sm font-medium text-gray-700">Call Sign</span>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </label>

        <label className="block text-left">
          <span className="text-sm font-medium text-gray-700">Training Intensity</span>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Easy">Easy</option>
            <option value="Intermediate">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </label>
        <label className="lock text-left">
          <span className="text-sm font-medium text-gray-700">Mission Type</span>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="mt-1 w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="preferred-difficulty">🎲 Surprise Me (By Difficulty)</option>
            <option value="Capitals">Capitals</option>
            <option value="Famous Landmarks">Famous Landmarks</option>
            <option value="Country Flags">Country Flags</option>
            <option value="Oceans and Seas">Oceans and Seas</option>
            <option value="Cultural Foods">Cultural Foods</option>
            <option value="Animal Habitats">Animal Habitats</option>
            <option value="Languages of the World">Languages of the World</option>
            <option value="Natural Wonders">Natural Wonders</option>
          </select>
        </label>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600 italic">
            Avatar: <span className="font-bold">{avatar}</span>
          </span>

          <Button onClick={() => setAvatar(generateCodename())} className="ml-2 text-xs py-1 px-2">
            🎲 Shuffle Avatar
          </Button>
        </div>

        <Button type="submit" disabled={!name.trim()}>
          Launch Mission
        </Button>
      </form>
      <p className="text-xs text-gray-400 italic mt-6">
        Commander profile will be stored locally. No transmission necessary.
      </p>
    </div>
  );
}

export default PlayerForm