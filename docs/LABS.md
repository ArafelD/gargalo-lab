# Guia dos 8 laboratórios

Cada lab é independente, determinístico (seed fixa) e usa apenas dados sintéticos.
Rodar um lab: `python -m gargalo_lab <nome ou número>` (ex.: `python -m gargalo_lab 05`).
Conferir todos os resultados de referência do artigo: `python -m gargalo_lab verify`.

| # | Comando | Módulo | Arquivos gerados em `output/` |
|---|---------|--------|-------------------------------|
| 01 | `enhance` | `enhance_myth.py` | `01_enhance_montage.png` |
| 02 | `exif` | `exif_osint.py` | `02_sample_with_gps.jpg`, `02_sample_clean.jpg` |
| 03 | `usb` | `usb_detect.py` | `03_usb_events.jsonl`, `03_usb_alerts.json` |
| 04 | `beacon` | `beacon_hunt.py` | `04_conn_log.csv` |
| 05 | `photo` | `triangulation.py` | `05_error_table.csv` |
| 06 | `deadman` | `deadman.py` | `06_deadman_report.json` |
| 07 | `insider` | `insider.py` | `07_access_log.csv` |
| 08 | `custody` | `custody.py` | `08_custody_log.json` |

## 01 · Mito do *enhance* (seção "O zoom que não existe")
**Como funciona:** gera uma cena sintética (placa fictícia e listras finas), reduz 8×, amplia por interpolação bicúbica e mede PSNR e energia de alta frequência. Também fabrica dois mundos diferentes (xadrez em fases opostas) que, reduzidos, ficam idênticos.
**Leia assim:** o montagem PNG mostra original, miniatura e "enhance" lado a lado. O detalhe fino perdido não volta.
**Limite:** interpolação clássica; não treina nem executa redes de super-resolução.

## 02 · Metadados EXIF (seção "Seguir o rastro")
**Como funciona:** cria um JPEG sintético com GPS de um marco público (Praça dos Três Poderes), lê os metadados, gera relatório de risco e recria a imagem só com pixels.
**Limite:** cobre EXIF básico; não analisa XMP/IPTC nem metadados de vídeo.

## 03 · Pendrive e USB (seção "O elo humano")
**Como funciona:** gera logs JSONL sintéticos de 5 estações; aplica R1 (dispositivo fora da allowlist), R2 (execução a partir da mídia em até 120 s) e R3 (dispositivo composto teclado + disco). Nenhum código malicioso existe no repositório.
**Limite:** regras didáticas; produção exige telemetria real de endpoint.

## 04 · *Beaconing* (seção "Seguir o rastro")
**Como funciona:** 6 h de conexões sintéticas (21 máquinas navegando, um NTP legítimo, um beacon de 60 s com jitter de 10% e outro de 300 s com jitter de 30%). Calcula o coeficiente de variação dos intervalos por par origem/destino e filtra por quantidade mínima de conexões, bytes baixos e lista de "conhecidos bons".
**Limite:** não cobre beacons com jitter muito alto, intervalos adaptativos nem tráfego cifrado com padrão mascarado.

## 05 · Triangulação (seção "A régua e o gelo")
**Como funciona:** duas câmeras paralelas simuladas. Mostra que um mundo 3× maior gera os mesmos pixels (ambiguidade de escala), recupera a escala com uma régua conhecida (porta de 2 m) e mede o erro por Monte Carlo (2.000 tentativas por célula) em função de ruído e distância entre câmeras.
**Limite:** modelo estéreo ideal, sem distorção de lente nem calibração real; serve para ensinar o raciocínio, não para uso pericial.

## 06 · *Dead man's switch* (seção "O botão que dispara")
**Como funciona:** máquina de estados (armado → avisado → disparado) com relógio injetado. Simula 200 meses e compara o gatilho ingênuo (5 h sem sinal) com aviso + tolerância de 3 h + quórum de 2 entre 3 guardiões. A "ação" só registra uma mensagem em lista na memória.
**Limite:** simulação de decisão; não há envio, vazamento nem conteúdo real.

## 07 · Ameaça interna (seção "Quando o perigo já tem crachá")
**Como funciona:** 30 dias de logs de 8 usuários, três regras (acesso fora do papel, volume vs. histórico pessoal com z-score, madrugada) e pontuação para severidade.
**Limite:** regras fixas; não modela comportamento coletivo nem contexto organizacional.

## 08 · Cadeia de custódia (seção "A régua e o gelo")
**Como funciona:** registro de custódia com hash SHA-256 encadeado (cada entrada inclui o hash da anterior), detecção de adulteração de evidência e de registro, e plano de coleta por ordem de volatilidade.
**Limite:** sem assinatura digital nem carimbo de tempo confiável; didático.
