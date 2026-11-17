# Base da edição a partir do original, na régua de edicao/src/tempos.json:
# corte; velocidade por pontos (troca seca onde dois pontos dividem a mesma origem); abaixo de 0,45x os 60 q/s
# não bastam e o quadro intermediário sai por fluxo óptico (DIS, nos dois sentidos); empurrão lento de câmera;
# e o áudio original na MESMA curva (velocidade de fita: na câmera lenta o som desce junto).
# Sai na escala de entrega (2 = 2160 x 3840, a resolução nativa do iPhone).
# uso: python scripts/base.py <IMG_1977.MOV> <tempos.json> <pasta_saida>
import sys, os, json, glob, subprocess
import numpy as np, cv2

ORIG, TEMPOS, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
T = json.load(open(TEMPOS, encoding="utf-8"))
FPS, N = T["fps"], T["quadros"]
ESC = T.get("saida", {}).get("escala", 1)
W, H = T["largura"] * ESC, T["altura"] * ESC
O, PTS, E = T["origem"], T["velocidade"], T["empurrao"]
LIM_INTERP = T.get("interpolar", {}).get("abaixoDe", 0.45)
SR = 48000


def sm(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# régua origem -> saída: v(origem) em reta entre pontos; t(origem) = integral de 1/v
passo = 1e-4
s_grid = np.arange(PTS[0][0], PTS[-1][0] + passo / 2, passo)
v_grid = np.full_like(s_grid, PTS[-1][1])
for (sa, va), (sb, vb) in zip(PTS, PTS[1:]):
    if sb <= sa:
        continue
    m = (s_grid >= sa) & (s_grid < sb)
    v_grid[m] = va + (vb - va) * (s_grid[m] - sa) / (sb - sa)
t_grid = np.concatenate([[0.0], np.cumsum((1 / v_grid[1:] + 1 / v_grid[:-1]) / 2 * passo)])
print(f"duração {t_grid[-1]:.4f} s para {N} quadros ({N / FPS:.4f} s)")
assert abs(t_grid[-1] - N / FPS) < 1 / FPS
assert s_grid[-1] <= O["limite"] + 0.01, "a régua passa do limite (a mão entra no quadro)"
origem_de = lambda t: np.interp(t, t_grid, s_grid)
vel_de = lambda s: float(np.interp(s, s_grid, v_grid))

# 1) quadros do trecho, nativos a 59,94, HDR HLG convertido para SDR, em 1,1x da saída para o empurrão
Q = os.path.join(OUT, "q")
os.makedirs(Q, exist_ok=True)
T0 = O["inicio"] - 0.1
W0, H0 = round(W * 1.1), round(H * 1.1)
tom = (f"zscale=w={W0}:h={H0}:filter=spline36:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{T0:.3f}", "-i", ORIG, "-t", f"{s_grid[-1] - T0 + 0.2:.3f}",
                "-vf", tom, "-q:v", "1", "-qmin", "1", os.path.join(Q, "%05d.jpg")], check=True)
arqs = sorted(glob.glob(os.path.join(Q, "*.jpg")))
print("quadros de origem:", len(arqs))

cache = {}
def quadro(k):
    k = min(len(arqs) - 1, max(0, k))
    if k not in cache:
        if len(cache) > 6:
            cache.pop(next(iter(cache)))
        cache[k] = cv2.imread(arqs[k])
    return cache[k]

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
fluxos = {}
def fluxo(k):
    """fluxo k -> k+1 e k+1 -> k, calculado em meia resolução e levado à resolução cheia"""
    if k not in fluxos:
        a = cv2.cvtColor(quadro(k), cv2.COLOR_BGR2GRAY); b = cv2.cvtColor(quadro(k + 1), cv2.COLOR_BGR2GRAY)
        a2 = cv2.resize(a, (W0 // 2, H0 // 2), interpolation=cv2.INTER_AREA); b2 = cv2.resize(b, (W0 // 2, H0 // 2), interpolation=cv2.INTER_AREA)
        up = lambda f: cv2.resize(f, (W0, H0), interpolation=cv2.INTER_LINEAR) * 2.0
        fluxos.clear()
        fluxos[k] = (up(dis.calc(a2, b2, None)), up(dis.calc(b2, a2, None)))
    return fluxos[k]

gy, gx = np.mgrid[0:H0, 0:W0].astype(np.float32)
def intermediario(k, a):
    """quadro na fração a entre k e k+1: cada lado puxado pelo seu fluxo e misturado pelo peso da distância"""
    f01, f10 = fluxo(k)
    i0 = cv2.remap(quadro(k), gx - a * f01[..., 0], gy - a * f01[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    i1 = cv2.remap(quadro(k + 1), gx - (1 - a) * f10[..., 0], gy - (1 - a) * f10[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return cv2.addWeighted(i0, 1 - a, i1, a, 0)

# 2) quadro de saída na régua, com o empurrão em volta da âncora
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "8", "-preset", "slow", "-pix_fmt", "yuv420p",
                        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        os.path.join(OUT, "base.mp4")], stdin=subprocess.PIPE)
ax, ay = E["ancora"][0] * ESC, E["ancora"][1] * ESC
k0 = W / W0
mapa = []
for f in range(N):
    t = f / FPS
    s = float(origem_de(t))
    kf = (s - T0) * O["fps"]
    k, a = int(np.floor(kf)), kf - np.floor(kf)
    v = vel_de(s)
    if v < LIM_INTERP and 0.04 < a < 0.96:
        img, modo = intermediario(k, a), "fluxo"
    else:
        k = int(round(kf)); img, modo = quadro(k), "origem"
    mapa.append({"q": f, "t": round(t, 4), "origem": round(s, 4), "v": round(v, 3), "k": round(kf, 2), "modo": modo})
    z = E["de"] + (E["ate"] - E["de"]) * sm(t / (N / FPS))
    M = np.float32([[z * k0, 0, ax * (1 - z)], [0, z * k0, ay * (1 - z)]])
    enc.stdin.write(cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
enc.stdin.close()
enc.wait()
json.dump(mapa, open(os.path.join(OUT, "mapa_quadros.json"), "w"), indent=0)
print("quadros por fluxo:", sum(1 for m in mapa if m["modo"] == "fluxo"))

# 3) áudio na mesma régua, entrada de 30 ms e saída de 250 ms
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", ORIG, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
aud = np.frombuffer(pcm, np.float32).reshape(-1, 2)
S = origem_de(np.arange(N * SR // FPS) / SR) * SR
y = np.stack([np.interp(S, np.arange(len(aud)), aud[:, c]) for c in (0, 1)], axis=1)
env = np.ones(len(y))
ini, fim = int(0.03 * SR), int(0.25 * SR)
env[:ini] = np.linspace(0, 1, ini)
env[-fim:] = np.linspace(1, 0, fim)
y = (y * env[:, None]).astype(np.float32)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                os.path.join(OUT, "audio.wav")], input=y.tobytes(), check=True)
print("base pronta:", os.path.join(OUT, "base.mp4"), f"{W}x{H}")
