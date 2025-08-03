// 📡 Get the base URL for your Flask API from the .env file
const API_BASE = import.meta.env.VITE_API_URL;

/**
 * 🧰 Universal request handler
 * - Handles GET, POST, PUT, DELETE
 * - Automatically sets headers
 * - Serializes body
 * - Parses JSON
 */
async function request(endpoint, method = "GET", body = null) {
    console.log(`API f (!response.ok) call to: ${API_BASE}/${endpoint}`);

    const options = {
        method,
        headers: { "Content-Type": "application/json" },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}/${endpoint}`, options);

    if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        const message = errorBody.error || `Request failed`;
        const err = new Error(message);
        err.status = response.status;  // 🔥 pass actual HTTP status code
        throw err;
    }

    return response.json();
}

export const createPlayer = (data) => request("players/", "POST", data);

export const createOrUpdateProfile = (data) => request("profiles/", "POST", data);

export const getQuestions = (filters = {}) => {
    const params = new URLSearchParams(filters).toString()
    console.log("Fetching questions with filters:", filters);
    return request(`questions?${params}`)
}

export const startGameSession = (data) => request("games/", "POST", data);

export const getGameSessionById = (id) => request(`games/${id}`);

export const submitAnswer = (data) => request("game_questions/", "POST", data);

export const getPlayerByEmail = (email) => request(`players/email/${encodeURIComponent(email)}`);

export const getAllBadges = () => request("badges");

export const getPlayerBadges = (id) => request(`badges/player/${id}`);

export const grantBadge = (data) => request("badges/grant", "POST", data);

export const updateGameSession = (sessionId, score, questions_answered) => {
    return request(`games/${sessionId}`, "PUT", {
        score,
        questions_answered,
    });
};

export const getTopSessionScores = () => request("leaderboard/top-session-scores");

export const getProfileByPlayerId = (playerId) => request(`profiles/${playerId}`);
