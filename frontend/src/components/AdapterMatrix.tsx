import type { AdapterSummary, ValidationEvidenceItem } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

interface AdapterMatrixProps {
  adapters: AdapterSummary[];
  evidence: ValidationEvidenceItem[];
}

export function AdapterMatrix({ adapters, evidence }: AdapterMatrixProps) {
  const { t } = useI18n();
  const evidenceByTool = new Map(evidence.map((item) => [item.tool_name, item]));
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t("adapters.table.adapter")}</th>
            <th>{t("adapters.table.family")}</th>
            <th>{t("adapters.table.status")}</th>
            <th>{t("adapters.table.maturity")}</th>
            <th>{t("adapters.table.boundary")}</th>
          </tr>
        </thead>
        <tbody>
          {adapters.map((adapter) => {
            const item = evidenceByTool.get(adapter.tool_name);
            return (
              <tr key={adapter.tool_name}>
                <td>
                  <strong>{adapter.display_name}</strong>
                  <span>{adapter.tool_name}</span>
                </td>
                <td>{adapter.solver_family}</td>
                <td>{adapter.current_status}</td>
                <td>{item?.maturity_level || adapter.maturity_level}</td>
                <td>
                  <BoundaryBadge>{t("adapters.table.noSolver")}</BoundaryBadge>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
