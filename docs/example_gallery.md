# Example Gallery

The Example Gallery makes bundled optical design workflows discoverable inside Agent Studio.

Current scope:
- Local optical design examples live under `examples/optical_design/`.
- The gallery uses `GET /api/examples` and `GET /api/examples/{example_id}`.
- Each example connects design goal, preview materials, suggested adapter, workflow focus, expected agent trace, and next actions.
- Examples are local preview workflows only.

Included example families:
- nanoparticle_plasmonics
- thin_film_coating
- waveguide_mode
- photonic_crystal_band
- dielectric_metasurface_preview
- lens_raytrace_preview

Workflow connection:
Example Gallery -> Load example -> Material suggestions -> Adapter recommendation -> Agent Trace Timeline -> Workflow plan -> Artifact preview -> Evidence -> Next action.

Calculator connection:
- `thin_film_coating` maps to thin-film spectrum and quarter-wave AR previews.
- `waveguide_mode` maps to waveguide V-number sweep and single-mode range previews.
- `lens_raytrace_preview` maps to paraxial two-lens relay preview.
- Gaussian beam goals map to Gaussian beam series/focus previews.
- Nanoparticle and metasurface examples remain material/adapter/workflow previews unless a scalar calculator is explicitly relevant.

Safety boundaries:
- No solver is executed by default.
- No external LLM is called by default.
- Material data is preview/design-assist only.
- Preview artifacts are not production-grade physical validation.
- Formal convergence proof is not claimed.
- The UI does not control PyPI/TestPyPI uploads, tags, or releases.
