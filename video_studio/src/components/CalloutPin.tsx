import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { CalloutSpec } from "../scenes";

interface CalloutPinProps {
  callout: CalloutSpec;
  sceneDuration: number;
}

const FONT_ZH =
  "'Microsoft YaHei', 'PingFang SC', 'Noto Sans SC', 'SimHei', sans-serif";
const FONT_MONO = "'Consolas', 'JetBrains Mono', 'Courier New', monospace";

export const CalloutPin: React.FC<CalloutPinProps> = ({
  callout,
  sceneDuration,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - callout.delayFrames;
  if (localFrame < 0) {
    return null;
  }

  const entry = spring({
    frame: localFrame,
    fps,
    config: { damping: 16, stiffness: 120, mass: 0.7 },
  });

  // Gentle exit before cross-dissolve tail
  const fadeOut = interpolate(
    frame,
    [sceneDuration - 24, sceneDuration - 8],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const opacity = Math.min(1, entry) * fadeOut;
  if (opacity <= 0.01) {
    return null;
  }

  // Convert percentage anchor into 1920x1080 coordinates
  const cx = (callout.xPct / 100) * 1920;
  const cy = (callout.yPct / 100) * 1080;

  const isRight = callout.cardAlign === "right";
  const elbowX = isRight ? cx + 44 : cx - 44;
  const elbowY = cy - 36;
  const endX = isRight ? cx + 128 : cx - 128;
  const endY = elbowY;

  const pathLen = 148;
  const dashOffset = interpolate(entry, [0, 1], [pathLen, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Subtle radar pulse on target ring
  const pulse = 1 + 0.18 * Math.sin(localFrame * 0.14);

  const cardWidth = 340;
  const cardLeft = isRight ? endX + 10 : endX - cardWidth - 10;
  const cardTop = endY - 38;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        opacity,
      }}
    >
      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: "absolute", inset: 0 }}
      >
        <defs>
          <filter id={`glow-${callout.id}`} x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Outer animated pulse ring */}
        <circle
          cx={cx}
          cy={cy}
          r={14 * pulse}
          fill="rgba(56, 189, 248, 0.12)"
          stroke="rgba(56, 189, 248, 0.72)"
          strokeWidth={1.6}
        />

        {/* Crisp inner target dot */}
        <circle
          cx={cx}
          cy={cy}
          r={5.5}
          fill="#38bdf8"
          stroke="#e0f2fe"
          strokeWidth={1.8}
          filter={`url(#glow-${callout.id})`}
        />

        {/* Animated polyline leader */}
        <polyline
          points={`${cx},${cy} ${elbowX},${elbowY} ${endX},${endY}`}
          fill="none"
          stroke="#38bdf8"
          strokeWidth={2}
          strokeDasharray={pathLen}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Terminal node dot */}
        <circle cx={endX} cy={endY} r={3.5} fill="#7dd3fc" />
      </svg>

      {/* Telemetry frosted-glass label card */}
      <div
        style={{
          position: "absolute",
          left: cardLeft,
          top: cardTop,
          width: cardWidth,
          padding: "11px 16px",
          backgroundColor: "rgba(10, 16, 28, 0.78)",
          border: "1px solid rgba(56, 189, 248, 0.55)",
          borderLeft: isRight ? "3px solid #38bdf8" : "1px solid rgba(56, 189, 248, 0.55)",
          borderRight: !isRight ? "3px solid #38bdf8" : "1px solid rgba(56, 189, 248, 0.55)",
          borderRadius: 6,
          boxShadow: "0 10px 28px rgba(0, 0, 0, 0.48)",
          transform: `translateY(${interpolate(entry, [0, 1], [10, 0])}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONT_ZH,
            fontSize: 20,
            fontWeight: 700,
            color: "#f8fafc",
            letterSpacing: "0.04em",
            lineHeight: 1.3,
          }}
        >
          {callout.label}
        </div>
        <div
          style={{
            fontFamily: `${FONT_MONO}, ${FONT_ZH}`,
            fontSize: 13.5,
            fontWeight: 500,
            color: "#7dd3fc",
            marginTop: 4,
            letterSpacing: "0.03em",
          }}
        >
          {callout.detail}
        </div>
      </div>
    </div>
  );
};
