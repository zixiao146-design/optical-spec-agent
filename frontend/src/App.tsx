import { useMemo, useState } from "react";
import { API_BASE_URL } from "./api/client";
import { BoundaryBadge } from "./components/BoundaryBadge";
import { SafetyNotice } from "./components/SafetyNotice";
import { AdapterMatrixPage } from "./pages/AdapterMatrixPage";
import { ArtifactPreviewPage } from "./pages/ArtifactPreviewPage";
import { DashboardPage } from "./pages/DashboardPage";
import { EvidencePage } from "./pages/EvidencePage";
import { SpecInputPage } from "./pages/SpecInputPage";
import { SystemStatusPage } from "./pages/SystemStatusPage";
import { WorkflowPlanPage } from "./pages/WorkflowPlanPage";

const PAGES = [
  "Dashboard",
  "Spec Input",
  "Adapter Matrix",
  "Workflow Plan",
  "Artifact Preview",
  "Validation Evidence",
  "System Status",
] as const;

type Page = (typeof PAGES)[number];

function pageComponent(page: Page) {
  switch (page) {
    case "Spec Input":
      return <SpecInputPage />;
    case "Adapter Matrix":
      return <AdapterMatrixPage />;
    case "Workflow Plan":
      return <WorkflowPlanPage />;
    case "Artifact Preview":
      return <ArtifactPreviewPage />;
    case "Validation Evidence":
      return <EvidencePage />;
    case "System Status":
      return <SystemStatusPage />;
    default:
      return <DashboardPage />;
  }
}

export default function App() {
  const [activePage, setActivePage] = useState<Page>("Dashboard");
  const content = useMemo(() => pageComponent(activePage), [activePage]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">OSA</span>
          <div>
            <h1>Agent Studio</h1>
            <p>Local MVP</p>
          </div>
        </div>
        <nav aria-label="Agent Studio sections">
          {PAGES.map((page) => (
            <button
              type="button"
              key={page}
              className={page === activePage ? "active" : ""}
              onClick={() => setActivePage(page)}
              aria-current={page === activePage ? "page" : undefined}
            >
              {page}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span>API base</span>
          <code>{API_BASE_URL}</code>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <span className="eyebrow">optical-spec-agent</span>
            <h2>{activePage}</h2>
          </div>
          <div className="boundary-row compact">
            <BoundaryBadge>No solver run</BoundaryBadge>
            <BoundaryBadge>No external LLM</BoundaryBadge>
            <BoundaryBadge tone="notice">Preview-first</BoundaryBadge>
          </div>
        </header>
        <SafetyNotice compact />
        {content}
      </main>
    </div>
  );
}
