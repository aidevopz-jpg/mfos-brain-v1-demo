import React, { useState } from "react";

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

interface Props {
  runResult: BrainRunResponse | null;
}

const AgentOutputPanels: React.FC<Props> = ({ runResult }) => {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({});

  if (!runResult) {
    return (
      <section className="agent-output-section">
        <p>No MFOS Brain run yet. Enter a request and click "Run MFOS Brain".</p>
      </section>
    );
  }

  const toggle = (key: string) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const outputsByName: Record<string, AgentOutput[]> = {};
  for (const out of runResult.agent_outputs) {
    const key = out.name.toLowerCase();
    if (!outputsByName[key]) outputsByName[key] = [];
    outputsByName[key].push(out);
  }

  const ordered = [
    "orchestrator",
    "architect",
    "reviewer",
    "challenger",
    "coo",
    "scribe",
    "orchestrator_final",
  ];

  return (
    <section className="agent-output-section">
      <h2>Agent Outputs</h2>
      {ordered.map((key) => {
        const items = outputsByName[key];
        if (!items || items.length === 0) return null;
        const label =
          key === "orchestrator_final"
            ? "ORCHESTRATOR FINAL"
            : key.toUpperCase();
        const isOpen = openSections[key] ?? true;
        return (
          <div key={key} className="agent-card">
            <div className="agent-card-header" onClick={() => toggle(key)}>
              <span>{label}</span>
              <span>{isOpen ? "\u25BE" : "\u25B8"}</span>
            </div>
            {isOpen && (
              <div className="agent-card-body">
                {items.map((item, idx) => (
                  <pre key={idx}>{item.content}</pre>
                ))}
              </div>
            )}
          </div>
        );
      })}
      <div className="agent-card">
        <div className="agent-card-header">
          <span>FINAL INTEGRATED BLUEPRINT (SCRIBE)</span>
        </div>
        <div className="agent-card-body">
          <pre>{runResult.final_output}</pre>
        </div>
      </div>
    </section>
  );
};

export default AgentOutputPanels;
