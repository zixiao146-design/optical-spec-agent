import type { PermissionGate } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";
import { EmptyState } from "./EmptyState";

interface PermissionGatePanelProps {
  gates: PermissionGate[];
}

function toneFor(status: PermissionGate["status"]) {
  return status === "allowed" ? "safe" : "notice";
}

export function PermissionGatePanel({ gates }: PermissionGatePanelProps) {
  const { language, t } = useI18n();

  return (
    <section className="page-panel wide">
      <h3>{t("commandCenter.permissionGates")}</h3>
      <p className="inline-boundary">{t("commandCenter.permissionIntro")}</p>
      {gates.length === 0 ? (
        <EmptyState title={t("commandCenter.noGatesTitle")} message={t("commandCenter.noGatesMessage")} />
      ) : (
        <div className="permission-grid">
          {gates.map((gate) => (
            <article className="permission-card" key={gate.gate_id}>
              <div className="timeline-heading">
                <h4>{language === "zh-CN" ? gate.label_zh : gate.label}</h4>
                <BoundaryBadge tone={toneFor(gate.status)}>
                  {t(`permission.${gate.status}`)}
                </BoundaryBadge>
              </div>
              <p>{gate.reason}</p>
              <dl className="timeline-details">
                <dt>{t("commandCenter.riskLevel")}</dt>
                <dd>{gate.risk_level}</dd>
                <dt>{t("commandCenter.defaultAllowed")}</dt>
                <dd>{gate.default_allowed ? t("permission.allowed") : t("permission.blocked")}</dd>
              </dl>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
