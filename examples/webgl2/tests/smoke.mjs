import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdir, stat, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const server = spawn(process.execPath, ["server.mjs"], { stdio: ["ignore", "pipe", "pipe"] });
let browser;

async function waitForServer() {
  for (let attempt = 0; attempt < 80; attempt += 1) {
    try {
      const response = await fetch("http://127.0.0.1:4173/");
      if (response.ok) return;
    } catch { /* server is still starting */ }
    await new Promise(resolve => setTimeout(resolve, 125));
  }
  throw new Error("The demo HTTP server did not start.");
}

function assertTarget(box, label, min = 44) {
  assert.ok(box, label + " has no measurable hit target.");
  assert.ok(box.width >= min && box.height >= min,
    label + " is smaller than the " + min + " CSS-pixel target: " + JSON.stringify(box));
}

try {
  await waitForServer();
  browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader"]
  });
  const artifactDir = fileURLToPath(new URL("../artifacts/", import.meta.url));
  await mkdir(artifactDir, { recursive: true });
  const pageErrors = [];

  const desktop = await browser.newPage({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 1 });
  desktop.on("pageerror", error => pageErrors.push(error.message));
  await desktop.goto("http://127.0.0.1:4173/?scene=midnight", { waitUntil: "networkidle" });
  await desktop.waitForFunction(() => document.documentElement.dataset.renderer === "webgl2-l2-l3", { timeout: 15000 });

  assert.equal(await desktop.locator("html").getAttribute("data-renderer"), "webgl2-l2-l3");
  assert.equal(await desktop.getByRole("button", { name: "Previous track" }).count(), 1);
  assert.equal(await desktop.getByRole("button", { name: "Next track" }).count(), 1);
  assert.equal(await desktop.getByRole("slider", { name: "Preview position" }).count(), 1);
  assert.equal(await desktop.getByRole("button", { name: "Connect the lens" }).count(), 1);

  for (const selector of ["#previous", "#play-toggle", "#next", "#morph-toggle"]) {
    assertTarget(await desktop.locator(selector).boundingBox(), selector);
  }
  assertTarget(await desktop.locator("#progress").boundingBox(), "#progress", 40);

  const morph = desktop.locator("#morph-toggle");
  await morph.click();
  assert.equal(await morph.getAttribute("aria-pressed"), "true");
  await desktop.waitForTimeout(450);
  await desktop.screenshot({ path: join(artifactDir, "webgl2-desktop-connected.png"), fullPage: true });
  await desktop.screenshot({ path: join(artifactDir, "webgl2-desktop.png"), fullPage: true });

  const play = desktop.locator("#play-toggle");
  await play.click();
  assert.equal(await play.getAttribute("aria-pressed"), "true");
  await desktop.locator("#progress").evaluate(element => {
    element.value = "72";
    element.dispatchEvent(new Event("input", { bubbles: true }));
  });
  assert.equal(await desktop.locator("#progress").inputValue(), "72");

  await desktop.locator("body").click({ position: { x: 2, y: 2 } });
  for (let index = 0; index < 6; index += 1) await desktop.keyboard.press("Tab");
  assert.equal(await desktop.evaluate(() => document.activeElement?.id), "morph-toggle",
    "Keyboard tab order must reach the morph action after the preceding controls.");
  const focusStyle = await morph.evaluate(element => {
    const style = getComputedStyle(element);
    return { outlineStyle: style.outlineStyle, outlineWidth: parseFloat(style.outlineWidth) };
  });
  assert.notEqual(focusStyle.outlineStyle, "none");
  assert.ok(focusStyle.outlineWidth >= 2, "Keyboard focus must have a visible outline.");

  // Isolate the frame-pacing window before opening the other capture pages.
  await desktop.evaluate(() => window.__liquidGlassResetMetrics());
  await desktop.waitForTimeout(3000);
  const desktopMetrics = await desktop.evaluate(() => window.__liquidGlassDiagnostics());
  assert.ok(desktopMetrics.frameSamples > 0, "Frame pacing samples must be collected.");
  assert.ok(desktopMetrics.averageFrameMs > 0);
  assert.ok(desktopMetrics.averageCpuSubmitMs >= 0);
  assert.ok(desktopMetrics.estimatedSceneTextureBytes > 0);
  assert.equal(desktopMetrics.gpuTimeMs, null,
    "GPU time is deliberately not inferred from JavaScript command-submission timing.");

  const matrix = [
    { name: "desktop-midnight", width: 1440, height: 960, dpr: 1, scene: "midnight" },
    { name: "tablet-bright", width: 768, height: 1024, dpr: 1, scene: "bright" },
    { name: "mobile-detailed", width: 390, height: 844, dpr: 2, scene: "detailed" },
    { name: "landscape-bright", width: 844, height: 390, dpr: 2, scene: "bright" }
  ];
  const captures = [];
  for (const scenario of matrix) {
    const page = await browser.newPage({
      viewport: { width: scenario.width, height: scenario.height },
      deviceScaleFactor: scenario.dpr,
      isMobile: scenario.width < 500,
      hasTouch: scenario.width < 500
    });
    page.on("pageerror", error => pageErrors.push(error.message));
    await page.goto("http://127.0.0.1:4173/?scene=" + scenario.scene, { waitUntil: "networkidle" });
    await page.waitForFunction(() => document.documentElement.dataset.renderer === "webgl2-l2-l3", { timeout: 15000 });
    const diagnostics = await page.evaluate(() => window.__liquidGlassDiagnostics());
    assert.equal(diagnostics.scene, scenario.scene);
    assert.equal(diagnostics.width, Math.floor(scenario.width * Math.min(scenario.dpr, 1.65)));
    assert.equal(diagnostics.height, Math.floor(scenario.height * Math.min(scenario.dpr, 1.65)));
    assert.ok(diagnostics.estimatedSceneTextureBytes > 0);
    assert.equal(diagnostics.drawCallsPerFrame, 2);
    if (scenario.scene === "bright") {
      const contrast = await page.evaluate(() => {
        const channels = value => (value.match(/[\d.]+/g) || []).map(Number);
        const luminance = rgb => {
          const values = rgb.map(value => {
            const channel = value / 255;
            return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
          });
          return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
        };
        const ratio = (a, b) => {
          const high = Math.max(luminance(a), luminance(b));
          const low = Math.min(luminance(a), luminance(b));
          return (high + 0.05) / (low + 0.05);
        };
        const panelStyle = getComputedStyle(document.querySelector("#glass-panel"));
        const bg = channels(panelStyle.backgroundColor);
        const alpha = bg.length >= 4 ? bg[3] : 1;
        const panelBg = bg.slice(0, 3);
        const panelColor = channels(getComputedStyle(document.querySelector("#panel-title")).color).slice(0, 3);
        const playColor = channels(getComputedStyle(document.querySelector("#play-toggle")).color).slice(0, 3);
        const exteriorColor = channels(getComputedStyle(document.querySelector(".stage-copy")).color).slice(0, 3);
        const backdrops = [[148,171,173], [240,232,199], [148,176,161]];
        const composite = backdrop => panelBg.map((channel, i) => channel * alpha + backdrop[i] * (1 - alpha));
        return {
          panelAlpha: alpha,
          panelContrast: Math.min(...backdrops.map(backdrop => ratio(panelColor, composite(backdrop)))),
          buttonContrast: Math.min(...backdrops.map(backdrop => ratio(playColor, composite(backdrop)))),
          exteriorContrast: Math.min(...backdrops.map(backdrop => ratio(exteriorColor, backdrop)))
        };
      });
      assert.ok(contrast.panelAlpha >= 0.78, "Bright-scene glass opacity is insufficient for readable foregrounds: " + JSON.stringify(contrast));
      assert.ok(contrast.panelContrast >= 4.5, "Bright-scene panel text contrast is below WCAG AA: " + JSON.stringify(contrast));
      assert.ok(contrast.buttonContrast >= 4.5, "Bright-scene button contrast is below WCAG AA: " + JSON.stringify(contrast));
      assert.ok(contrast.exteriorContrast >= 4.5, "Bright-scene exterior text contrast is below WCAG AA: " + JSON.stringify(contrast));
      await page.locator("html").evaluate(element => element.dataset.transparency = "reduced");
      const reduced = await page.locator("#glass-panel").evaluate(element => ({
        color: getComputedStyle(element).color,
        background: getComputedStyle(element).backgroundColor
      }));
      assert.equal(reduced.color, "rgb(16, 43, 67)");
      assert.equal(reduced.background, "rgb(248, 252, 255)");
      await page.locator("html").evaluate(element => delete element.dataset.transparency);
    }
    await page.screenshot({ path: join(artifactDir, scenario.name + ".png"), fullPage: true });
    if (scenario.name === "mobile-detailed") {
      await page.screenshot({ path: join(artifactDir, "webgl2-mobile.png"), fullPage: true });
    }
    captures.push({ ...scenario, diagnostics });
    await page.close();
  }

  const fallbackL1 = await browser.newPage({ viewport: { width: 960, height: 720 } });
  await fallbackL1.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      if (type === "webgl2") return null;
      return original.call(this, type, ...args);
    };
  });
  await fallbackL1.goto("http://127.0.0.1:4173/", { waitUntil: "networkidle" });
  assert.equal(await fallbackL1.locator("html").getAttribute("data-renderer"), "css-l1");
  assert.match(await fallbackL1.locator("#renderer-status").textContent(), /L1 BLUR/);
  const l1Filter = await fallbackL1.locator("#glass-panel").evaluate(element => getComputedStyle(element).backdropFilter);
  assert.match(l1Filter, /blur\(18px\)/);
  await fallbackL1.screenshot({ path: join(artifactDir, "webgl2-fallback-l1.png"), fullPage: true });

  const fallbackL0 = await browser.newPage({ viewport: { width: 960, height: 720 } });
  await fallbackL0.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function (type, ...args) {
      if (type === "webgl2") return null;
      return original.call(this, type, ...args);
    };
    const supports = CSS.supports.bind(CSS);
    Object.defineProperty(CSS, "supports", {
      configurable: true,
      value: (property, value) => property === "backdrop-filter" ? false : supports(property, value)
    });
  });
  await fallbackL0.goto("http://127.0.0.1:4173/", { waitUntil: "networkidle" });
  assert.equal(await fallbackL0.locator("html").getAttribute("data-renderer"), "css-l0");
  assert.match(await fallbackL0.locator("#renderer-status").textContent(), /L0/);
  const l0Filter = await fallbackL0.locator("#glass-panel").evaluate(element => getComputedStyle(element).backdropFilter);
  assert.equal(l0Filter, "none", "L0 must not accidentally keep the browser's backdrop blur effect.");
  await fallbackL0.screenshot({ path: join(artifactDir, "webgl2-fallback-l0.png"), fullPage: true });

  const accessibility = await browser.newPage({ viewport: { width: 1024, height: 768 } });
  await accessibility.emulateMedia({ reducedMotion: "reduce", contrast: "more" });
  await accessibility.goto("http://127.0.0.1:4173/?scene=midnight", { waitUntil: "networkidle" });
  await accessibility.waitForFunction(() => document.documentElement.dataset.renderer === "webgl2-l2-l3");
  const accessibleMorph = accessibility.locator("#morph-toggle");
  await accessibleMorph.click();
  await accessibility.waitForFunction(() => {
    const value = window.__liquidGlassDiagnostics?.();
    return value && value.morph === 1 && value.morphTarget === 1;
  });
  let accessibilityStyles = await accessibility.locator("#glass-panel").evaluate(element => {
    const style = getComputedStyle(element);
    return { background: style.backgroundColor, borderWidth: parseFloat(style.borderTopWidth),
      reducedMotion: matchMedia("(prefers-reduced-motion: reduce)").matches,
      increasedContrast: matchMedia("(prefers-contrast: more)").matches };
  });
  assert.equal(accessibilityStyles.reducedMotion, true);
  assert.equal(accessibilityStyles.increasedContrast, true);
  assert.ok(accessibilityStyles.borderWidth >= 2);
  assert.match(accessibilityStyles.background, /rgba\(.+,\s*0\.97\)/);

  await accessibility.emulateMedia({ reducedMotion: "no-preference", contrast: "no-preference" });
  await accessibility.locator("html").evaluate(element => element.dataset.transparency = "reduced");
  const reducedTransparency = await accessibility.locator("#glass-panel").evaluate(element => {
    const style = getComputedStyle(element);
    return { background: style.backgroundColor, backdropFilter: style.backdropFilter };
  });
  assert.equal(reducedTransparency.background, "rgb(8, 13, 29)");
  assert.equal(reducedTransparency.backdropFilter, "none");

  await accessibility.emulateMedia({ forcedColors: "active" });
  assert.equal(await accessibility.evaluate(() => matchMedia("(forced-colors: active)").matches), true);
  assert.equal(await accessibility.getByRole("button", { name: "Separate the lens" }).count(), 1);
  await accessibility.screenshot({ path: join(artifactDir, "webgl2-accessibility-fallback.png"), fullPage: true });
  await fallbackL1.close();
  await fallbackL0.close();

  if (pageErrors.length) throw new Error("Browser errors: " + pageErrors.join(" | "));
  const report = {
    schemaVersion: 1,
    environment: "headless Chromium + SwiftShader; CPU timings are command-submission timings, not GPU execution timings",
    visualMatrix: captures,
    desktopRuntime: desktopMetrics,
    accessibility: {
      keyboardFocus: focusStyle,
      reducedMotionAndContrast: accessibilityStyles,
      reducedTransparency: reducedTransparency,
      forcedColors: true
    },
    fallbackCoverage: ["CSS L1 backdrop-blur fallback", "L0 translucent fallback"],
    limitations: [
      "SwiftShader/headless browser results are not physical-GPU performance evidence.",
      "Scene texture bytes estimate one RGBA8 off-screen texture and exclude driver allocations and browser compositor memory.",
      "GPU execution time is not measured by the JavaScript CPU-submit timer."
    ]
  };
  await writeFile(join(artifactDir, "webgl2-validation-matrix.json"), JSON.stringify(report, null, 2) + "\n");

  for (const scenario of matrix) {
    const info = await stat(join(artifactDir, scenario.name + ".png"));
    assert.ok(info.size > 12000, "Screenshot is unexpectedly small: " + scenario.name);
  }
  process.stdout.write("PASS: WebGL2 L2/L3, semantics, 44px hit targets, keyboard focus, reduced motion, increased contrast, reduced transparency, forced colors, 4 visual scenarios, and CPU/memory diagnostics verified.\n");
} finally {
  if (browser) await browser.close();
  server.kill("SIGTERM");
}
