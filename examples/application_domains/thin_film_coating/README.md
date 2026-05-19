# Thin-film coating

Design domain: `thin_film_coating`

Natural-language goal:

- EN: Create a local preview for thin-film coating with no external solver execution.
- ZH: 为薄膜镀膜创建本地预览，不运行外部求解器。

Materials: sio2, tio2, al2o3, glass_bk7_preview

Linked requirement templates: thin_film_ar_coating

Expected calculators: optics.thin_film.spectrum, optics.thin_film.quarter_wave_ar

Expected adapters: preview-only TMM calculator path

Missing-input questions:

- What substrate and target wavelength should the coating optimize?
- Is normal incidence acceptable for the preview?

Evidence boundary: Sanity-checked thin-film preview calculator; not production-grade coating validation.

This case is preview/design-assist only. It performs no solver execution, calls no external LLM, performs no network material database lookup, and claims no production-grade physical validation or formal convergence proof.
