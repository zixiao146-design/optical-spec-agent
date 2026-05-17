import { useEffect, useMemo, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { MaterialSuggestionResponse, MaterialsResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { demoMaterialSuggestion, demoMaterials } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

const RELATED_EXAMPLES: Record<string, string[]> = {
  au: ["nanoparticle_plasmonics"],
  ag: ["nanoparticle_plasmonics"],
  sio2: ["nanoparticle_plasmonics", "thin_film_coating", "waveguide_mode", "photonic_crystal_band"],
  tio2: ["thin_film_coating", "dielectric_metasurface_preview"],
  al2o3: ["thin_film_coating"],
  si: ["waveguide_mode", "photonic_crystal_band", "dielectric_metasurface_preview"],
  si3n4: ["waveguide_mode", "dielectric_metasurface_preview"],
  gaas: ["photonic_crystal_band"],
  glass_bk7_preview: ["lens_raytrace_preview"],
  glass_fused_silica_preview: ["lens_raytrace_preview"],
  air: ["lens_raytrace_preview", "photonic_crystal_band"],
};

export function MaterialLibraryPage() {
  const { t } = useI18n();
  const [query, setQuery] = useState("");
  const [application, setApplication] = useState("nanoparticle plasmonics");
  const [materials, setMaterials] = useState<RemoteState<MaterialsResponse>>(INITIAL_LOADING_STATE);
  const [suggestion, setSuggestion] = useState<RemoteState<MaterialSuggestionResponse>>({ status: "idle" });

  useEffect(() => {
    let active = true;
    void agentApi.getMaterials().then((payload) => {
      if (active) setMaterials(stateFromPayload(payload, demoMaterials, t("materials.demo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const rows = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const all = materials.data?.materials || [];
    if (!needle) return all;
    return all.filter((item) => {
      const text = [
        item.material_id,
        item.display_name,
        item.category,
        item.optical_role,
        item.aliases.join(" "),
        item.common_use.join(" "),
      ].join(" ").toLowerCase();
      return text.includes(needle);
    });
  }, [materials.data?.materials, query]);

  async function suggest() {
    setSuggestion({ status: "loading", message: t("materials.suggestLoadingMessage") });
    const payload = await agentApi.suggestMaterials({ application });
    setSuggestion(stateFromPayload(payload, demoMaterialSuggestion, t("materials.suggestDemo")));
  }

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("materials.kicker")}</span>
          <h2>{t("materials.title")}</h2>
          <p>{t("materials.description")}</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("materials.badge.preview")}</BoundaryBadge>
          <BoundaryBadge>{t("materials.badge.noProduction")}</BoundaryBadge>
          <BoundaryBadge>{t("materials.badge.noNetwork")}</BoundaryBadge>
        </div>
      </section>

      <section className="page-panel">
        <h3>{t("materials.searchTitle")}</h3>
        <label htmlFor="material-search">{t("materials.searchLabel")}</label>
        <input
          id="material-search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="sio2, waveguide, plasmonics"
        />
      </section>

      <section className="page-panel">
        <h3>{t("materials.suggestTitle")}</h3>
        <label htmlFor="material-application">{t("materials.suggestLabel")}</label>
        <input
          id="material-application"
          value={application}
          onChange={(event) => setApplication(event.target.value)}
        />
        <button
          type="button"
          onClick={() => void suggest()}
          disabled={suggestion.status === "loading" || application.trim().length === 0}
        >
          {suggestion.status === "loading" ? t("materials.suggesting") : t("materials.suggestButton")}
        </button>
      </section>

      <section className="page-panel wide">
        {materials.status === "loading" ? <LoadingState label={t("materials.loading")} /> : null}
        {materials.status === "demo" ? <ApiDisconnectedNotice message={materials.message} /> : null}
        {materials.status === "error" && materials.error ? (
          <ErrorState message={materials.error.message} actions={materials.error.recommended_next_actions} />
        ) : null}
        {rows.length === 0 && materials.status !== "loading" ? (
          <EmptyState title={t("materials.emptyTitle")} message={t("materials.emptyMessage")} />
        ) : (
          <div className="material-grid" aria-label={t("materials.title")}>
            {rows.map((material) => (
              <article className="material-card" key={material.material_id}>
                <span>{material.category}</span>
                <h3>{material.display_name}</h3>
                <code>{material.material_id}</code>
                <p>{material.optical_role}</p>
                <p>{material.common_use.join(", ")}</p>
                <p>
                  <strong>{t("materials.relatedExamples")}:</strong>{" "}
                  {(RELATED_EXAMPLES[material.material_id] || [t("materials.relatedExamplesNone")]).join(", ")}
                </p>
                <BoundaryBadge>{t("materials.card.previewOnly")}</BoundaryBadge>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="page-panel wide">
        <h3>{t("materials.suggestionResult")}</h3>
        {suggestion.status === "idle" ? (
          <EmptyState title={t("materials.noSuggestionTitle")} message={t("materials.noSuggestionMessage")} />
        ) : null}
        {suggestion.status === "loading" ? <LoadingState label={t("materials.suggesting")} /> : null}
        {suggestion.status === "demo" ? <ApiDisconnectedNotice message={suggestion.message} /> : null}
        {suggestion.status === "error" && suggestion.error ? (
          <ErrorState message={suggestion.error.message} actions={suggestion.error.recommended_next_actions} />
        ) : null}
        {suggestion.data?.suggested_materials?.length ? (
          <ul className="compact-list">
            {suggestion.data.suggested_materials.map((item) => (
              <li key={item.material_id}>
                <strong>{item.display_name}</strong> <code>{item.material_id}</code>
                <span>{item.optical_role}</span>
                <span>{t("materials.usedInExamples")}: {(RELATED_EXAMPLES[item.material_id] || []).join(", ") || t("materials.relatedExamplesNone")}</span>
              </li>
            ))}
          </ul>
        ) : null}
      </section>

      <DiagnosticsPanel diagnostics={materials.data?.diagnostics || materials.error?.diagnostics} title={t("materials.diagnostics")} />
      <RecommendedActions actions={materials.data?.recommended_next_actions || materials.error?.recommended_next_actions} title={t("materials.actions")} />
      <JsonPanel title={t("materials.jsonTitle")} value={materials.data || materials.error || { status: materials.status }} />
      <JsonPanel title={t("materials.suggestionJsonTitle")} value={suggestion.data || suggestion.error || { status: suggestion.status }} />
    </div>
  );
}
