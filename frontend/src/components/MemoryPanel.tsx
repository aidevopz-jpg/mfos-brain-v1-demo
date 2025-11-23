import React, { useEffect, useState } from "react";
import axios from "axios";

interface MemoryItem {
  id: string;
  text: string;
  metadata: any;
}

interface Props {
  apiBase: string;
}

const MemoryPanel: React.FC<Props> = ({ apiBase }) => {
  const [items, setItems] = useState<MemoryItem[]>([]);
  const [query, setQuery] = useState("");
  const [activeItem, setActiveItem] = useState<MemoryItem | null>(null);

  const fetchAll = async () => {
    try {
      const res = await axios.get<MemoryItem[]>(`${apiBase}/api/memory`);
      setItems(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const search = async () => {
    if (!query.trim()) {
      await fetchAll();
      return;
    }
    try {
      const res = await axios.get<MemoryItem[]>(`${apiBase}/api/memory/search`, {
        params: { q: query },
      });
      setItems(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchAll();
  }, []);

  return (
    <aside className="memory-panel">
      <h2>Memory Spine</h2>
      <div className="memory-search">
        <input
          type="text"
          placeholder="Search memory…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={search}>Search</button>
      </div>
      <div className="memory-list">
        {items.map((item) => (
          <div
            key={item.id}
            className={`memory-item ${
              activeItem?.id === item.id ? "active" : ""
            }`}
            onClick={() => setActiveItem(item)}
          >
            <div className="memory-title">
              {item.metadata?.tags?.join(", ") || "Untitled"}
            </div>
            <div className="memory-meta">
              {item.metadata?.created_at || ""}
            </div>
          </div>
        ))}
      </div>
      <div className="memory-detail">
        {activeItem ? (
          <>
            <h3>Memory Detail</h3>
            <pre>{activeItem.text}</pre>
          </>
        ) : (
          <p>Select a memory to view details.</p>
        )}
      </div>
    </aside>
  );
};

export default MemoryPanel;
