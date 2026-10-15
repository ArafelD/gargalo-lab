# ⚖️ gargalo-lab

> **Oito laboratórios defensivos** que acompanham o artigo *"O gênio de fora ou o analista de dentro?"*, sobre onde a segurança da informação realmente quebra: no acesso, nas pessoas e nas provas. Inspirados em *Jason Bourne* (2016) e *Operação Vingança* (*The Amateur*, 2025).

[![CI](https://github.com/SEU_USUARIO/gargalo-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/SEU_USUARIO/gargalo-lab/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)
![Labs](https://img.shields.io/badge/labs-8-blueviolet)
![Tests](https://img.shields.io/badge/tests-17%20passing-brightgreen)
![Reference checks](https://img.shields.io/badge/reference%20checks-16%2F16-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Blue Team](https://img.shields.io/badge/focus-blue%20team%20%26%20DFIR-0A66C2)
![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1091%20%7C%20T1200%20%7C%20T1071%20%7C%20T1078%20%7C%20T1213-red)
![Synthetic data](https://img.shields.io/badge/data-100%25%20synthetic-lightgrey)

## O artigo

O texto completo está em [`docs/ARTIGO.md`](docs/ARTIGO.md). Este repositório é a parte prática: cada laboratório simula, com dados sintéticos, um conceito explicado no artigo e produz um resultado que você pode conferir.

## Os 8 laboratórios

| Lab | Tema do artigo | O que a simulação demonstra | Resultado de referência (seed fixa) |
|---|---|---|---|
| **01 Mito do *enhance*** | O zoom que não existe | Reduz uma cena sintética 8× e tenta "melhorar" com interpolação bicúbica; fabrica duas imagens diferentes que ficam idênticas depois de reduzidas | Miniatura com 1,56% dos pixels; ≈ 15 dB de qualidade; detalhe fino cai de 0,134 para 0,00008 |
| **02 Metadados EXIF** | Seguir o rastro | Cria foto sintética com GPS, mostra o que ela revela e remove a etiqueta | GPS presente antes, ausente depois (verificado por teste) |
| **03 Pendrive e USB** | O elo humano | Regras de detecção em logs sintéticos: dispositivo fora da lista, execução a partir da mídia, dispositivo "teclado + disco" | As três regras disparam só nos cenários esperados |
| **04 *Beaconing*** | Seguir o rastro | Seis horas de tráfego sintético com navegação aleatória, um serviço de hora legítimo e dois beacons (um regular, outro com jitter de 30%) | Os dois beacons são achados; o serviço legítimo é ignorado |
| **05 Triangulação** | A régua e o gelo | Duas câmeras sintéticas: mundos de escalas diferentes geram pixels idênticos; erro de medida conforme ruído e geometria | Erro médio de ≈ 2 cm (câmeras a 1,5 m, ruído de 1 px) a ≈ 81 cm (câmeras a 10 cm) |
| **06 *Dead man's switch*** | O botão que dispara | Simula 200 meses com ausências aleatórias; compara gatilho ingênuo com aviso, tolerância e quórum. É apenas uma simulação em memória, sem envio real | Disparo falso: 100% contra 8,5%; casos perdidos de 5,5%; atraso de ≈ 5,8 h |
| **07 Ameaça interna** | Quando o perigo já tem crachá | Logs de 30 dias de 8 usuários; regras de papel, volume e horário | Acesso fora do papel + volume + madrugada = severidade alta; volume alto dentro do papel = média |
| **08 Cadeia de custódia** | A régua e o gelo | Log de custódia com hash encadeado e plano de coleta por ordem de volatilidade | Adulteração de evidência ou de registro é detectada; desligar a máquina perde memória e estado de rede |

Detalhes de cada lab (como funciona, arquivos gerados, limites): [`docs/LABS.md`](docs/LABS.md).

## Início rápido

```bash
git clone https://github.com/SEU_USUARIO/gargalo-lab.git && cd gargalo-lab
python3 -m venv .venv && source .venv/bin/activate
make install

make test      # 17 testes
make verify    # confere os 16 resultados de referência da tabela acima
make run       # roda os 8 labs e grava os arquivos em ./output
```

Um lab específico: `python -m gargalo_lab 05` (ou `photo`). Com Docker: `docker compose up --build lab`, `docker compose run --rm --build tests` e `docker compose run --rm --build verify`.

O `verify` gera `output/REFERENCE_CHECK.md` com o resultado de cada afirmação da tabela (✅ / ❌), então qualquer mudança no código que quebre um número do artigo é detectada.

Opcional: `docker compose --profile owasp up juice-shop` sobe o OWASP Juice Shop, aplicação propositalmente vulnerável, exposta apenas em `127.0.0.1`, para estudar controle de acesso em ambiente seu.

## Estrutura

```
gargalo_lab/   # os 8 labs + cli.py + verify.py (NumPy e Pillow)
tests/         # 17 testes (unittest, sem dependências extras)
docs/          # ARTIGO.md, LABS.md, MITRE_MAPPING.md
.github/       # CI: Python 3.10-3.12, verify e build Docker
```

## Limitações honestas

Os modelos são simplificados (câmeras paralelas, ruído gaussiano, logs e tráfego sintéticos). Servem para **ensinar o raciocínio**, não para uso pericial ou operacional.

## Ética e uso responsável

Conteúdo educacional e defensivo. Nenhum código malicioso, nenhum envio real de mensagens, nenhum dado pessoal. Pratique apenas em ambientes seus ou com autorização por escrito.

## Licença

MIT. Veja [LICENSE](LICENSE).

— Porque conhecimento ofensivo só tem valor quando serve pra fortalecer a defesa. ⚔️
