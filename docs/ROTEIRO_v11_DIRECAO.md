# Roteiro v11 · a água revela a corrida

## Ideia de direção

O vídeo não deve parecer uma corrida ilustrada por cima de uma câmera lenta. A poça é o acontecimento; o reflexo conduz o olhar, o pé cria a tensão, a água cobre a lente e a voz de “ALL FINE” revela os dados. Cada mudança de imagem e de som responde a um desses acontecimentos.

O roteiro abaixo é uma proposta calculada sobre os tempos do original. Ele não altera a v10 entregue. A régua de produção só deve ser atualizada depois da aprovação da prévia deste animatic.

## Decisão de câmera lenta

A câmera grava a 59,94 q/s e a entrega sai a 30 q/s. A proposta usa `0,5x` entre 32,800 s e 33,210 s do original. Nesse ritmo, cada quadro de saída pode usar um quadro real da câmera; não é necessário inventar quadros com RIFE ou fluxo óptico.

Isso troca o movimento extremo e irregular de `0,12x` por uma desaceleração visível, com textura consistente no tênis, nas pernas, no reflexo e no respingo. O slow começa quando o corredor já está perto da poça e termina exatamente no ápice medido do pé. A soltura continua seca, conforme a direção já pedida.

## Roteiro com tempos

Os tempos de saída são calculados pela velocidade v11 aplicada ao código, a 30 q/s. Há no máximo um quadro de tolerância por arredondamento de origem.

| Saída | Quadro | Origem | Imagem e ação | Som e gráfico |
|---|---:|---:|---|---|
| 0,000–2,800 s | 0–83 | 30,000–32,800 s | Corrida em tempo real. Deixar céu, reflexo e poça respirarem; nenhum texto permanente. Empurrão de câmera de 100% a 104%, ancorado perto da linha d’água. | Começa um trecho instrumental de “ALL FINE”. Ambiente original zerado. Sem whoosh genérico. |
| 2,800 s | 84 | 32,800 s | Entrada seca em `0,5x`, já perto da lente. | Pequena redução musical de 2 dB por 100 ms para anunciar a mudança. |
| 2,800–3,620 s | 84–108 | 32,800–33,210 s | A pisada em 32,867 s, a água e a subida do último pé avançam a meia velocidade. O enquadramento permanece estável; sem zoom extra durante o gesto. | A trilha sustenta a aproximação. Não adicionar sub-hit sobre o passo real. |
| 3,620 s | 109 | 33,210 s | Soltura seca para `1x` no ápice do pé, entre o máximo do centro (33,201 s) e do topo (33,218 s). | Retorno da trilha à intensidade normal. |
| 3,680 s | 110–112 | 33,270 s | O pé toca ao lado da lente. A água começa a subir. | O som original do contato entra no quadro do toque; ambiente abre só por 250 ms. |
| 3,767 s | 113 | 33,356 s | Primeiro quadro de saída já claro: a água cobriu a lente. Os dados começam a aparecer aqui, sem antecipação. | Primeira entrada vocal de “ALL FINE” no mesmo quadro. Este é o drop narrativo e o ponto de sincronismo principal. |
| 3,767–4,767 s | 113–142 | 33,356–34,356 s | Sticker se monta em um segundo. A rota verde Kivow desenha primeiro; distância conta em seguida; ritmo e tempo entram em pares. | A voz conduz a montagem. Splash termina antes da palavra/voz ocupar a frente. |
| 4,767–8,267 s | 143–247 | 34,356–36,103 s | Fundo molhado desacelera a `0,5x`. Manter os dados estáveis e legíveis enquanto a água se move. Encerrar antes da mão voltar a pegar o celular. | Música segue sem novos efeitos; fade de saída nos últimos 300 ms. |

## Animação do sticker

- Quadro 113: acendem rótulo, distância, ritmo, tempo e marca K com opacidade 0→1 em 6 quadros; deslocamento vertical de 14 px para 0; blur de 6 px para 0.
- Quadros 113–142: rota desenha em 30 quadros, com ease-out suave; traço secundário creme fica abaixo do verde Kivow.
- Quadros 113–134: distância conta em 21 quadros. Usar os dados reais do Strava; os valores atuais são placeholders.
- Quadros 143–248: rota e números permanecem firmes; deriva máxima de 6 px ao longo de 3,52 s.
- Nenhum elemento fica parado desde o primeiro segundo, e nenhum dado começa antes da água cobrir a lente.

## Curva de velocidade proposta

| Origem | Velocidade | Regra |
|---|---:|---|
| 30,000–32,800 s | 1,0x | aproximação sem interpolação |
| 32,800–33,210 s | 0,5x | meia velocidade fixa; quadros originais da captura a 59,94 q/s |
| 33,210–34,350 s | 1,0x | soltura seca, contato e revelação |
| 34,350–36,1085 s | 0,5x | leitura com movimento real da água |

Não usar a curva descendente `0,25x → 0,12x` nesta proposta. O quadro de 59,94 q/s não sustenta esse ritmo sem interpolação pesada; o RIFE global atual altera contornos justamente no tênis e na água.

## Plano de som

1. Escolher o trecho da faixa pelo primeiro ataque vocal, não pelo BPM estimado nem pelo maior pico de volume.
2. Marcar o primeiro ataque vocal em amostra/tempo no MP3. Posicioná-lo em `3,755 s`, quadro 113, que é o primeiro quadro claro do sticker.
3. Usar a parte instrumental anterior como construção da aproximação e do slow. Não fazer a voz começar antes dos dados.
4. Abrir o som original apenas no contato em `3,680 s`; fechar em `3,930 s`. O resto do ambiente fica mutado.
5. Se a forma de onda vocal encobrir o splash, abaixar a música em 3 dB entre `3,680–3,767 s`, retornando ao nível normal no quadro da voz.
6. Não aplicar slow de fita à música. A trilha permanece em tempo e tom normais durante a câmera lenta.
7. Master: `-14 LUFS` integrado, true peak máximo `-1,5 dBTP`, AAC estéreo 320 kb/s.

## Efeitos e enquadramento

- Manter o empurrão de câmera contínuo e discreto; limitar a escala final a 104%, em vez de adicionar zooms que competem com a aproximação física.
- Não usar flash branco no impacto: a própria lente clareia quando a água a cobre.
- Não adicionar partículas artificiais: o respingo real é o efeito principal.
- Não colocar whoosh ou sub-hit por padrão. Só entram se a escuta A/B provar que acrescentam leitura sem mascarar o contato real.
- Fazer uma versão A sem efeitos extras e uma versão B com um único acento grave curto no toque, mantendo o mesmo corte e a mesma mixagem base.

## QA que decide a aprovação

- Soltura entre 33,201–33,218 s do original, sem quadro intermediário sintético no gesto de 0,5x.
- O primeiro quadro do sticker é o primeiro quadro claro da água; nunca antes.
- Ataque vocal medido cai no quadro 113, tolerância máxima de ±1 quadro.
- O som do toque antecede a voz; a forma de onda mostra o ambiente fora do intervalo curto de impacto abaixo de -60 dBFS.
- Folha ampliada do tênis e da borda da poça: sem duplicação, deformação ou salto de nitidez.
- Folha da rota: o verde Kivow aparece como traço principal; o creme funciona somente como rastro secundário.
- Leitura dos dados aprovada em telefone a 1080 x 1920; nenhum valor fica cortado ou coberto pelos controles da plataforma.
- Entrega só é aprovada depois de assistir ao arquivo completo com fones e no alto-falante do celular.

## Ordem de produção para reduzir retrabalho

1. Marcar o ataque vocal no arquivo original e congelar a origem musical.
2. Gerar prévia de 1080 com a nova curva de velocidade, sem render 4K.
3. Gerar uma folha de todos os quadros entre 32,800–33,351 s e revisar pé, reflexo e água.
4. Fazer duas mixagens A/B: splash natural e splash com acento grave discreto.
5. Assistir à prévia e aprovar timing, leitura e som.
6. Só então atualizar `tempos.json`, rodar QA e renderizar o master 4K uma única vez.

## Ponto de escuta antes do master

- O primeiro ataque vocal usado como referência é aproximadamente 9,8 s no MP3; confirmar na prévia que a sílaba começa no quadro 113. A extração automática de voz não é confiável para canto.
- Os dados do sticker ainda são placeholders; substituir por distância, ritmo e tempo verdadeiros.
- A duração v11 é 8,267 s (248 quadros). A prévia decide se o encerramento mais curto mantém leitura suficiente.
