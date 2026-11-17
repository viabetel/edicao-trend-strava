# Base da edição a partir do original, na régua de edicao/src/tempos.json:
# corte, rampa de velocidade (1x, 0,5x na pisada, 0,75x na lente molhada), empurrão lento de câmera
# e o áudio original na MESMA curva (velocidade variável de fita: na câmera lenta o som desce junto).
# uso: python scripts/base.py <IMG_1977.MOV> <tempos.json> <pasta_saida>
import sys, os, json, glob, subprocess
import numpy as np, cv2

ORIG, TEMPOS, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
T = json.load(open(TEMPOS, encoding="utf-8"))
FPS, N, W, H = T["fps"], T["quadros"], T["largura"], T["altura"]
O, VK, E = T["origem"], T["velocidade"], T["empurrao"]
SR = 48000


def sm(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def v(t):
    for (t0, v0), (t1, v1) in zip(VK, VK[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * sm((t - t0) / (t1 - t0) if t1 > t0 else 1)
    return VK[-1][1]


# tempo de origem para cada amostra de áudio da saída (integral da velocidade)
tt = np.arange(N * SR // FPS) / SR
vv = np.array([v(t) for t in tt])
S = O["inicio"] + np.concatenate([[0.0], np.cumsum((vv[1:] + vv[:-1]) / 2 / SR)])
print(f"origem: {S[0]:.3f} a {S[-1]:.3f} s (limite {O['limite']})")
assert S[-1] <= O["limite"] + 0.01, "a régua passa do limite (a mão entra no quadro)"

# 1) quadros do trecho, nativos a 59,94, HDR HLG convertido para SDR, em 1,1x para o empurrão
Q = os.path.join(OUT, "q")
os.makedirs(Q, exist_ok=True)
T0 = O["inicio"] - 0.1
W0, H0 = round(W * 1.1), round(H * 1.1)
tom = (f"zscale=w={W0}:h={H0}:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
       "zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{T0:.3f}", "-i", ORIG, "-t", f"{O['limite'] - T0 + 0.2:.3f}",
                "-vf", tom, "-q:v", "2", os.path.join(Q, "%05d.jpg")], check=True)
arqs = sorted(glob.glob(os.path.join(Q, "*.jpg")))
print("quadros de origem:", len(arqs))

# 2) quadro de saída = quadro de origem mais próximo na régua, com o empurrão em volta da âncora
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p",
                        os.path.join(OUT, "base.mp4")], stdin=subprocess.PIPE)
ax, ay = E["ancora"]
k0 = W / W0
cache = {}
mapa = []
for f in range(N):
    t = f / FPS
    s = S[min(len(S) - 1, round(t * SR))]
    k = min(len(arqs) - 1, max(0, round((s - T0) * O["fps"])))
    mapa.append((f, round(s, 4), k))
    if k not in cache:
        cache.clear()
        cache[k] = cv2.imread(arqs[k])
    z = E["de"] + (E["ate"] - E["de"]) * sm(t / (N / FPS))
    M = np.float32([[z * k0, 0, ax * (1 - z)], [0, z * k0, ay * (1 - z)]])
    enc.stdin.write(cv2.warpAffine(cache[k], M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
enc.stdin.close()
enc.wait()
json.dump(mapa, open(os.path.join(OUT, "mapa_quadros.json"), "w"))

# 3) áudio na mesma régua (interpolação na curva de tempo), entrada de 30 ms e saída de 250 ms
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", ORIG, "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.float32).reshape(-1, 2)
idx = S * SR
y = np.stack([np.interp(idx, np.arange(len(a)), a[:, c]) for c in (0, 1)], axis=1)
env = np.ones(len(y))
ini, fim = int(0.03 * SR), int(0.25 * SR)
env[:ini] = np.linspace(0, 1, ini)
env[-fim:] = np.linspace(1, 0, fim)
y = (y * env[:, None]).astype(np.float32)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                os.path.join(OUT, "audio.wav")], input=y.tobytes(), check=True)
print("base pronta:", os.path.join(OUT, "base.mp4"))
