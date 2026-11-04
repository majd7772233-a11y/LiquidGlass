import { spawn } from "node:child_process";
import { mkdir, stat } from "node:fs/promises";
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

try {
  await waitForServer();
  browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-dev-shm-usage", "--enable-webgl", "--use-gl=angle", "--use-angle=swiftshader"]
  });
  await mkdir(new URL("../artifacts/", import.meta.url), { recursive: true });

  const desktop = await browser.newPage({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 1 });
  const pageErrors = [];
  desktop.on("pageerror", error => pageErrors.push(error.message));
  await desktop.goto("http://127.0.0.1:4173/", { waitUntil: "networkidle" });
  await desktop.waitForFunction(() => document.documentElement.dataset.renderer === "webgl2-l2-l3", { timeout: 15000 });

  const renderer = await desktop.locator("html").getAttribute("data-renderer");
  if (renderer !== "webgl2-l2-l3") throw new Error("The demo did not initialize its WebGL2 renderer.");

  const morph = desktop.locator("#morph-toggle");
  await morph.click();
  if (await morph.getAttribute("aria-pressed") !== "true") throw new Error("The organic lens control did not enter its connected state.");
  await desktop.waitForTimeout(450);
  await desktop.screenshot({ path: new URL("../artifacts/webgl2-desktop.png", import.meta.url), fullPage: true });

  const play = desktop.locator("#play-toggle");
  await play.click();
  if (await play.getAttribute("aria-pressed") !== "true") throw new Error("The play/pause control did not update its semantic state.");
  await desktop.locator("#progress").fill("72");
  if (await desktop.locator("#progress").inputValue() !== "72") throw new Error("The timeline slider did not accept input.");

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  await mobile.goto("http://127.0.0.1:4173/", { waitUntil: "networkidle" });
  await mobile.waitForFunction(() => document.documentElement.dataset.renderer === "webgl2-l2-l3", { timeout: 15000 });
  await mobile.screenshot({ path: new URL("../artifacts/webgl2-mobile.png", import.meta.url), fullPage: true });

  if (pageErrors.length) throw new Error("Browser errors: " + pageErrors.join(" | "));
  for (const path of ["../artifacts/webgl2-desktop.png", "../artifacts/webgl2-mobile.png"]) {
    const info = await stat(new URL(path, import.meta.url));
    if (info.size < 12000) throw new Error("Screenshot is unexpectedly small: " + path);
  }
  process.stdout.write("PASS: WebGL2 initialized; owned-backdrop L2/L3 renderer, morph control, playback state, slider, and desktop/mobile captures verified.\n");
} finally {
  if (browser) await browser.close();
  server.kill("SIGTERM");
}
