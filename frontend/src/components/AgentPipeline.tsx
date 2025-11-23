import React from "react";

interface Props {
  runResult: any;
  loading: boolean;
}

const agents = [
  "orchestrator",
  "architect",
  "reviewer",
  "challenger",
  "coo",
  "scribe",
];

const AgentPipeline: React.FC<Props> = ({ runResult, loading }) => {
  const completedAgents = new Set(
    runResult?.agent_outputs?.map((a: any) => a.name.toLowerCase()) || []
  );

  return (
    <section className="pipeline-section">
      <h2>MFOS Agent Pipeline</h2>
      <div className="pipeline-row">
        {agents.map((a) => {
          const active = loading || completedAgents.has(a);
          return (
            <div key={a} className={`pipeline-node ${active ? "active" : ""}`}>
              <span className="node-dot" />
              <span className="node-label">{a.toUpperCase()}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default AgentPipeline;
