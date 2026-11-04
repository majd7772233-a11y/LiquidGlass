package org.liquidglass.reference;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.animation.ValueAnimator;
import android.os.Build;
import android.provider.Settings;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.TextView;

public final class MainActivity extends Activity {
    private GLSurfaceView glView;
    private GlassRenderer renderer;
    private LinearLayout panel;
    private TextView status;
    private Button playButton;
    private Button morphButton;
    private boolean playing = true;
    private boolean connected = false;
    private boolean reducedMotionEnabled;
    private boolean highContrastEnabled;
    private boolean activityResumed;
    private final Handler frameHandler = new Handler(Looper.getMainLooper());
    private final Runnable framePump = new Runnable() {
        @Override public void run() {
            if (!activityResumed || glView == null) return;
            glView.requestRender();
            if ((playing && !reducedMotionEnabled) || (renderer != null && renderer.isMorphing())) frameHandler.postDelayed(this, 16);
        }
    };
    private final Handler statusHandler = new Handler(Looper.getMainLooper());
    private final Runnable statusPoll = new Runnable() {
        @Override public void run() {
            if (status != null && renderer != null) {
                status.setText(renderer.getStatus());
                if (!isFinishing()) statusHandler.postDelayed(this, 250);
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Deterministic landscape layout exercise for headless emulator CI; production launches omit this extra.
        if (getIntent().getBooleanExtra("test_force_landscape", false)) {
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        }
        Window window = getWindow();
        window.setStatusBarColor(Color.rgb(8, 13, 29));
        window.setNavigationBarColor(Color.rgb(8, 13, 29));
        highContrastEnabled = isHighTextContrastEnabled();
        reducedMotionEnabled = isReducedMotionEnabled();
        android.util.Log.i("LiquidGlassDemo", "GL_ACCESSIBILITY reduced_motion=" + reducedMotionEnabled
                + " high_text_contrast=" + highContrastEnabled);

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(highContrastEnabled ? Color.BLACK : Color.rgb(8, 13, 29));

        renderer = new GlassRenderer();
        renderer.setPlaying(playing);
        renderer.setReducedMotion(reducedMotionEnabled);
        int extraSurfaces = Math.max(0, Math.min(3, getIntent().getIntExtra("extra_surfaces", 0)));
        renderer.setExtraSurfaceCount(extraSurfaces);
        android.util.Log.i("LiquidGlassDemo", "SURFACE_COUNT main=1 additional=" + extraSurfaces + " total=" + (extraSurfaces + 1));
        glView = new GLSurfaceView(this);
        glView.setEGLContextClientVersion(2);
        glView.setEGLConfigChooser(8, 8, 8, 8, 16, 0);
        glView.setPreserveEGLContextOnPause(true);
        glView.setRenderer(renderer);
        glView.setRenderMode(GLSurfaceView.RENDERMODE_WHEN_DIRTY);
        root.addView(glView, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
        ));

        TextView brand = text("◈  LIQUIDGLASS", 12, 0xFFEAF2FF, true);
        brand.setLetterSpacing(0.16f);
        FrameLayout.LayoutParams brandParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT,
                dp(36),
                Gravity.TOP | Gravity.START
        );
        brandParams.setMargins(dp(24), dp(18), dp(24), 0);
        root.addView(brand, brandParams);

        TextView edition = text("REFERENCE LAB / 002", 9, 0xFF94A8C5, false);
        edition.setTypeface(Typeface.MONOSPACE);
        edition.setLetterSpacing(0.12f);
        FrameLayout.LayoutParams editionParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT,
                dp(30),
                Gravity.TOP | Gravity.END
        );
        editionParams.setMargins(dp(20), dp(22), dp(24), 0);
        root.addView(edition, editionParams);

        panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        panel.setGravity(Gravity.CENTER_VERTICAL);
        panel.setPadding(dp(25), dp(23), dp(25), dp(20));
        panel.setBackground(roundedStroke(highContrastEnabled ? 0xFF05070B : 0x0DDBF3FF,
                highContrastEnabled ? Color.WHITE : 0x55E9F7FF, 32));
        panel.setElevation(dp(18));
        panel.setClipChildren(false);
        panel.setClipToPadding(false);

        TextView eyebrow = text("NOW EXPLORING  ·  OPENGL MATERIAL", 9, 0xFFB3C7E5, true);
        eyebrow.setTypeface(Typeface.MONOSPACE);
        eyebrow.setLetterSpacing(0.10f);
        panel.addView(eyebrow, wrap());

        TextView title = text("Light, held in motion.", 26, 0xFFF5F8FF, true);
        title.setPadding(0, dp(10), 0, dp(4));
        panel.addView(title, wrap());

        TextView subtitle = text("An app-owned scene, shaped by a living lens.", 12, 0xFFB5C5DE, false);
        subtitle.setPadding(0, 0, 0, dp(17));
        panel.addView(subtitle, wrap());

        LinearLayout dataRow = new LinearLayout(this);
        dataRow.setOrientation(LinearLayout.HORIZONTAL);
        dataRow.setGravity(Gravity.CENTER_VERTICAL);
        TextView track = text("CHROMATIC DRIFT", 9, 0xFFDDEBFF, true);
        track.setTypeface(Typeface.MONOSPACE);
        track.setLetterSpacing(0.08f);
        dataRow.addView(track, new LinearLayout.LayoutParams(0, dp(28), 1));
        TextView duration = text("00:48  /  FIELD 01", 8, 0xFF98AAC8, false);
        duration.setTypeface(Typeface.MONOSPACE);
        dataRow.addView(duration, wrap());
        panel.addView(dataRow, wrap());

        SeekBar strength = new SeekBar(this);
        strength.setMax(100);
        strength.setProgress(72);
        strength.setContentDescription("Refraction strength");
        strength.setProgressTintList(android.content.res.ColorStateList.valueOf(0xFF9CEBFF));
        strength.setThumbTintList(android.content.res.ColorStateList.valueOf(0xFFEAFBFF));
        strength.setProgressBackgroundTintList(android.content.res.ColorStateList.valueOf(0x558FAACD));
        LinearLayout.LayoutParams seekParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(48));
        seekParams.topMargin = dp(6);
        panel.addView(strength, seekParams);
        strength.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int value, boolean fromUser) {
                renderer.setStrength(0.45f + (value / 100.0f) * 0.95f);
                if (glView != null) glView.requestRender();
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) { }
            @Override public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        LinearLayout controls = new LinearLayout(this);
        controls.setOrientation(LinearLayout.HORIZONTAL);
        controls.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams controlsParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, dp(56));
        controlsParams.topMargin = dp(10);

        playButton = button("Pause preview");
        playButton.setContentDescription("Pause optical preview");
        morphButton = button("Connect lens");
        morphButton.setContentDescription("Connect the liquid lens");
        LinearLayout.LayoutParams firstButton = new LinearLayout.LayoutParams(0, dp(48), 1);
        firstButton.rightMargin = dp(7);
        LinearLayout.LayoutParams secondButton = new LinearLayout.LayoutParams(0, dp(48), 1);
        secondButton.leftMargin = dp(7);
        controls.addView(playButton, firstButton);
        controls.addView(morphButton, secondButton);
        panel.addView(controls, controlsParams);

        status = text("GL CONTEXT · INITIALIZING", 10, 0xFF9CCCE5, false);
        status.setAccessibilityLiveRegion(View.ACCESSIBILITY_LIVE_REGION_POLITE);
        status.setTypeface(Typeface.MONOSPACE);
        status.setLetterSpacing(0.04f);
        status.setGravity(Gravity.CENTER);
        status.setPadding(0, dp(15), 0, 0);
        panel.addView(status, wrap());

        FrameLayout.LayoutParams panelParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.WRAP_CONTENT,
                Gravity.CENTER
        );
        panelParams.setMargins(dp(22), dp(20), dp(22), dp(20));
        root.addView(panel, panelParams);
        panel.addOnLayoutChangeListener((view, left, top, right, bottom, oldLeft, oldTop, oldRight, oldBottom) -> updateLensRect());
        panel.post(this::updateLensRect);

        playButton.setOnClickListener(view -> {
            playing = !playing;
            renderer.setPlaying(playing);
            scheduleFrames();
            playButton.setText(playing ? "Pause preview" : "Play preview");
            playButton.setContentDescription(playing ? "Pause optical preview" : "Play optical preview");
        });
        morphButton.setOnClickListener(view -> {
            connected = !connected;
            renderer.setMorphTarget(connected ? 1.0f : 0.0f);
            scheduleFrames();
            morphButton.setText(connected ? "Separate lens" : "Connect lens");
            morphButton.setContentDescription(connected ? "Separate the connected liquid lens" : "Connect the liquid lens");
        });

        TextView footer = text("L2 REFRACTION  ·  L3 CONNECTED SHAPE  ·  JAVA / GLES 2.0", 9, 0xFF9FB0CD, false);
        footer.setTypeface(Typeface.MONOSPACE);
        footer.setGravity(Gravity.CENTER);
        footer.setLetterSpacing(0.04f);
        FrameLayout.LayoutParams footerParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, dp(42), Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL);
        footerParams.setMargins(dp(12), 0, dp(12), dp(12));
        root.addView(footer, footerParams);

        setContentView(root);
        root.post(() -> {
            android.content.res.Configuration configuration = getResources().getConfiguration();
            android.util.DisplayMetrics metrics = getResources().getDisplayMetrics();
            android.util.Log.i("LiquidGlassDemo",
                    "UI_READY activity=MainActivity width=" + root.getWidth()
                            + " height=" + root.getHeight()
                            + " orientation=" + configuration.orientation
                            + " screen_width_dp=" + configuration.screenWidthDp
                            + " screen_height_dp=" + configuration.screenHeightDp
                            + " density=" + metrics.density
                            + " panel_width=" + panel.getWidth());
        });
    }

    private void updateLensRect() {
        if (panel == null || renderer == null || glView == null || panel.getWidth() <= 0) return;
        int[] panelLocation = new int[2];
        int[] glLocation = new int[2];
        panel.getLocationOnScreen(panelLocation);
        glView.getLocationOnScreen(glLocation);
        renderer.setLensRect(
                panelLocation[0] - glLocation[0],
                panelLocation[1] - glLocation[1],
                panel.getWidth(),
                panel.getHeight()
        );
    }

    private TextView text(String value, float size, int color, boolean bold) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(color);
        view.setGravity(Gravity.CENTER_VERTICAL);
        view.setFontFeatureSettings("kern");
        if (bold) view.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
        return view;
    }

    private Button button(String label) {
        Button view = new Button(this);
        view.setText(label);
        view.setTextSize(11);
        view.setAllCaps(false);
        view.setTextColor(0xFFF2F8FF);
        view.setMinHeight(dp(48));
        view.setMinimumHeight(dp(48));
        view.setPadding(dp(10), 0, dp(10), 0);
        view.setBackground(roundedStroke(highContrastEnabled ? 0xFF101820 : 0x334F7495,
                highContrastEnabled ? Color.WHITE : 0xFF9DEBFF, 24));
        view.setStateListAnimator(null);
        return view;
    }

    private GradientDrawable roundedStroke(int fill, int stroke, int radiusDp) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setShape(GradientDrawable.RECTANGLE);
        drawable.setColor(fill);
        drawable.setCornerRadius(dp(radiusDp));
        drawable.setStroke(dp(1), stroke);
        return drawable;
    }

    private LinearLayout.LayoutParams wrap() {
        return new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    private boolean isHighTextContrastEnabled() {
        try {
            return Settings.Secure.getInt(getContentResolver(), "high_text_contrast_enabled", 0) == 1;
        } catch (RuntimeException ignored) {
            return false;
        }
    }

    private boolean isReducedMotionEnabled() {
        if (Build.VERSION.SDK_INT >= 26 && !ValueAnimator.areAnimatorsEnabled()) return true;
        try {
            return Settings.Global.getFloat(getContentResolver(), Settings.Global.ANIMATOR_DURATION_SCALE, 1f) == 0f;
        } catch (RuntimeException ignored) {
            return false;
        }
    }

    private void scheduleFrames() {
        frameHandler.removeCallbacks(framePump);
        if (!activityResumed || glView == null) return;
        glView.requestRender();
        if ((playing && !reducedMotionEnabled) || (renderer != null && renderer.isMorphing())) frameHandler.postDelayed(framePump, 16);
    }

    @Override protected void onResume() {
        super.onResume();
        activityResumed = true;
        android.util.Log.i("LiquidGlassDemo", "ACTIVITY_RESUMED activity=MainActivity");
        reducedMotionEnabled = isReducedMotionEnabled();
        if (renderer != null) renderer.setReducedMotion(reducedMotionEnabled);
        if (glView != null) glView.onResume();
        statusHandler.post(statusPoll);
        scheduleFrames();
    }

    @Override public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        android.util.Log.i("LiquidGlassDemo", "WINDOW_FOCUS hasFocus=" + hasFocus);
    }

    @Override protected void onPause() {
        activityResumed = false;
        frameHandler.removeCallbacks(framePump);
        statusHandler.removeCallbacks(statusPoll);
        if (glView != null) glView.onPause();
        super.onPause();
    }

    @Override protected void onDestroy() {
        activityResumed = false;
        frameHandler.removeCallbacks(framePump);
        statusHandler.removeCallbacks(statusPoll);
        if (renderer != null) renderer.release();
        super.onDestroy();
    }
}
