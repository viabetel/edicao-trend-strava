# Edição estilo trend do Strava: IMG_1977

Vídeo bruto do iPhone para ser editado no estilo das trends do Strava. O pedido ao ChatGPT está em **[PEDIDO_AO_CHATGPT.md](PEDIDO_AO_CHATGPT.md)**.

## O vídeo

| | |
|---|---|
| Arquivo | `IMG_1977.MOV`, iPhone 14 |
| Duração | 39,62 s (2376 quadros a 59,94 q/s) |
| Imagem | 2160 x 3840 na vertical (gravado 3840 x 2160 com rotação −90) |
| Cor | HEVC 10 bits, HDR HLG (BT.2020) |
| Áudio | AAC estéreo 48 kHz, som ambiente da gravação |
| Tamanho | 527 MB |

- **Original:** release [`original`](https://github.com/viabetel/edicao-trend-strava/releases/tag/original), porque o GitHub não aceita arquivo acima de 100 MB no repositório.
- **Prévia para assistir:** [`previa/IMG_1977_1080x1920.mp4`](previa/IMG_1977_1080x1920.mp4), 1080 x 1920, SDR, 30 q/s.

## Como ler o vídeo sem tocar

Gerado na nuvem pelo workflow [`analise.yml`](.github/workflows/analise.yml):

| Arquivo | O que mostra |
|---|---|
| [`analise/folha_inteiro_2qps.jpg`](analise/folha_inteiro_2qps.jpg) | o vídeo inteiro, 2 quadros por segundo, com o tempo em cada quadro |
| [`analise/folha_ultimos10s_10qps.jpg`](analise/folha_ultimos10s_10qps.jpg) | os últimos 10 s, 10 quadros por segundo (chegada e respingo) |
| [`analise/quadros/`](analise/quadros/) | quadros inteiros 1080 x 1920 a cada 3 s |
| [`analise/grafico_luz_diferenca_movimento.png`](analise/grafico_luz_diferenca_movimento.png) | luz, diferença entre quadros e movimento da câmera, segundo a segundo |
| [`analise/resumo.json`](analise/resumo.json) | os 10 instantes de maior mudança e a faixa de luz |
| [`analise/audio_onda.png`](analise/audio_onda.png), [`analise/audio_espectro.png`](analise/audio_espectro.png), [`analise/audio_loudness.txt`](analise/audio_loudness.txt) | o áudio original: volume a cada 100 ms, espectro e loudness |
| [`analise/ficha_original.json`](analise/ficha_original.json) | ficha técnica do original (ffprobe) |

## O que acontece no vídeo

Câmera no chão, rente a uma poça d'água, à noite. A poça espelha a rua iluminada: postes, palmeiras, uma cobertura de metal à esquerda e um muro claro com grafite à direita. Tempos medidos na folha e no gráfico, na prévia a 30 q/s:

| Trecho | O que acontece | Medida |
|---|---|---|
| 0,0 a 6,0 s | o celular é ajeitado no chão; a imagem treme | picos de movimento em 0,2, 1,0 e 3,8 s |
| 6,0 a 30,0 s | câmera parada; a pessoa espera de pé, pequena, à direita, ao fundo | diferença entre quadros perto de 0; ruído isolado no áudio em 13,4 s |
| 30,0 a 31,0 s | a pessoa sai correndo do fundo em direção à câmera | ainda pequena na tela |
| 31,0 a 32,5 s | a corrida cresce na tela, com o reflexo dela na poça | |
| 32,5 a 33,2 s | os pés entram na poça e levantam água | primeiro respingo em 32,5 s |
| 33,2 a 33,4 s | o tênis branco pisa ao lado da câmera; a água cobre a lente | maior mudança do vídeo (33,23 a 33,37 s); áudio no pico, −15,6 dBFS |
| 33,4 a 37,5 s | lente molhada: a imagem fica clara, com gotas e a rua desfocada atrás | luz média sobe de 62 para cerca de 158; imagem quase parada |
| 37,5 a 39,6 s | uma mão pega o celular; fim sem uso | movimento até 180 px/q |

O trecho útil de ação tem cerca de 3,4 s (30,0 a 33,4 s). A lente molhada (33,4 a 37,5 s) é um fundo claro e parado de 4 s logo depois do respingo.

Áudio: só som ambiente, sem música. Integrado em −23 LUFS, pico −0,6 dBFS. O passo na poça em 33,3 s é o único golpe forte antes do manuseio final (gráfico em [`analise/audio_onda.png`](analise/audio_onda.png)).

## Ainda não temos

- os dados da corrida: print do Strava ou GPX, distância, tempo, pace e elevação;
- a música que vai na edição;
- o @ e o texto que entram na peça.
