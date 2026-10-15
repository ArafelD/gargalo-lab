# Contribuindo
1. Fork + branch (`feat/labXX-nome`).
2. Todo lab novo precisa de: módulo em `gargalo_lab/`, saída com prefixo numérico (`09_...`), teste em `tests/`, linha na tabela do README, entrada em `docs/LABS.md` e checagem em `gargalo_lab/verify.py`.
3. Regra de ouro: **dados sintéticos e foco em detecção/defesa**. PRs com payloads, exploits, ferramentas ofensivas ou mecanismos reais de vazamento serão recusados.
4. Rode `make test && make verify` antes do PR.
