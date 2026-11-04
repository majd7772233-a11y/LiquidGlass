const canvas = document.querySelector("#scene");
const panel = document.querySelector("#glass-panel");
const status = document.querySelector("#renderer-status");
const morphButton = document.querySelector("#morph-toggle");
const morphLabel = morphButton.querySelector(".morph-label");
const playButton = document.querySelector("#play-toggle");
const playGlyph = playButton.querySelector(".play-glyph");
const playLabel = playButton.querySelector(".play-label");
const progress = document.querySelector("#progress");
const elapsed = document.querySelector("#elapsed");
const previous = document.querySelector("#previous");
const next = document.querySelector("#next");

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const gl = canvas.getContext("webgl2", {
  alpha: false,
  antialias: true,
  depth: false,
  stencil: false,
  powerPreference: "high-performance",
  preserveDrawingBuffer: true
});

if (!gl) {
  document.documentElement.classList.add("no-webgl");
  document.documentElement.dataset.renderer = "css-l1";
  const blurAvailable = window.CSS && CSS.supports("backdrop-filter", "blur(1px)");
  document.documentElement.dataset.renderer = blurAvailable ? "css-l1" : "css-l0";
  status.textContent = blurAvailable ? "CSS FALLBACK · L1 BLUR · NO REFRACTION" : "TRANSLUCENT FALLBACK · L0";
} else {
  startRenderer(gl);
}

function startRenderer(context) {
  const vertexSource = `#version 300 es
  in vec2 aPosition;
  in vec2 aTexCoord;
  out vec2 vUv;
  void main() {
    vUv = aTexCoord;
    gl_Position = vec4(aPosition, 0.0, 1.0);
  }`;

  const backgroundSource = `#version 300 es
  precision highp float;
  in vec2 vUv;
  out vec4 outColor;
  uniform vec2 uResolution;
  uniform float uTime;

  float softRing(float d, float width) {
    return 1.0 - smoothstep(width, width + 0.006, abs(d));
  }

  void main() {
    vec2 uv = vUv;
    float aspect = uResolution.x / max(uResolution.y, 1.0);
    vec2 p = (uv - 0.5) * vec2(aspect, 1.0);
    float t = uTime;

    vec3 deep = vec3(0.015, 0.035, 0.085);
    vec3 blue = vec3(0.08, 0.18, 0.34);
    vec3 violet = vec3(0.24, 0.13, 0.34);
    vec3 color = mix(deep, blue, smoothstep(-0.55, 0.58, p.y));
    color = mix(color, violet, (1.0 - smoothstep(-0.55, 0.72, p.x + 0.35 * p.y)) * 0.43);

    vec2 gridUv = uv * vec2(19.0, 13.0);
    vec2 gridCell = abs(fract(gridUv) - 0.5);
    float gridLine = 1.0 - smoothstep(0.478, 0.493, max(gridCell.x, gridCell.y));
    color += gridLine * vec3(0.055, 0.105, 0.17);

    float scan = softRing(p.y - 0.12 * sin(p.x * 3.2 + t * 0.24), 0.0025);
    color += scan * vec3(0.13, 0.27, 0.38) * 0.8;

    vec2 orbitA = p - vec2(-0.34 + 0.055 * sin(t * 0.22), 0.13);
    float ringA = softRing(length(orbitA) - 0.19, 0.0035);
    color += ringA * vec3(0.16, 0.65, 0.82) * 0.65;

    vec2 orbitB = p - vec2(0.33, -0.18 + 0.045 * cos(t * 0.18));
    float ringB = softRing(length(orbitB) - 0.27, 0.0028);
    color += ringB * vec3(0.72, 0.37, 0.91) * 0.72;

    float crossLine = 1.0 - smoothstep(0.0015, 0.006, abs(p.x + 0.11 * sin(t * 0.15)));
    color += crossLine * vec3(0.055, 0.11, 0.16) * 0.25;

    vec2 lightA = p - vec2(-0.22, 0.32 + 0.035 * sin(t * 0.31));
    float glowA = exp(-dot(lightA, lightA) * 5.2);
    vec2 lightB = p - vec2(0.48, -0.31 + 0.045 * cos(t * 0.25));
    float glowB = exp(-dot(lightB, lightB) * 7.0);
    color += glowA * vec3(0.12, 0.32, 0.52) + glowB * vec3(0.34, 0.14, 0.48);

    float vignette = (1.0 - smoothstep(0.12, 1.18, length(p * vec2(0.78, 1.1))));
    color *= 0.72 + 0.28 * vignette;
    outColor = vec4(color, 1.0);
  }`;

  const glassSource = `#version 300 es
  precision highp float;
  in vec2 vUv;
  out vec4 outColor;
  uniform sampler2D uScene;
  uniform vec2 uResolution;
  uniform vec4 uLensRect;
  uniform float uMorph;
  uniform float uStrength;
  uniform vec2 uPointer;

  float sdRoundBox(vec2 p, vec2 b, float r) {
    vec2 q = abs(p) - b + vec2(r);
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
  }

  float smoothUnion(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / max(k, 0.001), 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
  }

  float lensDistance(vec2 p) {
    float halfW = max(20.0, uLensRect.z * 0.5 - 2.0);
    float halfH = max(20.0, uLensRect.w * 0.5 - 2.0);
    float radius = min(halfH * 0.44, 42.0);
    float body = sdRoundBox(p, vec2(halfW, halfH), radius);
    if (uMorph < 0.001) return body;

    float lobeRadius = min(halfH * 0.40, halfW * 0.19) * uMorph;
    vec2 lobeCenter = vec2(halfW * 0.91, -halfH * 0.48);
    float lobe = length(p - lobeCenter) - lobeRadius;
    return smoothUnion(body, lobe, max(1.0, lobeRadius * 0.72));
  }

  void main() {
    vec2 uv = vUv;
    vec3 original = texture(uScene, uv).rgb;

    vec2 center = vec2(
      uLensRect.x + uLensRect.z * 0.5,
      uResolution.y - (uLensRect.y + uLensRect.w * 0.5)
    );
    vec2 p = gl_FragCoord.xy - center;
    float d = lensDistance(p);
    float mask = 1.0 - smoothstep(-1.4, 1.4, d);

    float e = 1.65;
    vec2 gradient = vec2(
      lensDistance(p + vec2(e, 0.0)) - lensDistance(p - vec2(e, 0.0)),
      lensDistance(p + vec2(0.0, e)) - lensDistance(p - vec2(0.0, e))
    );
    vec2 normal = length(gradient) > 0.001 ? normalize(gradient) : vec2(0.0, 1.0);

    float edge = exp(-abs(d) * 0.075);
    float body = 1.0 - smoothstep(0.0, 95.0, -d);
    vec2 pointerInfluence = (uPointer - 0.5) * 2.0;
    vec2 offsetPx = normal * uStrength * (3.5 + 15.0 * edge + 3.0 * body);
    offsetPx += pointerInfluence * body * 1.6;
    vec2 offsetUv = offsetPx / uResolution;

    vec3 refracted = texture(uScene, clamp(uv + offsetUv, 0.002, 0.998)).rgb;
    vec2 dispersion = normal * (1.2 / uResolution);
    float red = texture(uScene, clamp(uv + offsetUv + dispersion, 0.002, 0.998)).r;
    float blue = texture(uScene, clamp(uv + offsetUv - dispersion, 0.002, 0.998)).b;
    refracted = vec3(red, refracted.g, blue);

    vec2 lightDirection = normalize(vec2(-0.48, 0.86) + pointerInfluence * 0.11);
    float fresnel = pow(1.0 - abs(dot(normal, lightDirection)), 3.2);
    float rim = edge * (0.22 + 0.48 * fresnel);
    float specular = pow(max(dot(normal, lightDirection), 0.0), 13.0) * edge * 0.50;
    float broadHighlight = exp(-pow((p.y - uLensRect.w * 0.27) / max(18.0, uLensRect.w * 0.22), 2.0)) * mask;

    vec3 glass = mix(original, refracted, 0.91);
    glass = mix(glass, glass * vec3(0.88, 0.96, 1.045) + vec3(0.018, 0.026, 0.045), 0.13);
    glass += vec3(0.52, 0.79, 1.0) * rim * 0.27;
    glass += vec3(0.86, 0.95, 1.0) * specular;
    glass += vec3(0.44, 0.73, 0.92) * broadHighlight * 0.06;

    outColor = vec4(mix(original, glass, mask), 1.0);
  }`;

  let backgroundProgram;
  let glassProgram;
  let sceneTexture;
  let framebuffer;
  let buffer;
  let width = 1;
  let height = 1;
  let pixelRatio = 1;
  let morph = 0;
  let morphTarget = 0;
  let strength = 1;
  let pointer = [0.5, 0.5];
  let playing = false;
  let progressValue = Number(progress.value);
  let startedAt = performance.now();
  let lastFrame = startedAt;
  let progressOrigin = startedAt;
  let frameId = 0;

  try {
    backgroundProgram = createProgram(context, vertexSource, backgroundSource);
    glassProgram = createProgram(context, vertexSource, glassSource);
    buffer = context.createBuffer();
    context.bindBuffer(context.ARRAY_BUFFER, buffer);
    context.bufferData(context.ARRAY_BUFFER, new Float32Array([
      -1, -1, 0, 0,
       1, -1, 1, 0,
      -1,  1, 0, 1,
       1,  1, 1, 1
    ]), context.STATIC_DRAW);
    sceneTexture = context.createTexture();
    framebuffer = context.createFramebuffer();
    resize();
    document.documentElement.dataset.renderer = "webgl2-l2-l3";
    status.textContent = "WEBGL2 · OWNED SCENE TEXTURE · L2 / L3";
    status.title = "The lens samples and displaces the application-owned background texture.";
  } catch (error) {
    console.error(error);
    document.documentElement.classList.add("no-webgl");
    document.documentElement.dataset.renderer = "css-l1";
    const blurAvailable = window.CSS && CSS.supports("backdrop-filter", "blur(1px)");
    document.documentElement.dataset.renderer = blurAvailable ? "css-l1" : "css-l0";
    status.textContent = blurAvailable ? "CSS FALLBACK · L1 BLUR · REFRACTION UNAVAILABLE" : "TRANSLUCENT FALLBACK · L0";
    return;
  }

  function createProgram(glContext, vertexText, fragmentText) {
    const compile = (type, source) => {
      const shader = glContext.createShader(type);
      glContext.shaderSource(shader, source);
      glContext.compileShader(shader);
      if (!glContext.getShaderParameter(shader, glContext.COMPILE_STATUS)) {
        const log = glContext.getShaderInfoLog(shader);
        glContext.deleteShader(shader);
        throw new Error("Shader compile failed: " + log);
      }
      return shader;
    };
    const vertex = compile(glContext.VERTEX_SHADER, vertexText);
    const fragment = compile(glContext.FRAGMENT_SHADER, fragmentText);
    const program = glContext.createProgram();
    glContext.attachShader(program, vertex);
    glContext.attachShader(program, fragment);
    glContext.linkProgram(program);
    glContext.deleteShader(vertex);
    glContext.deleteShader(fragment);
    if (!glContext.getProgramParameter(program, glContext.LINK_STATUS)) {
      throw new Error("Program link failed: " + glContext.getProgramInfoLog(program));
    }
    return program;
  }

  function bindQuad(program) {
    context.useProgram(program);
    context.bindBuffer(context.ARRAY_BUFFER, buffer);
    const position = context.getAttribLocation(program, "aPosition");
    const texCoord = context.getAttribLocation(program, "aTexCoord");
    context.enableVertexAttribArray(position);
    context.vertexAttribPointer(position, 2, context.FLOAT, false, 16, 0);
    context.enableVertexAttribArray(texCoord);
    context.vertexAttribPointer(texCoord, 2, context.FLOAT, false, 16, 8);
  }

  function resize() {
    pixelRatio = Math.min(window.devicePixelRatio || 1, 1.65);
    width = Math.max(1, Math.floor(window.innerWidth * pixelRatio));
    height = Math.max(1, Math.floor(window.innerHeight * pixelRatio));
    canvas.width = width;
    canvas.height = height;
    context.bindTexture(context.TEXTURE_2D, sceneTexture);
    context.texParameteri(context.TEXTURE_2D, context.TEXTURE_MIN_FILTER, context.LINEAR);
    context.texParameteri(context.TEXTURE_2D, context.TEXTURE_MAG_FILTER, context.LINEAR);
    context.texParameteri(context.TEXTURE_2D, context.TEXTURE_WRAP_S, context.CLAMP_TO_EDGE);
    context.texParameteri(context.TEXTURE_2D, context.TEXTURE_WRAP_T, context.CLAMP_TO_EDGE);
    context.texImage2D(context.TEXTURE_2D, 0, context.RGBA8, width, height, 0, context.RGBA, context.UNSIGNED_BYTE, null);
    context.bindFramebuffer(context.FRAMEBUFFER, framebuffer);
    context.framebufferTexture2D(context.FRAMEBUFFER, context.COLOR_ATTACHMENT0, context.TEXTURE_2D, sceneTexture, 0);
    if (context.checkFramebufferStatus(context.FRAMEBUFFER) !== context.FRAMEBUFFER_COMPLETE) {
      throw new Error("WebGL2 scene framebuffer is incomplete.");
    }
    context.bindFramebuffer(context.FRAMEBUFFER, null);
    context.viewport(0, 0, width, height);
  }

  function render(now) {
    const delta = Math.min(0.05, Math.max(0, (now - lastFrame) / 1000));
    lastFrame = now;
    if (reducedMotion.matches) {
      morph = morphTarget;
    } else {
      morph += (morphTarget - morph) * (1 - Math.exp(-delta * 7.5));
    }
    if (playing && !reducedMotion.matches) {
      progressValue = (progressValue + delta * 100 / 48) % 100;
      progress.value = String(Math.round(progressValue));
      updateElapsed();
    }

    const time = reducedMotion.matches ? 0 : (now - startedAt) / 1000;
    context.bindFramebuffer(context.FRAMEBUFFER, framebuffer);
    context.viewport(0, 0, width, height);
    bindQuad(backgroundProgram);
    context.uniform2f(context.getUniformLocation(backgroundProgram, "uResolution"), width, height);
    context.uniform1f(context.getUniformLocation(backgroundProgram, "uTime"), time);
    context.drawArrays(context.TRIANGLE_STRIP, 0, 4);

    context.bindFramebuffer(context.FRAMEBUFFER, null);
    bindQuad(glassProgram);
    context.activeTexture(context.TEXTURE0);
    context.bindTexture(context.TEXTURE_2D, sceneTexture);
    context.uniform1i(context.getUniformLocation(glassProgram, "uScene"), 0);
    context.uniform2f(context.getUniformLocation(glassProgram, "uResolution"), width, height);
    const rect = panel.getBoundingClientRect();
    context.uniform4f(
      context.getUniformLocation(glassProgram, "uLensRect"),
      rect.left * pixelRatio, rect.top * pixelRatio,
      rect.width * pixelRatio, rect.height * pixelRatio
    );
    context.uniform1f(context.getUniformLocation(glassProgram, "uMorph"), morph);
    context.uniform1f(context.getUniformLocation(glassProgram, "uStrength"), strength);
    context.uniform2f(context.getUniformLocation(glassProgram, "uPointer"), pointer[0], pointer[1]);
    context.drawArrays(context.TRIANGLE_STRIP, 0, 4);

    frameId = requestAnimationFrame(render);
  }

  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(document.documentElement);
  resizeObserver.observe(panel);
  window.addEventListener("resize", resize);
  canvas.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    cancelAnimationFrame(frameId);
    document.documentElement.classList.add("no-webgl");
    const blurAvailable = window.CSS && CSS.supports("backdrop-filter", "blur(1px)");
    document.documentElement.dataset.renderer = blurAvailable ? "css-l1" : "css-l0";
    status.textContent = blurAvailable ? "CONTEXT LOST · CSS L1 FALLBACK" : "CONTEXT LOST · L0 FALLBACK";
  });

  window.addEventListener("pointermove", (event) => {
    pointer = [event.clientX / Math.max(1, window.innerWidth), 1 - event.clientY / Math.max(1, window.innerHeight)];
  }, { passive: true });

  morphButton.addEventListener("click", () => {
    morphTarget = morphTarget > 0.5 ? 0 : 1;
    morphButton.setAttribute("aria-pressed", String(morphTarget > 0.5));
    morphLabel.textContent = morphTarget > 0.5 ? "Separate the lens" : "Connect the lens";
  });
  playButton.addEventListener("click", () => {
    playing = !playing;
    playButton.setAttribute("aria-pressed", String(playing));
    playGlyph.textContent = playing ? "Ⅱ" : "▶";
    playLabel.textContent = playing ? "Pause preview" : "Play preview";
    progressOrigin = performance.now();
  });
  progress.addEventListener("input", () => {
    progressValue = Number(progress.value);
    updateElapsed();
  });
  previous.addEventListener("click", () => {
    progressValue = 0;
    progress.value = "0";
    updateElapsed();
  });
  next.addEventListener("click", () => {
    progressValue = 100;
    progress.value = "100";
    updateElapsed();
  });

  function updateElapsed() {
    const seconds = Math.min(48, Math.floor(progressValue / 100 * 48));
    elapsed.textContent = String(Math.floor(seconds / 60)).padStart(2, "0") + ":" + String(seconds % 60).padStart(2, "0");
  }

  morphButton.addEventListener("pointerdown", () => { strength = 1.08; });
  morphButton.addEventListener("pointerup", () => { strength = 1; });
  requestAnimationFrame(render);
}
