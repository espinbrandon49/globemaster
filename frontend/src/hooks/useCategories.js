import { useEffect, useState } from "react";
import { getCategories } from "../api/apiService";

const STORAGE_KEY = "cachedCategories";

export default function useCategories() {
  const [cats, setCats] = useState(() => {
    // Load from localStorage on first render
    const cached = localStorage.getItem(STORAGE_KEY);
    try {
      return cached ? JSON.parse(cached) : [];
    } catch {
      return [];
    }
  });

  const [loading, setLoading] = useState(cats.length === 0);
  const [err, setErr] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchCats = async () => {
      try {
        const data = await getCategories();
        if (isMounted && Array.isArray(data)) {
          setCats(data);
          localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        }
      } catch (e) {
        console.error("⚠️ Failed to load categories from API:", e);
        setErr("Failed to load categories");
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    // Always fetch to refresh, even if we have cached data
    fetchCats();

    return () => {
      isMounted = false;
    };
  }, []);

  // Build a label map for quick lookup
  const labelMap = cats.reduce((acc, c) => {
    if (c && c.key) acc[c.key] = c.label || c.key;
    return acc;
  }, {});

  const getLabel = (key) => {
    if (!key) return "";
    return labelMap[key] || key;
  };

  return { cats, getLabel, loading, err };
}
