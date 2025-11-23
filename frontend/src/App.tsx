import React, { useState } from "react";
import axios from "axios";
import AgentPipeline from "./components/AgentPipeline";
import AgentOutputPanels from "./components/AgentOutputPanels";
import MemoryPanel from "./components/MemoryPanel";

interface AgentOutput {
  name: string;
  content: string;
  metadata?: any;
}

interface BrainRunResponse {
  prompt: string;
  agent_outputs: AgentOutput[];
  final_output: string;
  memory_entry_id?: string;
}

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const App: React.FC = () => {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [runResult, setRunResult] = useState<BrainRunResponse | null>(null);

  const handleRun = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post<BrainRunResponse>(`${API_BASE}/api/run-brain`, {
        prompt,
      });
      setRunResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error running MFOS Brain. Check console.");
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (text: string) => {
    setPrompt(text);
  };

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="orb" />
        <div>
          <h1>MFOS BRAIN (V1 DEMO)</h1>
          <p>Synthetic COO • Multi-Agent Intelligence • Self-Expanding Blueprint</p>
        </div>
      </header>

      <section className="prompt-section">
        <textarea
          placeholder='Enter a request for the MFOS Brain… e.g. "Design PRM compensation v1"'
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <div className="prompt-buttons">
          <button onClick={handleRun} disabled={loading}>
            {loading ? "Running…" : "Run MFOS Brain"}
          </button>
          <button onClick={() => loadExample("Design PRM compensation v1 for MFOS.")}>
            Load Example: PRM Comp
          </button>
          <button onClick={() => loadExample("Architect the vendor mesh MVP for MFOS.")}>
            Load Example: Vendor Mesh MVP
          </button>
        </div>
      </section>

      <AgentPipeline runResult={runResult} loading={loading} />

      <div className="main-content">
        <AgentOutputPanels runResult={runResult} />
        <MemoryPanel apiBase={API_BASE} />
      </div>
    </div>
  );
};

export default App;
