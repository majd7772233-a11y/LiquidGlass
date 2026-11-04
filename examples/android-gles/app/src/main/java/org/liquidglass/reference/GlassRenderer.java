package org.liquidglass.reference;

import android.opengl.GLES20;
import android.opengl.GLSurfaceView;
import android.util.Log;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

final class GlassRenderer implements GLSurfaceView.Renderer {
    private static final String TAG = "LiquidGlassDemo";

    private static final String VERTEX_SHADER =
            "attribute vec2 aPosition;\n" +
            "attribute vec2 aTexCoord;\n" +
            "varying vec2 vUv;\n" +
            "void main(){ vUv = aTexCoord; gl_Position = vec4(aPosition, 0.0, 1.0); }";

    private static final String BACKGROUND_SHADER =
            "precision mediump float;\n" +
            "varying vec2 vUv;\n" +
            "uniform vec2 uResolution;\n" +
            "uniform float uTime;\n" +
            "float ring(float d, float w){ return 1.0 - smoothstep(w, w + 0.008, abs(d)); }\n" +
            "void main(){\n" +
            " vec2 uv = vUv; float aspect = uResolution.x / max(uResolution.y, 1.0);\n" +
            " vec2 p = (uv - 0.5) * vec2(aspect, 1.0); float t = uTime;\n" +
            " vec3 color = mix(vec3(0.014,0.032,0.078), vec3(0.09,0.19,0.34), smoothstep(-0.55,0.58,p.y));\n" +
            " color = mix(color, vec3(0.24,0.13,0.34), smoothstep(0.72,-0.55,p.x+0.35*p.y)*0.43);\n" +
            " vec2 cell = abs(fract(uv*vec2(19.0,13.0))-0.5);\n" +
            " float grid = 1.0-smoothstep(0.478,0.493,max(cell.x,cell.y));\n" +
            " color += grid*vec3(0.055,0.105,0.17);\n" +
            " float scan = ring(p.y-0.12*sin(p.x*3.2+t*0.24),0.003);\n" +
            " color += scan*vec3(0.13,0.27,0.38)*0.8;\n" +
            " vec2 a = p-vec2(-0.34+0.055*sin(t*0.22),0.13);\n" +
            " color += ring(length(a)-0.19,0.004)*vec3(0.16,0.65,0.82)*0.65;\n" +
            " vec2 b = p-vec2(0.33,-0.18+0.045*cos(t*0.18));\n" +
            " color += ring(length(b)-0.27,0.003)*vec3(0.72,0.37,0.91)*0.72;\n" +
            " vec2 g1 = p-vec2(-0.22,0.32+0.035*sin(t*0.31));\n" +
            " color += exp(-dot(g1,g1)*5.2)*vec3(0.12,0.32,0.52);\n" +
            " vec2 g2 = p-vec2(0.48,-0.31+0.045*cos(t*0.25));\n" +
            " color += exp(-dot(g2,g2)*7.0)*vec3(0.34,0.14,0.48);\n" +
            " float vignette = 1.0-smoothstep(0.12,1.18,length(p*vec2(0.78,1.1)));\n" +
            " color *= 0.72+0.28*vignette; gl_FragColor=vec4(color,1.0);\n" +
            "}";

    private static final String GLASS_SHADER =
            "precision mediump float;\n" +
            "varying vec2 vUv;\n" +
            "uniform sampler2D uScene;\n" +
            "uniform vec2 uResolution;\n" +
            "uniform vec4 uLensRect;\n" +
            "uniform float uMorph;\n" +
            "uniform float uStrength;\n" +
            "uniform float uHasScene;\n" +
            "uniform vec2 uPointer;\n" +
            "float roundBox(vec2 p,vec2 b,float r){ vec2 q=abs(p)-b+vec2(r); return length(max(q,0.0))+min(max(q.x,q.y),0.0)-r; }\n" +
            "float unite(float a,float b,float k){ float h=clamp(0.5+0.5*(b-a)/max(k,0.001),0.0,1.0); return mix(b,a,h)-k*h*(1.0-h); }\n" +
            "float lens(vec2 p){\n" +
            " float hw=max(20.0,uLensRect.z*0.5-2.0); float hh=max(20.0,uLensRect.w*0.5-2.0);\n" +
            " float body=roundBox(p,vec2(hw,hh),min(hh*0.44,42.0));\n" +
            " if(uMorph<0.001) return body;\n" +
            " float radius=min(hh*0.40,hw*0.19)*uMorph;\n" +
            " float bubble=length(p-vec2(hw*0.91,-hh*0.48))-radius;\n" +
            " return unite(body,bubble,max(1.0,radius*0.72));\n" +
            "}\n" +
            "void main(){\n" +
            " vec2 uv=vUv; vec3 original=vec3(0.035,0.065,0.12);\n" +
            " if(uHasScene>0.5) original=texture2D(uScene,uv).rgb;\n" +
            " vec2 center=vec2(uLensRect.x+uLensRect.z*0.5,uResolution.y-(uLensRect.y+uLensRect.w*0.5));\n" +
            " vec2 p=gl_FragCoord.xy-center; float d=lens(p);\n" +
            " float mask=1.0-smoothstep(-1.6,1.6,d); float e=1.7;\n" +
            " vec2 grad=vec2(lens(p+vec2(e,0.0))-lens(p-vec2(e,0.0)),lens(p+vec2(0.0,e))-lens(p-vec2(0.0,e)));\n" +
            " vec2 n=length(grad)>0.001?normalize(grad):vec2(0.0,1.0);\n" +
            " float edge=exp(-abs(d)*0.075); float body=1.0-smoothstep(0.0,95.0,-d);\n" +
            " vec2 pointerForce=(uPointer-0.5)*2.0;\n" +
            " vec2 offset=n*uStrength*(3.5+15.0*edge+3.0*body)+pointerForce*body*1.6;\n" +
            " vec3 refracted=original;\n" +
            " if(uHasScene>0.5){\n" +
            "  vec2 shifted=clamp(uv+offset/uResolution,vec2(0.002),vec2(0.998));\n" +
            "  refracted=texture2D(uScene,shifted).rgb;\n" +
            "  vec2 dispersion=n*(1.2/uResolution);\n" +
            "  refracted.r=texture2D(uScene,clamp(shifted+dispersion,vec2(0.002),vec2(0.998))).r;\n" +
            "  refracted.b=texture2D(uScene,clamp(shifted-dispersion,vec2(0.002),vec2(0.998))).b;\n" +
            " }\n" +
            " vec2 lightDir=normalize(vec2(-0.48,0.86)+pointerForce*0.11);\n" +
            " float fresnel=pow(1.0-abs(dot(n,lightDir)),3.2);\n" +
            " float rim=edge*(0.22+0.48*fresnel);\n" +
            " float spec=pow(max(dot(n,lightDir),0.0),13.0)*edge*0.50;\n" +
            " float highlight=exp(-pow((p.y-uLensRect.w*0.27)/max(18.0,uLensRect.w*0.22),2.0))*mask;\n" +
            " vec3 glass=mix(original,refracted,uHasScene>0.5?0.91:0.0);\n" +
            " glass=mix(glass,glass*vec3(0.88,0.96,1.045)+vec3(0.018,0.026,0.045),0.13);\n" +
            " glass+=vec3(0.52,0.79,1.0)*rim*0.27+vec3(0.86,0.95,1.0)*spec+vec3(0.44,0.73,0.92)*highlight*0.06;\n" +
            " gl_FragColor=vec4(mix(original,glass,mask),1.0);\n" +
            "}";

    private final FloatBuffer quad;
    private volatile float[] lensRect = new float[]{40f, 400f, 720f, 330f};
    private volatile float morphTarget = 0f;
    private volatile float strength = 1.13f;
    private volatile float pointerX = 0.5f;
    private volatile float pointerY = 0.5f;
    private volatile boolean playing = false;

    private int backgroundProgram;
    private int glassProgram;
    private int sceneTexture;
    private int framebuffer;
    private int surfaceWidth = 1;
    private int surfaceHeight = 1;
    private boolean framebufferReady;
    private boolean loggedReady;
    private float morph;
    private long startNanos;
    private long lastNanos;

    GlassRenderer() {
        ByteBuffer bytes = ByteBuffer.allocateDirect(16 * 4);
        bytes.order(ByteOrder.nativeOrder());
        quad = bytes.asFloatBuffer();
        quad.put(new float[]{
                -1f, -1f, 0f, 0f,
                 1f, -1f, 1f, 0f,
                -1f,  1f, 0f, 1f,
                 1f,  1f, 1f, 1f
        });
        quad.position(0);
    }

    void setLensRect(float x, float y, float width, float height) {
        lensRect = new float[]{x, y, width, height};
    }

    void setMorphTarget(float value) {
        morphTarget = Math.max(0f, Math.min(1f, value));
    }

    void setStrength(float value) {
        strength = Math.max(0.25f, Math.min(1.5f, value));
    }

    void setPlaying(boolean value) {
        playing = value;
    }

    void release() {
        // GL resources are released with the EGL context; GLSurfaceView owns its lifecycle.
    }

    @Override
    public void onSurfaceCreated(GL10 unused, EGLConfig config) {
        GLES20.glDisable(GLES20.GL_DEPTH_TEST);
        GLES20.glDisable(GLES20.GL_CULL_FACE);
        GLES20.glClearColor(0.025f, 0.04f, 0.08f, 1f);
        try {
            backgroundProgram = linkProgram(VERTEX_SHADER, BACKGROUND_SHADER);
            glassProgram = linkProgram(VERTEX_SHADER, GLASS_SHADER);
            startNanos = System.nanoTime();
            lastNanos = startNanos;
            Log.i(TAG, "GL_CONTEXT_READY version=OpenGL_ES_2.0");
        } catch (RuntimeException error) {
            backgroundProgram = 0;
            glassProgram = 0;
            Log.e(TAG, "GL_SHADER_FAILURE " + error.getMessage());
        }
    }

    @Override
    public void onSurfaceChanged(GL10 unused, int width, int height) {
        surfaceWidth = Math.max(1, width);
        surfaceHeight = Math.max(1, height);
        GLES20.glViewport(0, 0, surfaceWidth, surfaceHeight);
        createSceneFramebuffer();
    }

    private void createSceneFramebuffer() {
        deleteFramebuffer();
        int[] textureIds = new int[1];
        int[] framebufferIds = new int[1];
        GLES20.glGenTextures(1, textureIds, 0);
        sceneTexture = textureIds[0];
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, sceneTexture);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_LINEAR);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE);
        GLES20.glTexImage2D(GLES20.GL_TEXTURE_2D, 0, GLES20.GL_RGBA,
                surfaceWidth, surfaceHeight, 0, GLES20.GL_RGBA, GLES20.GL_UNSIGNED_BYTE, null);

        GLES20.glGenFramebuffers(1, framebufferIds, 0);
        framebuffer = framebufferIds[0];
        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, framebuffer);
        GLES20.glFramebufferTexture2D(GLES20.GL_FRAMEBUFFER, GLES20.GL_COLOR_ATTACHMENT0,
                GLES20.GL_TEXTURE_2D, sceneTexture, 0);
        int result = GLES20.glCheckFramebufferStatus(GLES20.GL_FRAMEBUFFER);
        framebufferReady = result == GLES20.GL_FRAMEBUFFER_COMPLETE;
        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, 0);

        if (framebufferReady) {
            Log.i(TAG, "SCENE_FBO_READY width=" + surfaceWidth + " height=" + surfaceHeight);
        } else {
            Log.w(TAG, "GL_FALLBACK tier=L0 framebuffer_status=0x" + Integer.toHexString(result));
        }
    }

    @Override
    public void onDrawFrame(GL10 unused) {
        if (backgroundProgram == 0 || glassProgram == 0) {
            GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT);
            return;
        }

        long now = System.nanoTime();
        float delta = Math.min(0.05f, Math.max(0f, (now - lastNanos) / 1_000_000_000f));
        lastNanos = now;
        float target = morphTarget;
        morph += (target - morph) * (1f - (float) Math.exp(-delta * 7.5f));
        float time = playing ? (now - startNanos) / 1_000_000_000f : 0f;

        if (framebufferReady) {
            GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, framebuffer);
        } else {
            GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, 0);
        }
        GLES20.glViewport(0, 0, surfaceWidth, surfaceHeight);
        GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT);
        drawBackground(time);

        GLES20.glBindFramebuffer(GLES20.GL_FRAMEBUFFER, 0);
        GLES20.glViewport(0, 0, surfaceWidth, surfaceHeight);
        if (framebufferReady) {
            GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT);
        } else {
            GLES20.glEnable(GLES20.GL_BLEND);
            GLES20.glBlendFunc(GLES20.GL_SRC_ALPHA, GLES20.GL_ONE_MINUS_SRC_ALPHA);
        }
        drawGlass();
        if (!framebufferReady) GLES20.glDisable(GLES20.GL_BLEND);

        if (!loggedReady) {
            loggedReady = true;
            Log.i(TAG, framebufferReady
                    ? "GL_READY tier=L3 renderer=GLES2_APP_OWNED_FBO"
                    : "GL_READY tier=L0 renderer=GLES2_TINT_FALLBACK");
        }
    }

    private void drawBackground(float time) {
        GLES20.glUseProgram(backgroundProgram);
        bindQuad(backgroundProgram);
        uniform2f(backgroundProgram, "uResolution", surfaceWidth, surfaceHeight);
        uniform1f(backgroundProgram, "uTime", time);
        GLES20.glDrawArrays(GLES20.GL_TRIANGLE_STRIP, 0, 4);
    }

    private void drawGlass() {
        GLES20.glUseProgram(glassProgram);
        bindQuad(glassProgram);
        float[] rect = lensRect;
        uniform2f(glassProgram, "uResolution", surfaceWidth, surfaceHeight);
        uniform4f(glassProgram, "uLensRect", rect[0], rect[1], rect[2], rect[3]);
        uniform1f(glassProgram, "uMorph", morph);
        uniform1f(glassProgram, "uStrength", strength);
        uniform1f(glassProgram, "uHasScene", framebufferReady ? 1f : 0f);
        uniform2f(glassProgram, "uPointer", pointerX, pointerY);
        GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, sceneTexture);
        int sampler = GLES20.glGetUniformLocation(glassProgram, "uScene");
        if (sampler >= 0) GLES20.glUniform1i(sampler, 0);
        GLES20.glDrawArrays(GLES20.GL_TRIANGLE_STRIP, 0, 4);
    }

    private void bindQuad(int program) {
        int position = GLES20.glGetAttribLocation(program, "aPosition");
        int texCoord = GLES20.glGetAttribLocation(program, "aTexCoord");
        quad.position(0);
        GLES20.glEnableVertexAttribArray(position);
        GLES20.glVertexAttribPointer(position, 2, GLES20.GL_FLOAT, false, 16, quad);
        quad.position(2);
        GLES20.glEnableVertexAttribArray(texCoord);
        GLES20.glVertexAttribPointer(texCoord, 2, GLES20.GL_FLOAT, false, 16, quad);
        quad.position(0);
    }

    private void uniform1f(int program, String name, float value) {
        int location = GLES20.glGetUniformLocation(program, name);
        if (location >= 0) GLES20.glUniform1f(location, value);
    }

    private void uniform2f(int program, String name, float x, float y) {
        int location = GLES20.glGetUniformLocation(program, name);
        if (location >= 0) GLES20.glUniform2f(location, x, y);
    }

    private void uniform4f(int program, String name, float x, float y, float z, float w) {
        int location = GLES20.glGetUniformLocation(program, name);
        if (location >= 0) GLES20.glUniform4f(location, x, y, z, w);
    }

    private int linkProgram(String vertexSource, String fragmentSource) {
        int vertex = compileShader(GLES20.GL_VERTEX_SHADER, vertexSource);
        int fragment = compileShader(GLES20.GL_FRAGMENT_SHADER, fragmentSource);
        int program = GLES20.glCreateProgram();
        GLES20.glAttachShader(program, vertex);
        GLES20.glAttachShader(program, fragment);
        GLES20.glBindAttribLocation(program, 0, "aPosition");
        GLES20.glBindAttribLocation(program, 1, "aTexCoord");
        GLES20.glLinkProgram(program);
        int[] status = new int[1];
        GLES20.glGetProgramiv(program, GLES20.GL_LINK_STATUS, status, 0);
        GLES20.glDeleteShader(vertex);
        GLES20.glDeleteShader(fragment);
        if (status[0] == 0) {
            String log = GLES20.glGetProgramInfoLog(program);
            GLES20.glDeleteProgram(program);
            throw new IllegalStateException("Program link failed: " + log);
        }
        return program;
    }

    private int compileShader(int type, String source) {
        int shader = GLES20.glCreateShader(type);
        GLES20.glShaderSource(shader, source);
        GLES20.glCompileShader(shader);
        int[] status = new int[1];
        GLES20.glGetShaderiv(shader, GLES20.GL_COMPILE_STATUS, status, 0);
        if (status[0] == 0) {
            String log = GLES20.glGetShaderInfoLog(shader);
            GLES20.glDeleteShader(shader);
            throw new IllegalStateException("Shader compile failed: " + log);
        }
        return shader;
    }

    private void deleteFramebuffer() {
        if (framebuffer != 0) {
            GLES20.glDeleteFramebuffers(1, new int[]{framebuffer}, 0);
            framebuffer = 0;
        }
        if (sceneTexture != 0) {
            GLES20.glDeleteTextures(1, new int[]{sceneTexture}, 0);
            sceneTexture = 0;
        }
        framebufferReady = false;
    }
}
