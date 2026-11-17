# Auditoria da v6 e plano de produção da v7

## Veredito

A v6 está correta como prova técnica do timing, mas ainda não é a versão final de linguagem. O início do slow motion está bem marcado em 32,80 s e a soltura acontece no ponto alto do pé, porém a qualidade visual cai porque a interpolação é aplicada na imagem inteira durante o trecho mais difícil: tênis, pernas, água, reflexo e respingo se movem ao mesmo tempo.

O próximo passo não deve ser apenas baixar mais a velocidade. A v7 precisa combinar uma curva de velocidade mais curta e controlada, interpolação com QA por quadro, desenho sonoro e uma entrada gráfica que use o impacto como virada.

## Estado medido da v6

- Master: 2160 x 3840, 30 q/s, 298 quadros, 9,933 s.
- Vídeo: H.264 High, aproximadamente 118 Mb/s, CRF 12 na etapa final.
- Áudio: AAC 320 kb/s, medição final de -14,4 LUFS, LRA 3,1 LU, pico -1,1 dBFS.
- Curva: 1x até 32,80 s; queda de 0,25x para 0,12x; soltura seca em 33,21 s; 0,5x a partir de 34,35 s.
- Interpolação: 66 quadros RIFE, 8 quadros de origem dentro do trecho abaixo de 0,45x; os demais 232 quadros são de origem.
- O sticker começa em 33,345 s, cerca de 5 quadros antes do quadro claro em que a água cobre a lente.
- O arquivo 4K em `Downloads` bate com a ficha da entrega em tamanho e duração.

## O que funciona

1. A entrada em câmera lenta está finalmente próxima da poça, não na primeira passada.
2. O pé é solto entre 33,201 s e 33,218 s, no ponto alto definido pela medição.
3. A saída SDR está consistente com o pipeline Remotion e o master tem resolução suficiente para a entrega vertical.
4. A folha de soltura permite auditar o impacto, a cobertura da lente e a entrada do sticker.
5. O loudness final está dentro do alvo de -14 LUFS.

## Problemas que precisam ser resolvidos

### 1. Câmera lenta

O RIFE v4.6 recebe o quadro inteiro em resolução de trabalho de 2376 x 4224. Nesse plano, o movimento do corredor é apenas uma parte da cena; o reflexo e a água não obedecem ao mesmo modelo de movimento. Isso produz bordas moles, duplicação do tênis e respingos que parecem derretidos.

O teste atual de sanidade compara o quadro gerado com uma mistura linear dos vizinhos. Esse teste detecta faixas e diferenças grosseiras, mas não reprova fantasma em objetos de alto contraste. Também aceita quadros de origem dentro do slow motion, criando uma alternância sutil de textura e nitidez.

Direção v7:

- reduzir a dependência de 0,12x; usar 0,5x na aproximação, 0,25x no gesto do pé e uma retenção curta no ápice;
- interpolar somente o intervalo que realmente precisa de quadros novos;
- manter água e fundo preservados sempre que possível e concentrar a interpolação na região do corredor;
- não alternar silenciosamente entre RIFE, origem e DIS: registrar o método e a métrica de cada quadro;
- reprovar quadro com fantasma por diferença de contorno, não só por média de pixels;
- gerar uma folha ampliada do tênis, da borda da poça e do reflexo para aprovação.

### 2. Planejamento visual

Hoje a peça depende quase toda do slow motion e do sticker. A ação forte termina por volta de 33,4 s do original; depois há aproximadamente 4 s de lente molhada, com pouca mudança visual. O sticker continua desenhando a rota enquanto o fundo quase não muda.

Direção v7 recomendada:

- 0,00–0,45 s: entrada limpa no quadro, sem cartão fixo;
- 0,45–2,65 s: corrida em tempo real, com uma chamada mínima de atividade entrando e saindo;
- 2,65–4,95 s: pisada e água em câmera lenta, sem sobrecarregar o quadro;
- 4,95–5,30 s: ápice do pé, retenção curta e silêncio parcial;
- 5,30–6,20 s: soltura seca, pouso e cobertura da lente;
- 6,20–9,20 s: sticker se monta com a água como textura, rota desenhando em ritmo musical;
- 9,20–9,93 s: saída com o sticker já legível, sem prolongar a leitura além do necessário.

O sticker deve usar os dados reais da atividade. Os valores atuais 8,01 km, 5:55/km e 47min23s ainda são dados de exemplo e não devem ir para uma entrega pública como se fossem a corrida real.

### 3. Efeitos

O projeto atual tem empurrão de câmera, desenho de rota e entrada de elementos, mas não tem uma hierarquia de efeitos para vender o impacto. A v7 deve usar poucos efeitos, cada um ligado a uma causa visível:

- micro-zoom de 100% para 106% durante a aproximação;
- queda breve de exposição e/ou contraste no início do slow motion;
- whoosh curto na entrada da desaceleração;
- sub hit no ponto mais baixo da pisada;
- impacto de água sincronizado com o quadro em que a lente clareia;
- retorno seco do espectro e da velocidade no pé alto;
- ducking da música durante o impacto, sem cobrir o som da água.

Não usar partículas ou respingos artificiais sobre a imagem real sem antes validar se o registro original já entrega o efeito necessário.

### 4. Som

O pipeline atual apenas retimeia o áudio ambiente e normaliza para -14 LUFS. Não há música, mapa de batidas, efeitos, ducking ou stems. Isso deixa o impacto visual sem uma dramaturgia sonora.

“ALL FINE”, de MARIA PESSOA GALASSI, está identificado em plataformas como single de 2025 com duração de 2:10; uma fonte de análise lista 112 BPM e tonalidade G# menor. Fontes: [YouTube](https://www.youtube.com/watch?v=sfYfI0L1zZw), [Spotify](https://open.spotify.com/intl-pt/album/2eN5NO2am9obUayhq24fRV), [Shazam](https://www.shazam.com/album/1824693566/all-fine-single).

Para usar a faixa corretamente, o projeto ainda precisa receber um arquivo de áudio autorizado, de preferência WAV ou AAC/MP3 de boa qualidade. O link de streaming ou o resultado do Shazam não substitui o arquivo de produção nem a autorização de uso.

Mapa sonoro provisório para 112 BPM:

- duração da batida: 0,5357 s;
- duração de um compasso 4/4: 2,1429 s;
- colocar o início da peça em um downbeat ou em uma entrada musical clara;
- reservar o impacto da água para um beat ou sub-hit, com ducking de 4 a 6 dB por 180 a 260 ms;
- manter o som original da poça audível entre -18 e -12 dBFS no pico local, antes do master;
- fechar com -14 LUFS integrado, true peak máximo de -1,5 dBTP e AAC de 320 kb/s.

Sem o arquivo da faixa, não é possível aprovar o sincronismo final. O mapa de batidas precisa ser medido na gravação usada, não inferido apenas pelo BPM de uma página externa.

## Implementação técnica v7

1. Criar uma régua v7 separando `origem`, `velocidade`, `congelar`, `audio` e `efeitos` em um único JSON.
2. Alterar `scripts/base.py` para gerar mapa com `origem`, `método`, `fração`, `nitidez`, `diferença de contorno` e motivo de fallback por quadro.
3. Renderizar a interpolação apenas em uma região de interesse do corredor, preservando a água e o fundo quando a métrica indicar que o quadro inteiro está instável.
4. Criar `scripts/qa.py` para medir duração, resolução, fps, continuidade da origem, ponto da soltura, tempo até a lente clarear, loudness e artefatos do trecho lento.
5. Adicionar folhas de prova específicas: trecho completo, tênis em 200%, reflexo e primeiros 12 quadros do sticker.
6. Adicionar mixagem opcional de música, efeitos e ambiente no workflow, sem gravar a faixa dentro do Git se ela não tiver licença para redistribuição.
7. Atualizar o texto e o sticker com os dados reais da atividade antes de renderizar a entrega pública.

## Critérios de aprovação da v7

- 1x até o quadro de origem definido na nova régua, com tolerância máxima de 1 quadro;
- soltura entre 33,201 s e 33,218 s do original, salvo decisão criativa explícita;
- nenhum quadro RIFE reprovado por fantasma ou borda dupla na folha ampliada;
- nenhuma troca de nitidez perceptível entre quadro de origem e quadro sintético;
- sticker só aparece quando a lente já está coberta e fica legível em 1080 x 1920;
- dados do sticker conferidos contra print ou arquivo da atividade;
- master 2160 x 3840, 30 q/s, -14 ±1 LUFS, true peak abaixo de -1,5 dBTP;
- música, água, impacto e soltura audíveis separadamente na folha de onda e na escuta do master.

## Pendências para fechar a produção

- arquivo autorizado de “ALL FINE”;
- print do Strava ou GPX com distância, tempo, ritmo e elevação;
- @ ou texto que deve aparecer;
- decisão entre manter 9,93 s ou encurtar o plano molhado para cerca de 8,5–9,2 s;
- confirmação de que a entrega pública será SDR Rec.709, que é o caminho atual do Remotion.
