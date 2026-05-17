import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

export function QuickstartPanel() {
  const { t } = useI18n();
  return (
    <section className="quickstart-success" aria-label={t("quickstartSuccess.title")}>
      <div className="page-title">
        <span>{t("quickstartSuccess.kicker")}</span>
        <h3>{t("quickstartSuccess.title")}</h3>
        <p>
          {t("quickstartSuccess.description")}
        </p>
      </div>
      <ul className="check-list">
        <li>{t("quickstartSuccess.apiConnected")}</li>
        <li>{t("quickstartSuccess.packageVersion")}</li>
        <li>{t("quickstartSuccess.apiContract")}</li>
        <li>{t("quickstartSuccess.spec")}</li>
        <li>{t("quickstartSuccess.workflow")}</li>
        <li>{t("quickstartSuccess.preview")}</li>
        <li>{t("quickstartSuccess.evidence")}</li>
        <li>{t("quickstartSuccess.nextAction")}</li>
      </ul>
      <div className="boundary-row">
        <BoundaryBadge>{t("quickstartSuccess.badge.noSolver")}</BoundaryBadge>
        <BoundaryBadge>{t("quickstartSuccess.badge.noLlm")}</BoundaryBadge>
        <BoundaryBadge tone="notice">{t("quickstartSuccess.badge.preview")}</BoundaryBadge>
      </div>
    </section>
  );
}
