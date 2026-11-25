import React from "react";
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import {
  CROSSFADE_FRAMES,
  MotionType,
  SCENES,
  SceneSpec,
  TOTAL_DURATION_FRAMES,
} from "./scenes";
import { CalloutPin } from "./components/CalloutPin";

const FONT_ZH =
  "'Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', 'SimHei', sans-serif";
const FONT_MONO = "'Consolas', 'JetBrains Mono', 'Courier New', monospace";

function getKenBurnsTransform(
  motion: MotionType,
  progress: number
): { scale: number; tx: number; ty: number } {
  const eased = Easing.inOut(Easing.quad)(progress);
  switch (motion) {
    case "zoomInPanRight":
      return {
        scale: interpolate(eased, [0, 1], [1.05, 1.13]),
        tx: interpolate(eased, [0, 1], [20, -22]),
        ty: interpolate(eased, [0, 1], [4, -6]),
      };
    case "craneTiltUp":
      return {
        scale: interpolate(eased, [0, 1], [1.05, 1.14]),
        tx: interpolate(eased, [0, 1], [-8, 8]),
        ty: interpolate(eased, [0, 1], [-14, 16]),
      };
    case "macroSlowPush":
      return {
        scale: interpolate(eased, [0, 1], [1.04, 1.15]),
        tx: interpolate(eased, [0, 1], [-14, 14]),
        ty: interpolate(eased, [0, 1], [8, -10]),
      };
    case "pullBackTwilight":
      return {
        scale: interpolate(eased, [0, 1], [1.14, 1.05]),
        tx: interpolate(eased, [0, 1], [12, -12]),
        ty: interpolate(eased, [0, 1], [10, -8]),
      };
  }
}

const SceneLayer: React.FC<{
  scene: SceneSpec;
  isFirst: boolean;
  isLast: boolean;
}> = ({ scene, isFirst, isLast }) => {
  const frame = useCurrentFrame();
  const dur = scene.durationInFrames;
  const progress = Math.min(1, Math.max(0, frame / Math.max(1, dur - 1)));

  const fadeIn = interpolate(
    frame,
    [0, isFirst ? 18 : CROSSFADE_FRAMES],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const fadeOut = interpolate(
    frame,
    [dur - (isLast ? 20 : CROSSFADE_FRAMES), dur],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const sceneOpacity = Math.min(fadeIn, fadeOut);

  const { scale, tx, ty } = getKenBurnsTransform(scene.motion, progress);

  const textOpacity = interpolate(
    frame,
    [12, 26, dur - 22, dur - 8],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const badgeShift = interpolate(frame, [6, 24], [14, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ opacity: sceneOpacity }}>
      {/* Keyframe Layer with Ken Burns motion */}
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img
          src={staticFile(scene.image)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `translate3d(${tx}px, ${ty}px, 0) scale(${scale})`,
            transformOrigin: "center center",
          }}
        />
      </AbsoluteFill>

      {/* Top/Bottom Contrast Scrims */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(6,10,19,0.58) 0%, rgba(6,10,19,0.0) 24%, rgba(6,10,19,0.0) 64%, rgba(6,10,19,0.88) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Animated Structural Callout Pins */}
      {scene.callouts.map((callout) => (
        <CalloutPin
          key={callout.id}
          callout={callout}
          sceneDuration={dur}
        />
      ))}

      {/* Top-left Chapter Badge & Title */}
      <div
        style={{
          position: "absolute",
          top: 56,
          left: 62,
          opacity: textOpacity,
          transform: `translateY(${badgeShift}px)`,
        }}
      >
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            padding: "5px 14px",
            backgroundColor: "rgba(10, 16, 28, 0.78)",
            border: "1px solid rgba(56, 189, 248, 0.6)",
            borderRadius: 4,
            fontFamily: `${FONT_MONO}, ${FONT_ZH}`,
            fontSize: 16,
            fontWeight: 700,
            color: "#38bdf8",
            letterSpacing: "0.08em",
          }}
        >
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              backgroundColor: "#38bdf8",
              display: "inline-block",
            }}
          />
          {scene.chapter}
        </div>
        <div
          style={{
            marginTop: 12,
            fontFamily: FONT_ZH,
            fontSize: 40,
            fontWeight: 800,
            color: "#f8fafc",
            letterSpacing: "0.04em",
            textShadow: "0 4px 20px rgba(0, 0, 0, 0.75)",
          }}
        >
          {scene.title}
        </div>
      </div>

      {/* Bottom Centered Documentary Subtitle */}
      <div
        style={{
          position: "absolute",
          bottom: 72,
          left: 120,
          right: 120,
          display: "flex",
          justifyContent: "center",
          opacity: textOpacity,
        }}
      >
        <div
          style={{
            padding: "14px 32px",
            backgroundColor: "rgba(6, 10, 19, 0.74)",
            borderBottom: "2px solid rgba(56, 189, 248, 0.65)",
            borderRadius: 8,
            fontFamily: FONT_ZH,
            fontSize: 34,
            fontWeight: 600,
            color: "#f8fafc",
            textAlign: "center",
            letterSpacing: "0.04em",
            lineHeight: 1.4,
            textShadow: "0 2px 12px rgba(0, 0, 0, 0.85)",
          }}
        >
          {scene.subtitle}
        </div>
      </div>

      {/* Neural Narration Audio delayed 16 frames after crossfade entry */}
      <Sequence from={16} durationInFrames={dur - 18}>
        <Audio src={staticFile(scene.audio)} volume={0.95} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const OsakaStationDoc: React.FC = () => {
  const globalFrame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const timelineProgress = Math.min(
    100,
    Math.max(0, (globalFrame / Math.max(1, durationInFrames - 1)) * 100)
  );
  const secondsElapsed = (globalFrame / 30).toFixed(1).padStart(4, "0");

  return (
    <AbsoluteFill style={{ backgroundColor: "#050811" }}>
      {/* Ambient Background Pad across entire 30s timeline */}
      <Audio
        src={staticFile("audio/ambient_pad.wav")}
        volume={(f) => {
          const fadeIn = interpolate(f, [0, 30], [0, 0.12], {
            extrapolateRight: "clamp",
          });
          const fadeOut = interpolate(
            f,
            [TOTAL_DURATION_FRAMES - 45, TOTAL_DURATION_FRAMES],
            [0.12, 0],
            { extrapolateLeft: "clamp" }
          );
          return Math.min(fadeIn, fadeOut);
        }}
      />

      {/* Overlapping 4 Scenes */}
      {SCENES.map((scene, idx) => (
        <Sequence
          key={scene.id}
          from={scene.from}
          durationInFrames={scene.durationInFrames}
        >
          <SceneLayer
            scene={scene}
            isFirst={idx === 0}
            isLast={idx === SCENES.length - 1}
          />
        </Sequence>
      ))}

      {/* Persistent Architectural Drafting HUD Border */}
      <div
        style={{
          position: "absolute",
          inset: 28,
          border: "1px solid rgba(148, 163, 184, 0.28)",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            position: "absolute",
            top: -1,
            left: -1,
            width: 24,
            height: 24,
            borderTop: "2.5px solid #38bdf8",
            borderLeft: "2.5px solid #38bdf8",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: -1,
            right: -1,
            width: 24,
            height: 24,
            borderTop: "2.5px solid #38bdf8",
            borderRight: "2.5px solid #38bdf8",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: -1,
            left: -1,
            width: 24,
            height: 24,
            borderBottom: "2.5px solid #38bdf8",
            borderLeft: "2.5px solid #38bdf8",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: -1,
            right: -1,
            width: 24,
            height: 24,
            borderBottom: "2.5px solid #38bdf8",
            borderRight: "2.5px solid #38bdf8",
          }}
        />
      </div>

      {/* Top-Right Spec Telemetry Pill */}
      <div
        style={{
          position: "absolute",
          top: 56,
          right: 62,
          display: "flex",
          alignItems: "center",
          gap: 14,
          padding: "8px 18px",
          backgroundColor: "rgba(10, 16, 28, 0.72)",
          border: "1px solid rgba(148, 163, 184, 0.38)",
          borderRadius: 6,
          fontFamily: FONT_MONO,
          fontSize: 14,
          fontWeight: 600,
          color: "#cbd5e1",
          letterSpacing: "0.08em",
          pointerEvents: "none",
        }}
      >
        <span>1080P · 30FPS</span>
        <span style={{ color: "#38bdf8" }}>|</span>
        <span>ANTIGRAVITY × COLAB</span>
        <span style={{ color: "#38bdf8" }}>|</span>
        <span style={{ color: "#7dd3fc" }}>{secondsElapsed}s / 30.0s</span>
      </div>

      {/* Bottom 3px Global Timeline Progress Bar */}
      <div
        style={{
          position: "absolute",
          bottom: 28,
          left: 28,
          right: 28,
          height: 3,
          backgroundColor: "rgba(148, 163, 184, 0.2)",
          pointerEvents: "none",
        }}
      >
        <div
          style={{
            width: `${timelineProgress}%`,
            height: "100%",
            backgroundColor: "#38bdf8",
            boxShadow: "0 0 10px rgba(56, 189, 248, 0.85)",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
