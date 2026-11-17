import React from "react";
import { Composition } from "remotion";
import { Edicao } from "./Edicao";
import T from "./tempos.json";

export const RemotionRoot: React.FC = () => (
  <Composition id="TrendPoca" component={Edicao} durationInFrames={T.quadros} fps={T.fps} width={T.largura} height={T.altura} />
);
