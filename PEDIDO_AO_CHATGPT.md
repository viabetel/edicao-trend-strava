# Pedido ao ChatGPT

## O pedido do Nicácio, nas palavras dele

> "preciso de edição nisso aqui igual as trends do strava"

## O que queremos de você

1. **Pesquisar as trends de edição do Strava que estão rodando agora** no Reels, no TikTok e no Shorts. Exemplos do que procurar:
   - números da atividade entrando por cima do vídeo (distância, tempo, pace, elevação);
   - a linha do percurso se desenhando;
   - o cartão de compartilhamento do Strava animado;
   - parciais por km;
   - revelação do resultado no final.

   Para cada trend, traga um link ou o nome de um exemplo real. Diga também o que define a trend: o que o público reconhece em 1 segundo.
2. **Assistir ao nosso vídeo pelas folhas e pelos gráficos** deste repositório. O roteiro de leitura está no README. Anote o que acontece em cada trecho e onde estão os momentos fortes.
3. **Propor de 2 a 3 direções de edição** que usem este vídeo nesse estilo. Recomende uma e explique o motivo.
4. **Devolver um prompt de produção** para o Claude executar a direção recomendada, com:
   - roteiro de tempo em segundos e quadros (30 q/s na saída), amarrado aos momentos do vídeo;
   - cada camada gráfica com conteúdo, posição na tela 1080x1920, fonte, tamanho, cor, entrada, saída e curva;
   - números de movimento: duração, atraso, deslocamento em px, desfoque, escala;
   - **sem adjetivo no lugar de número**;
   - velocidade do vídeo: onde acelera, desacelera ou congela, e se algum trecho volta;
   - corte e reenquadramento: o que fica de fora dos 39,6 s;
   - som: trilha (tipo e BPM, ou o áudio original), efeitos e onde a batida casa com o visual;
   - a lista do que falta pedir ao Nicácio. Por exemplo: os dados da atividade (print do Strava, arquivo GPX, distância, tempo, pace, elevação), a música e o @ que aparece;
   - critérios de QA medíveis para aprovar o render.

## Como o Claude trabalha

Isto define o que o seu prompt pode pedir:

- **Ferramentas:**
  - Remotion 4 (React) para as camadas animadas;
  - ffmpeg para corte, velocidade, cor e mixagem;
  - Python com OpenCV para medir;
  - Figma para desenhar as camadas antes do código.
- **Render só na nuvem**, no GitHub Actions, nunca no computador do Nicácio.
- **Método de motion medido:**
  - um único arquivo de tempos;
  - curvas com parâmetros;
  - folha de contato e QA numérico antes de entregar.

  Exemplo do método, com outro projeto, no repositório público https://github.com/viabetel/motion-engine-caderno02.
- **Regras de arte do Nicácio:**
  - texto entra e sai, nunca fica como cartão parado o vídeo todo;
  - nada de travessão nem de copy com cara de IA;
  - som com causa visível na tela;
  - beleza primeiro.
- **O original é HDR (HLG) do iPhone.** Diga se a entrega deve ser SDR (Rec.709) ou HDR. O Remotion renderiza em SDR.

## Formato da resposta

Um único arquivo Markdown com:

1. trends pesquisadas;
2. leitura do vídeo;
3. direções e recomendação;
4. prompt de produção;
5. perguntas ao Nicácio.
