import { useEffect, useState } from "react";
import { getPlayerBadges, getAllBadges } from "../api/apiService";
import useCategories from "../hooks/useCategories"; // ✅ added

function BadgeDisplay({ playerId }) {
  const [playerBadges, setPlayerBadges] = useState([]);
  const [allBadges, setAllBadges] = useState([]);
  const { getLabel } = useCategories(); // ✅ lookup for category labels

  useEffect(() => {
    const fetchBadges = async () => {
      try {
        const [playerData, badgeCatalog] = await Promise.all([
          getPlayerBadges(playerId),
          getAllBadges(),
        ]);

        setPlayerBadges(playerData);
        setAllBadges(badgeCatalog);
      } catch (err) {
        console.error("Failed to load badges:", err.message);
      }
    };

    fetchBadges();
  }, [playerId]);

  const earnedBadgeIds = new Set(playerBadges.map((pb) => pb.badge_id));

  return (
    <div className="bg-white shadow rounded-lg p-4 border border-blue-100">
      <h3 className="text-lg font-bold text-blue-800 mb-2 flex items-center gap-2">
        🏅 Honors Earned
        <span className="text-xs font-medium text-gray-500">
          {Array.from(earnedBadgeIds).length} total
        </span>
      </h3>
      <ul className="grid grid-cols-2 sm:grid-cols-3 gap-3 mt-2">
        {allBadges.map((badge) => {
          const isEarned = earnedBadgeIds.has(badge.id);
          const categoryLabel =
            badge.category && getLabel(badge.category) !== badge.category
              ? getLabel(badge.category)
              : badge.category || null;

          return (
            <li
              key={badge.id}
              className={`border rounded p-3 flex flex-col items-center text-center shadow-sm transition-shadow ${isEarned
                  ? "bg-yellow-50 border-yellow-200 hover:shadow-md"
                  : "bg-gray-100 border-gray-300 opacity-60"
                }`}
            >
              <span className={`text-3xl ${isEarned ? "" : "grayscale"}`}>
                {isEarned ? badge.icon : "🔒"}
              </span>
              <p className="font-semibold mt-2 text-sm text-blue-900">
                {badge.name}
              </p>
              {categoryLabel && (
                <p className="text-[11px] text-gray-500 italic">
                  {categoryLabel}
                </p>
              )}
              <p className="text-xs text-gray-600 mt-1">{badge.description}</p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default BadgeDisplay;
