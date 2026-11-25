import React from "react";
import { Composition } from "remotion";
import { OsakaStationDoc } from "./OsakaStationDoc";
import { FPS, TOTAL_DURATION_FRAMES } from "./scenes";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="OsakaStationDoc"
      component={OsakaStationDoc}
      durationInFrames={TOTAL_DURATION_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
