# Superprompt v5 · câmera lenta perto da poça, soltando com o pé no alto

## 1. O pedido (palavras do Nicácio)

- "deveria ficar um pouco mais lento"
- "o pé quando estiver tudo pra cima no último passo que vc solta"
- "vc ainda tá fazendo o slow motion no ponto errado, deveria ser bem próximo da poça e bem melhor desenvolvido"
- da rodada anterior: "comece e pare subitamente", "depois ela volta quando a água e o gráfico já estiverem desenvolvidos dando mais tempo pra ler tudo", "qualidade máxima"

## 2. O que estava errado na v4 (medido)

| Ponto | v4 | Problema |
|---|---|---|
| Início do lento | 32,43 s, na pisada 1 | corredor ainda longe: corpo inteiro na tela, cerca de 30 % da altura. O lento gastava tempo longe da câmera |
| Velocidade mais lenta | 0,2x | pouco lento para o clímax |
| Soltura | 33,13 s | o último pé ainda estava baixo (centro da sola em y 882 de 1920) e subindo |
| Ponto mais alto do pé | 33,20 a 33,22 s, centro da sola em y 820, topo em y 686 | ficou fora do lento: passou em 1x |

## 3. Mapa físico medido (original a 59,94 q/s, coordenadas em 1080 x 1920)

| Origem (s) | O que acontece | Medida |
|---|---|---|
| 30,0 | corredor parado ao fundo | início do corte |
| 32,43 | pisada 1, longe | golpe no som em 32,435 |
| 32,80 | perto da poça: o pé da pisada 2 vem descendo; pernas ocupam a metade de baixo da tela | |
| 32,867 | pisada 2 toca a água bem na frente da lente | golpe no som em 32,85 |
| 33,05 | o último pé sai da água e começa a subir | |
| 33,15 | sola preta aparece grande, subindo | centro em y 982 |
| 33,201 | **pé no ponto mais alto (centro)** | centro da sola em y 820 |
| 33,218 | **pé no ponto mais alto (topo)** | topo da sola em y 686 |
| 33,25 | descendo | centro em y 1106 |
| 33,27 | pousa ao lado da lente | golpe mais forte do som, −9,3 dB |
| 33,351 | a água cobre a lente | luz salta de 140 para 174 |

## 4. Curva de velocidade v5 (pontos [origem, velocidade], troca seca onde dois pontos dividem a origem)

| Trecho de origem | Velocidade | Saída | Por quê |
|---|---|---|---|
| 30,00 a 32,80 | 1x | 0,00 a 2,80 s | a corrida chega em tempo real |
| 32,80 | **liga seco** 1x para 0,25x | 2,80 s | já perto da poça, com o pé da pisada 2 descendo |
| 32,80 a 33,15 | desce de 0,25x a 0,12x | 2,80 a 4,78 s | pisada 2 e respingo em câmera lenta, ficando mais lento a cada quadro |
| 33,15 a 33,21 | 0,12x | 4,78 a 5,28 s | o último pé sobe até o alto, bem lento |
| 33,21 | **solta seco** para 1x com o pé no alto | 5,28 s | entre o centro mais alto (33,201) e o topo mais alto (33,218) |
| 33,21 a 34,35 | 1x | 5,28 a 6,42 s | desce, pousa (5,34 s) e a água cobre a lente (5,42 s, 4 quadros depois da soltura); o sticker se monta em 1 s |
| 34,35 a 36,11 | 0,5x | 6,42 a 9,93 s | câmera lenta volta para a leitura |

Total 9,93 s (298 quadros a 30 q/s). A câmera lenta dura 2,48 s, toda dentro da aproximação final.

## 5. Quadros intermediários (qualidade máxima)

- Abaixo de 0,45x, os 60 q/s não bastam. A 0,12x, cada par de quadros reais vira cerca de 4 quadros na saída.
- Método principal: **RIFE v4.6** (rife-ncnn-vulkan, CPU, modo UHD), na resolução cheia de trabalho (2376 x 4224), com o instante exato de cada quadro (fração entre os dois reais).
- Reserva automática: fluxo óptico DIS nos dois sentidos, se o RIFE falhar. O mapa de quadros registra o método de cada um.
- Proibido duplicar quadro: dá trepidação.

## 6. Som

- Mesma régua da imagem, em velocidade de fita.
- A 0,25x e a 0,12x, a pisada 2 vira um baque grave e o ambiente quase some.
- Na soltura o som volta seco ao tom real e o pouso (−9,3 dB) estoura no tempo certo, logo antes da água na lente.
- Master em −14 LUFS e pico −1,5 dBTP; AAC de 320 kbps.

## 7. Sticker

É o da v3, sem mudança (Figma Kivow 676:465): Minha assinatura em tinta, informações a 125 %. Tudo entra junto no primeiro quadro claro da água na lente:
- rótulo, Ritmo, Tempo e marca K: acendem, sobem 14 px e saem do foco de 6 px em 0,4 s;
- traço se desenha em 1,0 s;
- 8,01 conta em 0,7 s;
- depois sobe 6 px até o fim.

## 8. Câmera e saída

- Empurrão contínuo de 100 % para 106 % no vídeo todo, âncora (540, 1000).
- Master em 2160 x 3840: base em 4K e Remotion com escala 2, ProRes HQ, depois H.264 High CRF 12. A prévia 1080 vai para o celular.

## 9. Critérios de aceite (medidos antes de entregar)

1. O lento liga no quadro de origem 32,80 s ±1 quadro (60 q/s). Antes disso, nenhum quadro sintético.
2. A soltura cai entre 33,201 e 33,218 s, com o pé no ponto mais alto.
3. Da soltura à água na lente: no máximo 5 quadros de saída.
4. O sticker aparece no primeiro quadro claro e nenhum antes.
5. Folha de todos os quadros do trecho lento (2,8 a 5,4 s), olhada em 2x: sem pé deformado, sem perna dupla, sem respingo derretido.
6. Duração de 298 quadros; master em 2160 x 3840; loudness de −14 ±1,5 LUFS.

## 10. Ordem

Régua no Figma → `tempos.json` → base (RIFE) → Remotion 4K → folhas e auditoria → entrega: prévia no celular e master em Downloads.
