import argparse
import json
import re
import subprocess
from pathlib import Path


def argumentos():
    parser = argparse.ArgumentParser(description="Auditoria numérica da entrega da edição")
    parser.add_argument("--mapa", required=True)
    parser.add_argument("--tempos", required=True)
    parser.add_argument("--video", required=True)
    parser.add_argument("--loudness", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def ffprobe(video):
    processo = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=codec_type,width,height,r_frame_rate,nb_frames:format=duration",
            "-of",
            "json",
            video,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(processo.stdout)


def primeiro_momento(mapa, origem):
    for quadro in mapa:
        if quadro["origem"] >= origem:
            return quadro
    return None


def ler_loudness(caminho):
    texto = Path(caminho).read_text(encoding="utf-8")
    valores = {}
    for chave, valor in re.findall(r"^\s*(I|LRA|Peak):\s+([-+0-9.]+)", texto, re.MULTILINE):
        valores[chave] = float(valor)
    return valores


def main():
    args = argumentos()
    tempos = json.loads(Path(args.tempos).read_text(encoding="utf-8"))
    mapa = json.loads(Path(args.mapa).read_text(encoding="utf-8"))
    ficha = ffprobe(args.video)
    loudness = ler_loudness(args.loudness)

    stream_video = next(stream for stream in ficha["streams"] if stream["codec_type"] == "video")
    stream_audio = next((stream for stream in ficha["streams"] if stream["codec_type"] == "audio"), None)
    fps_num, fps_den = [int(parte) for parte in stream_video["r_frame_rate"].split("/")]
    fps = fps_num / fps_den
    duracao = float(ficha["format"]["duration"])
    origem = tempos["origem"]
    passos = tempos["passos"]
    lento = [quadro for quadro in mapa if quadro["v"] < tempos["interpolar"]["abaixoDe"]]
    metodos = {}
    for quadro in lento:
        metodos[quadro["modo"]] = metodos.get(quadro["modo"], 0) + 1

    primeiro_lento = lento[0] if lento else None
    soltura = [
        quadro
        for quadro in mapa
        if passos["peNoAltoCentro"] <= quadro["origem"] <= passos["peNoAltoTopo"]
    ]
    impacto = primeiro_momento(mapa, tempos["sticker"]["origemImpacto"])
    duracao_esperada = tempos["quadros"] / tempos["fps"]
    erros = []
    avisos = []

    if stream_video["width"] != tempos["largura"] * tempos["saida"]["escala"]:
        erros.append("largura do master diferente da especificação")
    if stream_video["height"] != tempos["altura"] * tempos["saida"]["escala"]:
        erros.append("altura do master diferente da especificação")
    if abs(fps - tempos["fps"]) > 0.01:
        erros.append("fps do master diferente da especificação")
    if abs(duracao - duracao_esperada) > 1 / tempos["fps"]:
        erros.append("duração do master fora da tolerância de um quadro")
    if primeiro_lento is None:
        erros.append("não foi encontrado o início do slow motion")
    elif abs(primeiro_lento["origem"] - passos["pertoDaPoca"]) > 2 / tempos["origem"]["fps"]:
        erros.append("início do slow motion fora da tolerância")
    if not soltura:
        erros.append("não foi encontrado quadro da soltura no ponto alto")
    if impacto is None:
        erros.append("não foi encontrado o primeiro quadro do sticker")
    if loudness.get("I") is None:
        avisos.append("loudness não foi lido")
    elif abs(loudness["I"] + 14) > 1.5:
        erros.append("loudness integrado fora de -14 ±1,5 LUFS")
    if loudness.get("Peak") is not None and loudness["Peak"] > -1.0:
        avisos.append("pico medido acima de -1 dBFS; conferir true peak")
    if not stream_audio:
        erros.append("master sem áudio")
    if metodos.get("fluxo", 0):
        avisos.append("há quadros de fallback por fluxo óptico no slow motion")
    if len(lento) and metodos.get("rife", 0) / len(lento) < 0.8:
        avisos.append("menos de 80% do slow motion usa RIFE")

    relatorio = {
        "ok": not erros,
        "erros": erros,
        "avisos": avisos,
        "video": {
            "width": stream_video["width"],
            "height": stream_video["height"],
            "fps": round(fps, 4),
            "duration": round(duracao, 4),
            "frames": stream_video.get("nb_frames"),
            "audio": bool(stream_audio),
        },
        "loudness": loudness,
        "slow_motion": {
            "frames": len(lento),
            "methods": metodos,
            "first_frame": primeiro_lento,
            "release_frames": soltura,
            "sticker_frame": impacto,
        },
    }
    Path(args.out).write_text(json.dumps(relatorio, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))
    if erros:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
