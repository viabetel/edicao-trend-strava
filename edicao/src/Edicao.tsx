import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/SpaceGrotesk";
import T from "./tempos.json";
import G from "./sticker.json";

// Base (corte, rampa de velocidade e empurrão) vem pronta de scripts/base.py; aqui entra só o sticker do Kivow,
// o arranjo 9:16 da variante tinta do "Minha assinatura" desenhado no Figma (coordenadas do quadro 1080 x 1920).
const { fontFamily } = loadFont("normal", { weights: ["300"], subsets: ["latin"] });

const clamp = (x: number) => Math.max(0, Math.min(1, x));
const sm = (x: number) => { const c = clamp(x); return c * c * (3 - 2 * c); };
const chegada = (x: number, m = 3) => 1 - Math.pow(1 - clamp(x), m);

/** acende, sobe 14 px e sai de um foco de 6 px em 0,4 s */
const entrada = (t: number, t0: number, dur = 0.4): React.CSSProperties => {
  const e = chegada((t - t0) / dur);
  return { opacity: e, transform: `translateY(${((1 - e) * 14).toFixed(2)}px)`, filter: e < 1 ? `blur(${((1 - e) * 6).toFixed(2)}px)` : undefined };
};

const Peca: React.FC<{ p: { src: string; x: number; y: number; w: number; h: number }; estilo: React.CSSProperties }> = ({ p, estilo }) => (
  <div style={{ position: "absolute", left: p.x, top: p.y, width: p.w, height: p.h, ...estilo }}>
    <Img src={staticFile(p.src)} style={{ width: p.w, height: p.h, display: "block" }} />
  </div>
);

// régua origem -> saída, a mesma de scripts/base.py: v(origem) em reta entre pontos, t(origem) = integral de 1/v
const PTS = T.velocidade as [number, number][];
const velDe = (s: number) => {
  for (let i = 1; i < PTS.length; i++) {
    const [sa, va] = PTS[i - 1], [sb, vb] = PTS[i];
    if (sb > sa && s >= sa && s < sb) return va + ((vb - va) * (s - sa)) / (sb - sa);
  }
  return PTS[PTS.length - 1][1];
};
const saidaDe = (origem: number) => {
  const passo = 1e-4;
  let t = 0;
  for (let s = PTS[0][0]; s < origem; s += passo) t += passo / velDe(s + passo / 2);
  return t;
};
/** primeiro instante com a lente coberta: tudo entra junto aqui */
export const T_IMPACTO = saidaDe(T.sticker.origemImpacto);

const Sticker: React.FC<{ t: number }> = ({ t }) => {
  const S = T.sticker, t0 = T_IMPACTO, fim = T.quadros / T.fps;
  const pTraco = sm((t - t0) / S.traco);
  const eConta = chegada((t - t0) / S.conta, 3);
  const valor = (G.valor.final * eConta).toFixed(2).replace(".", ",");
  const aNumero = chegada((t - t0) / 0.2);
  const ePartida = chegada((t - t0) / 0.2);
  const deriva = -S.deriva * sm((t - t0 - S.traco) / (fim - t0 - S.traco));
  const traco = (d: string, x: number, y: number, esc: number, sw: number, cor: string) => (
    <path d={d} transform={`translate(${x} ${y}) scale(${esc})`} fill="none" stroke={cor} strokeWidth={sw} strokeLinecap="butt" strokeLinejoin="miter"
      pathLength={1} strokeDasharray={pTraco < 1 ? `${pTraco} 1` : undefined} />
  );
  const quadrado = (q: { x: number; y: number; lado: number }, cor: string) => (
    <rect x={q.x} y={q.y} width={q.lado} height={q.lado} fill={cor}
      style={{ transformBox: "fill-box", transformOrigin: "center", transform: `scale(${(0.6 + 0.4 * ePartida).toFixed(3)})` }} opacity={ePartida} />
  );
  const I = G.instancia;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, transformOrigin: "0 0",
      transform: `translate(${I.x}px, ${(I.y + deriva).toFixed(2)}px) scale(${I.escala})` }}>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        {pTraco > 0 ? <>
          {quadrado(G.rastroPartida, G.creme)}
          {traco(G.rastro.d, G.rastro.x, G.rastro.y, G.rastro.escala, G.rastro.sw, G.creme)}
          {traco(G.traco.d, G.traco.x, G.traco.y, G.traco.escala, G.traco.sw, G.verdeKivow)}
          {quadrado(G.partida, G.verdeKivow)}
        </> : null}
        {aNumero > 0 ? <g opacity={aNumero} style={{ filter: aNumero < 1 ? `blur(${((1 - aNumero) * 6).toFixed(2)}px)` : undefined }}>
          <text x={G.valor.fimX} y={G.valor.base} textAnchor="end" fontFamily={fontFamily} fontWeight={300} fontSize={G.valor.corpo} fill={G.tinta}>{valor}</text>
          <text x={G.unidade.x} y={G.unidade.base} fontFamily={fontFamily} fontWeight={300} fontSize={G.unidade.corpo} fill={G.tinta}>{G.unidade.texto}</text>
        </g> : null}
      </svg>
      <Peca p={G.rotulo} estilo={entrada(t, t0, S.entrada)} />
      <Peca p={G.ritmo} estilo={entrada(t, t0, S.entrada)} />
      <Peca p={G.tempo} estilo={entrada(t, t0, S.entrada)} />
      <Peca p={G.marca} estilo={entrada(t, t0, S.entrada)} />
    </div>
  );
};

export const Edicao: React.FC = () => {
  const t = useCurrentFrame() / T.fps;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <OffthreadVideo src={staticFile("base.mp4")} muted />
      {t >= T_IMPACTO ? <Sticker t={t} /> : null}
    </AbsoluteFill>
  );
};
