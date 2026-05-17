import { expect, test, type Page } from "@playwright/test";

const LOCAL_HOSTS = new Set(["127.0.0.1", "localhost"]);

const pages = [
  { nav: "Dashboard", heading: "Local Agent API workbench" },
  { nav: "Spec Input", heading: "Parse and validate local optical specs" },
  { nav: "Example Gallery", heading: "Optical design example gallery" },
  { nav: "Adapter Matrix", heading: "Adapter maturity and evidence" },
  { nav: "Material Library", heading: "Local preview material catalog" },
  { nav: "Workflow Plan", heading: "Generate a synchronous local workflow preview" },
  { nav: "Artifact Preview", heading: "Generate solver-native preview content" },
  { nav: "Agent Collaboration", heading: "Agent Trace Timeline" },
  { nav: "Validation Evidence", heading: "Evidence and limitations" },
  { nav: "System Status", heading: "Local API contract and schema" },
];

async function blockExternalNetwork(page: Page) {
  await page.route("**/*", async (route) => {
    const url = route.request().url();
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      await route.continue();
      return;
    }
    const host = new URL(url).hostname;
    if (LOCAL_HOSTS.has(host)) {
      await route.continue();
      return;
    }
    await route.abort("blockedbyclient");
  });
}

async function expectForbiddenControlsAbsent(page: Page) {
  for (const label of [
    /Upload to PyPI/i,
    /Upload to TestPyPI/i,
    /Create tag/i,
    /Create release/i,
    /Run solver/i,
    /External LLM/i,
  ]) {
    await expect(page.getByRole("button", { name: label })).toHaveCount(0);
  }
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    window.localStorage.setItem("agent-studio-language", "en");
  });
  await blockExternalNetwork(page);
});

test("major Agent Studio pages render in local visual smoke", async ({ page }) => {
  await page.goto("/");

  for (const entry of pages) {
    await page.getByRole("button", { name: entry.nav }).click();
    await expect(page.getByRole("heading", { name: entry.heading, exact: true }).first()).toBeVisible();
    await expect(page.getByRole("main")).toContainText(entry.nav);
    await expectForbiddenControlsAbsent(page);
  }
});

test("safety notices remain visible and conservative", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("No solver is executed by default.").first()).toBeVisible();
  await expect(page.getByText("No external LLM is called by default.").first()).toBeVisible();
  await expect(
    page.getByText("Preview artifacts are not production-grade physical validation.").first(),
  ).toBeVisible();
  await expect(page.getByText("Formal convergence proof is not claimed.").first()).toBeVisible();
  await expect(
    page.getByText("This UI does not control PyPI/TestPyPI publication or GitHub releases.").first(),
  ).toBeVisible();
  await expectForbiddenControlsAbsent(page);
});

test("fixture-backed interactions are visible without solver or LLM controls", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Spec Input" }).click();
  await expect(page.getByRole("button", { name: "Load example spec" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Load fixture" })).toBeVisible();
  await expect(page.getByText("Demo fixture loaded", { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Workflow Plan" }).click();
  await expect(page.getByRole("button", { name: "Load workflow fixture" })).toBeVisible();
  await expect(page.locator(".inline-boundary", { hasText: "No solver is executed by default." })).toBeVisible();

  await page.getByRole("button", { name: "Artifact Preview" }).click();
  await expect(page.getByRole("button", { name: "Load minimal spec" })).toBeVisible();
  await expect(
    page.locator(".inline-boundary", {
      hasText: "Preview-only artifact. No solver is executed by default.",
    }),
  ).toBeVisible();

  await page.getByRole("button", { name: "Material Library" }).click();
  await expect(page.getByText("not production-grade optical constants").first()).toBeVisible();
  await expect(page.getByRole("button", { name: "Suggest materials" })).toBeVisible();

  await page.getByRole("button", { name: "Example Gallery" }).click();
  await expect(page.locator("button", { hasText: "Load example" }).first()).toBeVisible();
  await expect(page.locator("button", { hasText: "View agent trace" }).first()).toBeVisible();

  await page.getByRole("button", { name: "Agent Collaboration" }).click();
  await expect(page.getByRole("button", { name: "Load nanoparticle agent trace" })).toBeVisible();
  await expect(page.getByText("does not call an external LLM").first()).toBeVisible();

  await expectForbiddenControlsAbsent(page);
});
