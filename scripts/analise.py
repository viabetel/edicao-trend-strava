# Lê a prévia (1080x1920, 30 q/s) e gera: folha do vídeo inteiro a 2 q/s, folha do trecho final a 10 q/s,
# quadros inteiros a cada 3 s, gráfico de luz / diferença / movimento por quadro e um resumo em JSON.
# uso: python scripts/analise.py <previa.mp4> <pasta>
import sys, os, json
import numpy as np, cv2
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

V, OUT = sys.argv[1:3]
os.makedirs(os.path.join(OUT, "quadros"), exist_ok=True)
cap = cv2.VideoCapture(V)
FPS = cap.get(cv2.CAP_PROP_FPS) or 30
peq = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    peq.append(cv2.resize(f, (270, 480), interpolation=cv2.INTER_AREA))
    i = len(peq) - 1
    if i % int(round(3 * FPS)) == 0:
        cv2.imwrite(os.path.join(OUT, "quadros", f"t{i / FPS:04.1f}s.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 88])
n = len(peq)
t = np.arange(n) / FPS

def folha(idx, w, h, cols, nome):
    th = []
    for i in idx:
        im = cv2.resize(peq[i], (w, h))
        cv2.rectangle(im, (0, 0), (w, 18), (0, 0, 0), -1)
        cv2.putText(im, f"{i / FPS:.1f}s", (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        th.append(im)
    while len(th) % cols:
        th.append(np.full((h, w, 3), 255, np.uint8))
    linhas = [np.hstack(th[k:k + cols]) for k in range(0, len(th), cols)]
    cv2.imwrite(os.path.join(OUT, nome), np.vstack(linhas), [cv2.IMWRITE_JPEG_QUALITY, 85])

folha([i for i in range(0, n, int(round(FPS / 2)))], 180, 320, 10, "folha_inteiro_2qps.jpg")
ini = max(0, n - int(round(10 * FPS)))
folha([i for i in range(ini, n, int(round(FPS / 10)))], 150, 267, 12, "folha_ultimos10s_10qps.jpg")

cinza = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in peq]
luz = np.array([g.mean() for g in cinza])
dif = np.array([0.0] + [float(np.abs(cinza[i] - cinza[i - 1]).mean()) for i in range(1, n)])
mov = [0.0]
for i in range(1, n):
    (dx, dy), _ = cv2.phaseCorrelate(cinza[i - 1].copy(), cinza[i].copy())
    mov.append(float(np.hypot(dx, dy)) * 4)  # px por quadro na escala 1080
mov = np.array(mov)
fig, ax = plt.subplots(3, 1, figsize=(16, 8), sharex=True)
ax[0].plot(t, luz, "k"); ax[0].set_ylabel("luz média")
ax[1].plot(t, dif, "k"); ax[1].set_ylabel("diferença entre quadros")
ax[2].plot(t, mov, "k"); ax[2].set_ylabel("movimento global px/q (1080)")
ax[2].set_xlabel("segundos"); ax[2].set_xticks(np.arange(0, t[-1] + 1, 1))
for a in ax:
    a.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "grafico_luz_diferenca_movimento.png"), dpi=70)
picos = [round(float(t[i]), 2) for i in np.argsort(dif)[::-1][:10]]
json.dump({"quadros_previa": n, "fps_previa": FPS, "duracao_s": round(n / FPS, 2),
           "maiores_diferencas_s": sorted(picos), "luz_min": round(float(luz.min()), 1), "luz_max": round(float(luz.max()), 1)},
          open(os.path.join(OUT, "resumo.json"), "w"), indent=1)
print("ok", n)
