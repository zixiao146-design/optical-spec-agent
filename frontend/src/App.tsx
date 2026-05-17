import { useMemo, useState } from "react";
import { API_BASE_URL } from "./api/client";
import { BoundaryBadge } from "./components/BoundaryBadge";
import { LanguageSwitcher } from "./components/LanguageSwitcher";
import { SafetyNotice } from "./components/SafetyNotice";
import { useI18n } from "./i18n/useI18n";
import { AdapterMatrixPage } from "./pages/AdapterMatrixPage";
import { AgentCollaborationPage } from "./pages/AgentCollaborationPage";
import { AgentCommandCenterPage } from "./pages/AgentCommandCenterPage";
import { ArtifactPreviewPage } from "./pages/ArtifactPreviewPage";
import { DashboardPage } from "./pages/DashboardPage";
import { EvidencePage } from "./pages/EvidencePage";
import { ExampleGalleryPage } from "./pages/ExampleGalleryPage";
import { MaterialLibraryPage } from "./pages/MaterialLibraryPage";
import { SpecInputPage } from "./pages/SpecInputPage";
import { SystemStatusPage } from "./pages/SystemStatusPage";
import { WorkflowPlanPage } from "./pages/WorkflowPlanPage";

const PAGES = [
  "Agent Command Center",
  "Dashboard",
  "Spec Input",
  "Example Gallery",
  "Adapter Matrix",
  "Material Library",
  "Workflow Plan",
  "Artifact Preview",
  "Agent Collaboration",
  "Validation Evidence",
  "System Status",
] as const;

type Page = (typeof PAGES)[number];

const PAGE_LABEL_KEYS: Record<Page, string> = {
  "Agent Command Center": "nav.agentCommandCenter",
  Dashboard: "nav.dashboard",
  "Spec Input": "nav.specInput",
  "Example Gallery": "nav.exampleGallery",
  "Adapter Matrix": "nav.adapterMatrix",
  "Material Library": "nav.materialLibrary",
  "Workflow Plan": "nav.workflowPlan",
  "Artifact Preview": "nav.artifactPreview",
  "Agent Collaboration": "nav.agentCollaboration",
  "Validation Evidence": "nav.validationEvidence",
  "System Status": "nav.systemStatus",
};

function pageComponent(page: Page, onNavigate: (page: Page) => void) {
  switch (page) {
    case "Agent Command Center":
      return <AgentCommandCenterPage />;
    case "Spec Input":
      return <SpecInputPage />;
    case "Example Gallery":
      return <ExampleGalleryPage />;
    case "Adapter Matrix":
      return <AdapterMatrixPage />;
    case "Material Library":
      return <MaterialLibraryPage />;
    case "Workflow Plan":
      return <WorkflowPlanPage />;
    case "Artifact Preview":
      return <ArtifactPreviewPage />;
    case "Agent Collaboration":
      return <AgentCollaborationPage />;
    case "Validation Evidence":
      return <EvidencePage />;
    case "System Status":
      return <SystemStatusPage />;
    default:
      return <DashboardPage onNavigate={onNavigate} />;
  }
}

export default function App() {
  const { t } = useI18n();
  const [activePage, setActivePage] = useState<Page>("Agent Command Center");
  const content = useMemo(() => pageComponent(activePage, setActivePage), [activePage]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">OSA</span>
          <div>
            <h1>Agent Studio</h1>
            <p>{t("app.brand.subtitle")}</p>
          </div>
        </div>
        <LanguageSwitcher />
        <nav aria-label={t("app.nav.label")}>
          {PAGES.map((page) => (
            <button
              type="button"
              key={page}
              className={page === activePage ? "active" : ""}
              onClick={() => setActivePage(page)}
              aria-current={page === activePage ? "page" : undefined}
            >
              {t(PAGE_LABEL_KEYS[page])}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span>{t("app.apiBase")}</span>
          <code>{API_BASE_URL}</code>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <span className="eyebrow">optical-spec-agent</span>
            <h2>{t(PAGE_LABEL_KEYS[activePage])}</h2>
          </div>
          <div className="boundary-row compact">
            <BoundaryBadge>{t("app.topbar.noSolver")}</BoundaryBadge>
            <BoundaryBadge>{t("app.topbar.noExternalLlm")}</BoundaryBadge>
            <BoundaryBadge tone="notice">{t("app.topbar.previewFirst")}</BoundaryBadge>
          </div>
        </header>
        <SafetyNotice compact />
        {content}
      </main>
    </div>
  );
}
