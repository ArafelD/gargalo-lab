# O gênio de fora ou o analista de dentro? O que dois filmes de espionagem (e um hacker de verdade) revelam sobre onde a segurança realmente quebra

*Publicado em 21 de maio de 2026 · Plantão Tech*

---

Imagine que você está no sofá, numa terça-feira à noite, com o filme já na metade. Numa sala escura da CIA, alguém aponta para uma imagem granulada de câmera de segurança e dá a ordem que todo espectador conhece de cor: "enhance". Em segundos, o borrão vira um rosto. O hacker de plantão digita algo, o firewall cai, a música sobe. Quando os créditos rolam, fica uma ideia confortável e perigosa: segurança da informação é uma disputa de gênios, vencida por quem digita mais rápido.

A vida real é bem menos empolgante e bem mais instrutiva. Quase nunca é o teclado que decide o jogo; é a **chave**, é a **pessoa** e é a **prova** que sobra depois. Neste artigo vamos usar dois filmes de espionagem, *Jason Bourne* (2016) e *Operação Vingança* (*The Amateur*, 2025), como cenário para entender onde a segurança de fato quebra. Pelo caminho, vamos conversar com um personagem real, Kevin Mitnick, cuja história mostra por que o elo mais frágil costuma estar longe do código.

Se você é estudante, vai encontrar o raciocínio por trás de técnicas que se estudam em cursos e laboratórios. Se é profissional, talvez reconheça situações do seu dia a dia com roupagem de Hollywood. E se chegou aqui por curiosidade, não precisa de formação nenhuma: cada conceito será explicado a partir do que ele significa na prática.

## Dois filmes, duas teorias sobre como uma agência cai

Em *Jason Bourne*, a invasão vem de fora. A ex-agente Nicky Parsons entra num servidor da CIA a partir de Reykjavík, em parceria com um grupo hacktivista, para expor operações secretas, e é a chefe de operações cibernéticas da agência, Heather Lee, quem percebe o movimento [1][2]. O próprio Bourne, ao contrário do que a memória costuma sugerir, não é o hacker: é o alvo. Já em *Operação Vingança*, dirigido por James Hawes e estrelado por Rami Malek, o protagonista é Charlie Heller, um criptoanalista da CIA que perde a esposa num atentado em Londres e pressiona a própria agência para receber treinamento e ir atrás dos responsáveis [6][7]. Charlie não precisa invadir a instituição: ele já trabalha nela.

Essa diferença de premissa é mais do que enredo, é uma pequena aula sobre modelos de ameaça. Um modelo de ameaça é, na essência, a resposta honesta a uma pergunta simples: *de quem estou me protegendo, e o que essa pessoa já tem?* Para o invasor de fora, o desafio é conseguir qualquer acesso. Para quem já está dentro, o acesso existe, e o problema passa a ser distinguir uso normal de uso indevido.

Quanto ao realismo técnico, vale desmontar um mito: não houve "consenso unânime" de que *Jason Bourne* seria um desastre. Quando especialistas foram ouvidos na época, as opiniões se dividiram. Um deles achou plausível o uso de injeção de SQL e *backdoor* para roubar dados, outro estranhou a interface que mostrava a hacker atravessando três firewalls, e um tecnólogo da HPE lembrou que quebrar criptografia digitando um comando é fantasia de cinema [3]. A fala "use SQL para corromper os bancos de dados", que virou piada, foi analisada pela Imperva, empresa de segurança, justamente por mexer num tipo de ataque real [4]. E a célebre frase "é pior que o Snowden" não é um veredito de crítico de tecnologia: é uma fala de personagem dentro do filme [5].

*Operação Vingança* cai em outra tentação. Seu diretor de fotografia conta que a primeira meia hora mostra Charlie analisando imagens de câmeras de segurança e decifrando dados [9], uma abordagem mais sóbria que a do filme de 2016. Mesmo assim, críticos apontam tecnologia "extremamente questionável", como um dispositivo de escuta do tamanho de um clipe de papel transmitindo entre os Estados Unidos e Londres [10], e o protagonista ainda termina invadindo um navio [6]. É um anti-herói cerebral, não um superespião [8], mas continua sendo cinema.

## O zoom que não existe: por que informação perdida não volta

Voltemos à cena do "enhance", porque ela esconde uma lição valiosa. Em *Jason Bourne*, a equipe manda melhorar imagens de vigilância como se a câmera tivesse guardado detalhes secretos esperando para serem revelados [5]. A intuição é sedutora, mas falha logo no primeiro passo.

Pense numa fotografia como um mosaico de pequenos quadrados coloridos, os pixels. Uma câmera de baixa resolução registra poucos quadrados, e cada um resume tudo o que havia naquela área: um rosto inteiro pode caber em dez quadradinhos. Agora imagine resumir um livro de oitocentas páginas num único tweet. É perfeitamente possível, mas o caminho de volta é impossível: milhares de livros diferentes cabem no mesmo tweet. A imagem pequena é esse tweet. Ampliá-la significa pedir a um programa que **invente** os pixels que faltam, normalmente fazendo médias entre vizinhos, como a interpolação bicúbica, que é a técnica clássica.

A inteligência artificial mudou o jogo, mas não a regra. Redes neurais de super-resolução aprendem, com milhares de fotos, como costumam ser olhos, placas e letras, e então *chutam* detalhes plausíveis. A literatura científica faz uma distinção importante: recuperar o detalhe verdadeiro é muito difícil, ao passo que sintetizar um detalhe convincente, que pode divergir da realidade, é bem mais fácil [11]. Quem explica o tema de forma bem-humorada lembra que essas redes precisam adivinhar o que falta, justamente porque a imagem original não tem informação suficiente [12].

A consequência prática vai além do cinema. Uma imagem "melhorada" pode ser convincente sem ser verdadeira, e uma placa ou um rosto reconstruídos por IA são, no fundo, hipóteses bem produzidas. Por isso, em qualquer investigação séria, a primeira pergunta diante de uma imagem deveria ser: *isto é dado capturado ou dado inventado?*

## Antes do talento vem a chave: por que o acesso é o verdadeiro gargalo

Imagine o melhor arrombador do mundo diante de um cofre dentro de uma sala em que ele não consegue entrar. Talento sem porta aberta vale zero. Esse princípio, tão óbvio quanto negligenciado, está no centro de uma das listas mais influentes da segurança de aplicações, o OWASP Top 10, e a edição de 2025 reforça o recado: **Broken Access Control**, o controle de acesso quebrado, segue em primeiro lugar, e a recomendação mais repetida para preveni-lo é negar tudo por padrão, exceto o que for explicitamente público [13].

Controle de acesso é o porteiro do prédio. Falhar nele é permitir que alguém entre ou veja onde não devia, e o mundo digital oferece variações criativas disso. O SSRF, por exemplo, é um truque parente: em vez de entrar no prédio, o atacante convence o próprio prédio a *buscar algo lá dentro* em seu nome. Essa categoria, que durante anos teve lugar próprio na lista, foi absorvida pelo controle de acesso quebrado na edição de 2025, e a antiga categoria de componentes vulneráveis foi ampliada para falhas na cadeia de suprimentos de software [13]. A injeção, família do SQL injection citado em *Bourne*, caiu para a quinta posição, mas continua perigosa [14].

Repare como isso reorganiza a leitura dos filmes. Num deles, a invasão só acontece porque existe uma ex-integrante que conhece a agência por dentro. No outro, o próprio protagonista já é o acesso. Quando alguém disser que "um nerd derrotou a agência inteira", a pergunta mais útil não é "como ele digitou aquilo?", e sim: **quem entregou a chave a ele?**

## O elo humano: do pendrive no chão à lenda de Kevin Mitnick

Nos anos 1980 e 1990, Kevin Mitnick tornou-se pioneiro de um tipo de invasão que dispensa invadir máquina alguma: ele enganava funcionários de empresas de telefonia para que eles próprios o ajudassem a obter software e serviços, o que o levou à lista de mais procurados do FBI [15]. Mitnick passou quase cinco anos preso e, depois, reinventou-se como consultor de segurança e palestrante, até morrer em 2023, aos 59 anos [15]. Sua história é uma das ilustrações mais claras do que hoje chamamos **engenharia social**: em vez de quebrar a fechadura, convencer alguém a abrir a porta.

O mecanismo continua funcionando porque explora qualidades humanas, não falhas de software: prestatividade, curiosidade, pressa. Um estudo clássico espalhou 297 pendrives pelo campus de uma universidade e estimou que entre 45% e 98% deles foram conectados a computadores; o primeiro em menos de seis minutos [16]. O motivo mais comum não era descuido, era gentileza: as pessoas queriam descobrir o dono para devolver o objeto [16]. Em outra descrição do mesmo trabalho, 68% dos participantes disseram não ter tomado nenhuma precaução [17]. Um pendrive achado no chão é, em essência, uma porta nova instalada na parede da sua casa por um desconhecido; basta você abri-la.

A defesa para isso é menos glamourosa do que um antivírus de filme. O catálogo MITRE ATT&CK, que organiza as técnicas observadas em ataques reais, descreve esse cenário como replicação por mídia removível e recomenda, entre outras medidas, restringir o uso de mídia removível quando ela não é necessária [18]. Na prática, equipes de defesa desenham regras que reconhecem três sinais: um dispositivo fora da lista de aprovados, um programa que começa a rodar a partir da mídia poucos instantes depois de ela ser conectada, e um aparelho que se apresenta ao sistema como teclado e disco ao mesmo tempo, uma combinação suspeita para algo que deveria ser apenas armazenamento. Nenhuma dessas regras exige adivinhar a intenção de quem largou o pendrive. Elas apenas observam o que a porta nova começou a fazer.

## Quando o perigo já tem crachá: a ameaça interna

Charlie Heller, em *Operação Vingança*, é a encarnação cinematográfica de um problema que tira o sono de equipes de segurança: o *insider*, a pessoa com acesso legítimo. A definição ampla aceita por agências como a CISA americana vai além do funcionário revoltado e inclui os chamados insiders comprometidos, cujas credenciais ou aparelhos foram tomados por terceiros; entre as respostas recomendadas estão o privilégio mínimo e a segurança de identidade [19][20].

O que torna o tema tão difícil é a natureza do rastro. Do ponto de vista dos registros do sistema, alguém autorizado fazendo algo indevido se parece, à primeira vista, com trabalho comum. O porteiro conferiu o crachá na entrada, mas ninguém perguntou o que aquela pessoa foi fazer na gaveta do vizinho. Por isso as equipes costumam combinar três perguntas simples: o que foi acessado pertence ao papel dessa pessoa? A quantidade foge muito do histórico dela? Aconteceu em horário atípico? Uma resposta afirmativa é curiosidade ou um dia fora da curva; três juntas pedem investigação. E um alerta de volume sem acesso fora do papel, por exemplo, merece olhar, não acusação. Ficar de olho em pessoas, aliás, exige transparência e regras claras; monitoramento sem limite vira outro problema.

## Seguir o rastro: do modem de Raleigh aos batimentos escondidos na rede

Se Mitnick era mestre em enganar pessoas, a sua captura foi uma aula de seguir rastros. A história é contada no livro *Takedown*, de Tsutomu Shimomura, o especialista em segurança que percebeu que seu próprio computador tinha sido invadido e passou a perseguir o intruso [22]. O percurso, segundo um resumo do caso, foi rastrear a incursão até um modem específico num provedor em Raleigh, na Carolina do Norte, e então usar equipamento de rastreamento de telefonia celular para que o FBI chegasse ao apartamento onde Mitnick estava [21]. Nenhum "enhance" mágico: apenas registros, correlação e paciência.

Esse mesmo espírito vale hoje para três tipos de rastro que vale a pena entender. O primeiro são os **metadados das fotos**. Toda imagem tirada num celular carrega uma etiqueta escondida chamada EXIF, que pode guardar coordenadas de GPS, data, hora e modelo do aparelho [23]. As grandes redes sociais costumam remover esses dados no envio, mas nem todo canal faz isso; e-mails e links de armazenamento em nuvem tendem a entregar o arquivo original, localização incluída [23], e análises independentes mostram que a limpeza varia de serviço para serviço [24]. O relato mais citado sobre o risco conta que, em 2016, dois estudantes de Harvard usaram coordenadas de fotos para identificar 229 traficantes em mercados da dark web [24]. Uma foto aparentemente inocente pode ser uma pista geográfica.

O segundo rastro é mais discreto: o **batimento cardíaco da rede**. Programas maliciosos que esperam ordens de um controlador remoto costumam "ligar para casa" em intervalos regulares, como um despertador. Gente navegando é bagunçada; despertador é metódico. A detecção explora essa diferença medindo a regularidade dos intervalos entre conexões: quanto mais parecido com um relógio, mais suspeito. A própria documentação das ferramentas reconhece a limitação, já que serviços legítimos, como atualizações e monitoramento, também podem parecer beaconing e gerar falsos positivos [25]. Estatística sozinha não fecha o caso; contexto é parte do método. E, como toda corrida entre ataque e defesa, existe a contramedida: quem adiciona variação aleatória aos intervalos força o defensor a usar estatística mais refinada.

O terceiro rastro é uma ressalva sobre o cinema: gravações de câmeras de segurança não carregam "um endereço IP mágico" dentro do vídeo. O que se correlaciona na vida real são os registros dos sistemas que gravaram, transmitiram ou armazenaram as imagens. Menos Hollywood, mais investigação.

## A régua e o gelo: como imagens e dados viram prova

Os filmes de espionagem adoram a cena em que um analista junta vídeos de câmeras, celulares e outros aparelhos e reconstrói o local do crime em três dimensões. A ideia tem fundamento real e nome técnico, fotogrametria, ou *structure from motion*: estimar a forma de uma cena a partir de várias imagens 2D. O detalhe que o cinema omite é que, com câmeras comuns, a reconstrução só fica correta até um fator de escala desconhecido. Uma foto de um carrinho de brinquedo muito perto e outra de um carro verdadeiro muito longe podem ser idênticas; só uma **régua conhecida** na cena, como a distância real entre dois pontos, ou sensores extras, como GPS e inércia, permitem chegar a medidas reais [26][27][28]. E mesmo com régua, a qualidade depende de ruído nas imagens e da geometria entre as câmeras: o mesmo método pode errar por centímetros ou por metros. Na prática, um trabalho sério exige pontos de referência, verificação independente do erro e método documentado, o oposto do "um clique e sai o 3D".

Quando a imagem ou o log vira evidência, entra outra disciplina: a forense digital. Aqui o cinema comete seu erro favorito, o do "destrua tudo". Cortar a energia ou queimar o equipamento apaga justamente o que mais interessa. A regra clássica se chama **ordem de volatilidade** e funciona como gelo numa mesa quente: o que derrete primeiro precisa ser guardado primeiro. Memória e estado de rede vêm antes do disco, que vem antes de logs remotos e mídias de arquivo [30][31]. Guias como o NIST SP 800-86 tratam da coleta de dados voláteis e da integridade de arquivos dentro do processo de resposta a incidentes [29], e materiais de formação apontam o desligamento "por garantia", quando dados voláteis ainda importam, como erro clássico [31].

Para provar depois que ninguém mexeu na evidência, a prática é calcular um carimbo matemático (um hash) no momento da coleta, trabalhar a partir de cópias verificadas e recalcular o carimbo mais tarde para mostrar que os valores batem; a cadeia de custódia registra quem manuseou o quê, quando e por quê [30][31]. Dá para pensar numa corrente: cada elo carrega a assinatura do anterior, e qualquer alteração no meio denuncia a si mesma. Uma regra de ouro resume o capítulo: isolar, preservar, investigar. Nessa ordem.

Há ainda uma lição de método no que *Operação Vingança* faz bem, que é cruzar fontes em vez de confiar numa só. Uma imagem, um log ou um rumor isolados contam pouco; vários independentes que concordam contam muito. Mas independência é o ponto frágil: duas fontes que vêm do mesmo lugar, ou que foram geradas pela mesma máquina, valem como uma só.

## O botão que dispara quando você para de apertar

Um dos dispositivos preferidos do cinema de espionagem é o *dead man's switch*, o mecanismo que executa uma ação se o dono deixa de enviar um sinal periódico de "estou aqui". A ideia é intuitiva e traiçoeira, porque parar de apertar o botão não prova que algo grave aconteceu: pode ser celular sem bateria, voo longo ou sono pesado. A literatura prática aponta falhas nos dois sentidos. Um prazo curto demais gera disparos falsos numa ausência banal, e depender do servidor de terceiros herda os riscos desse servidor, inclusive o de ser desligado sem aviso [32]. Desenhos melhores evitam liberar tudo de uma vez e dividem o segredo em partes, de modo que um disparo precoce não seja fatal [32].

A lição de engenharia vale para qualquer gatilho automático, de alarmes a bloqueios de conta: todo sistema que decide sozinho troca um tipo de erro por outro. Um bom desenho adiciona tolerância, aviso prévio e confirmação humana, aceitando que o preço será um pouco mais de demora. Vale registrar também uma observação de responsabilidade: este artigo não ensina a montar mecanismos de vazamento, e questões que envolvem denunciantes carregam risco pessoal e jurídico sério, merecendo orientação profissional.

## Do sofá ao terminal: o caminho real para quem quer fazer isso de verdade

O filme corre; a carreira caminha. Quem quer sair do sofá pode pensar o caminho em três etapas, sem pressa e sem prazos mágicos, já que eles variam muito de pessoa para pessoa.

Na primeira, constroem-se os fundamentos: redes, para entender como os dados viajam (abrir uma ferramenta como o Wireshark e *olhar* o tráfego real é a forma mais rápida de perder o medo do assunto), o sistema Linux, onde vive boa parte da infraestrutura, e o raciocínio de causa e efeito. Na segunda, começa a segurança aplicada: estudar as vulnerabilidades web da lista OWASP em laboratórios próprios, usando, por exemplo, um proxy como o Burp Suite para observar e alterar as requisições entre navegador e servidor, ou um mapeador de portas como o Nmap para descobrir quais serviços uma máquina de teste expõe. Esse é também o território dos CTFs (*Capture The Flag*), competições de desafios em plataformas como TryHackMe, Hack The Box e PicoCTF, que treinam o raciocínio resolvendo problemas, não fugindo de helicóptero. Na terceira etapa vem a especialização, e é aí que o roteiro de cinema mais destoa: o herói faz tudo sozinho, enquanto na vida real existem especialistas e equipes, como red team, blue team, SOC, forense e nuvem. Certificações como Security+, eJPT, OSCP e CEH podem servir de mapa de estudo, nunca de substituto da prática.

A comunidade também conta. No Brasil, eventos como H2HC, Roadsec e BSides São Paulo aparecem entre os mais citados do cenário [33], e o profissional de segurança deveria ser tudo, menos solitário.

Uma última palavra sobre *Mr. Robot*, que muita gente chama de documentário. A série é referência de realismo em ficção: consultores como Kor Adana afirmam que os casos se baseiam em precedentes reais e que a equipe usa ferramentas autênticas como o Kali Linux [34]. Mas o próprio Adana admite que invadir uma rede de prisão como na série levaria semanas ou meses de pesquisa [34], e uma cena de ransomware chegou a ser cortada porque os consultores concluíram que não funcionaria tecnicamente [35]. A série ensina cultura e ferramentas; o tempo e o trabalho de verdade ela comprime, porque TV tem horário. Para estudar com método, vale ainda a técnica de Feynman, que consiste em explicar o assunto com palavras simples, achar o ponto onde você trava, voltar à fonte e simplificar de novo [36].

## O laboratório que acompanha este artigo

Para que nada disso fique só na teoria, preparei um repositório com laboratórios práticos, o **gargalo-lab**, escrito em Python com NumPy e Pillow. Todos os dados são sintéticos, não há nenhuma ferramenta ofensiva e o repositório traz testes automatizados (14, todos passando), Dockerfile, integração contínua, política de segurança e um mapeamento conceitual para o MITRE ATT&CK. Para rodar: `make install && make test && make run`. O repositório inclui ainda, como opção, um alvo de treino OWASP exposto apenas em `127.0.0.1`.

São oito laboratórios, cada um ligado a um tema deste texto:

| Lab | Tema do artigo | O que a simulação demonstra | Resultado de referência (seed fixa) |
|---|---|---|---|
| 01 Mito do *enhance* | O zoom que não existe | Reduz uma cena sintética 8× e tenta "melhorar" com interpolação bicúbica; fabrica duas imagens diferentes que ficam idênticas depois de reduzidas | Miniatura com 1,56% dos pixels; ≈ 15 dB de qualidade; detalhe fino cai de 0,134 para 0,00008 |
| 02 Metadados EXIF | Seguir o rastro | Cria foto sintética com GPS, mostra o que ela revela e remove a etiqueta | GPS presente antes, ausente depois (verificado por teste) |
| 03 Pendrive e USB | O elo humano | Regras de detecção em logs sintéticos: dispositivo fora da lista, execução a partir da mídia, dispositivo "teclado + disco" | As três regras disparam só nos cenários esperados |
| 04 *Beaconing* | Seguir o rastro | Seis horas de tráfego sintético com navegação aleatória, um serviço de hora legítimo e dois beacons (um regular, outro com jitter de 30%) | Os dois beacons são achados; o serviço legítimo é ignorado |
| 05 Triangulação | A régua e o gelo | Duas câmeras sintéticas: mundos de escalas diferentes geram pixels idênticos; erro de medida conforme ruído e geometria | Erro médio de ≈ 2 cm (câmeras a 1,5 m, ruído de 1 px) a ≈ 81 cm (câmeras a 10 cm) |
| 06 *Dead man's switch* | O botão que dispara | Simula 200 meses com ausências aleatórias; compara gatilho ingênuo com aviso, tolerância e quórum. É apenas uma simulação em memória, sem envio real | Disparo falso: 100% contra 8,5%; casos perdidos de 5,5%; atraso de ≈ 5,8 h |
| 07 Ameaça interna | Quando o perigo já tem crachá | Logs de 30 dias de 8 usuários; regras de papel, volume e horário | Acesso fora do papel + volume + madrugada = severidade alta; volume alto dentro do papel = média |
| 08 Cadeia de custódia | A régua e o gelo | Log de custódia com hash encadeado e plano de coleta por ordem de volatilidade | Adulteração de evidência ou de registro é detectada; desligar a máquina perde memória e estado de rede |

Um aviso honesto: os modelos são simplificados (câmeras paralelas, ruído gaussiano, logs sintéticos). Servem para ensinar o raciocínio, não para uso pericial ou operacional.

## Conclusão: o que a lenda e os filmes têm em comum

Kevin Mitnick virou lenda porque entendeu que a parte mais maleável de qualquer sistema é a que tem rosto. Quem o capturou, por sua vez, venceu pela paciência de seguir rastros, não por truques cinematográficos. Os dois filmes de que falamos fazem o mesmo contraste, cada um a seu modo: *Jason Bourne* aposta no gênio de fora, e *Operação Vingança* aposta no analista de dentro. A realidade, como costuma acontecer, mistura os dois e acrescenta um terceiro personagem que o roteiro raramente mostra: o processo, aquele conjunto de regras, registros e hábitos que decide quem entra, o que fica guardado e o que pode ser provado depois.

O insight central é simples e incômodo: **o roteiro corta caminho onde a vida real cobra método**. O zoom que não existe, o pendrive que ninguém questiona, a foto que entrega o endereço, o crachá que abre gavetas demais e a prova que ninguém lacrou são o mesmo problema visto de ângulos diferentes. Cada "como ele fez isso?" que o cinema deixa sem resposta é um convite para estudar o que ficou fora do enquadramento.

E você? Qual cena de filme te fez pensar "isso não funciona assim", e que conceito real estava escondido por trás dela? Conta nos comentários.

— Porque conhecimento ofensivo só tem valor quando serve pra fortalecer a defesa. ⚔️

---

## Fontes e créditos

**Filmes de referência:** *Jason Bourne* (2016), dir. Paul Greengrass; *Operação Vingança* (*The Amateur*, 2025), dir. James Hawes. Este artigo é uma obra nova, com pesquisa, correções de fatos e laboratório próprios, que reúne e evolui versões anteriores do tema.

1. Wikipedia. *Jason Bourne (film)*. https://en.wikipedia.org/wiki/Jason_Bourne_(film)
2. The Digital Bits. *Jason Bourne (4K UHD Review)*, 2016. https://digitalbits.com/item/jason-bourne-uhd-bd
3. SC Media. *Jason Bourne cyberespionage theme wasn't all movie magic*. https://www.scworld.com/news/jason-bourne-cyberespionage-theme-wasnt-all-movie-magic
4. Imperva. Blog: análise de cenários de segurança em *Jason Bourne*. https://www.imperva.com/blog/?p=421
5. Bend Bulletin. Crítica de *Jason Bourne*, 28 jul. 2016. https://bendbulletin.com/?p=778255
6. Wikipedia. *The Amateur (2025 film)*. https://en.wikipedia.org/wiki/The_Amateur_(2025_film)
7. NNPA / Florida Sun. Crítica de *The Amateur*, 24 abr. 2025. https://mydigitalpublication.com/article/The+Amateur/4968039/844964/article.html
8. UK Film Review. *The Amateur*, 15 abr. 2025. https://www.ukfilmreview.co.uk/reviews/the-amateur
9. Creative First. *Lethal Intelligence: How DP Martin Ruhe Shot a Decoder's Revenge in The Amateur*, 2025. https://creativefirst.film/?p=27576
10. Gone With The Twins. *The Amateur (2025)* (crítica). https://gonewiththetwins.com/amateur-2025/
11. *Patch-Based Image Hallucination for Super Resolution with Detail Reconstruction from Similar Sample Images* (arXiv:1806.00874). https://arxiv.org/pdf/1806.00874
12. Litt, Geoffrey. *ENHANCE!: Upscaling images CSI-style with generative adversarial neural networks*, 2017. https://www.geoffreylitt.com/2017/06/04/enhance-upscaling-images-with-generative-adversarial-neural-networks
13. The Register. *OWASP Top 10: Broken access control still tops app security list*, 11 nov. 2025. https://www.theregister.com/2025/11/11/new_owasp_top_ten_broken/
14. Reflectiz. *OWASP Top Ten 2025: The Complete Guide*. https://www.reflectiz.com/blog/owasp-top-ten-2025/
15. InformationWeek. *Hacker Legend Kevin Mitnick, a Felon Turned Security Expert, Dies at 59*, 2023. https://www.informationweek.com/security-and-risk-strategy/hacker-legend-kevin-mitnick-a-felon-turned-security-expert-dies-at-59
16. Tischer, M. et al. *Users Really Do Plug in USB Drives They Find*. IEEE Symposium on Security and Privacy, 2016. https://research.google/pubs/users-really-do-plug-in-usb-drives-they-find/
17. VICE. *A Whole Lot of Nitwits Will Plug a Random USB Into Their Computer, Study Finds*. https://www.vice.com/en/article/study-finds-48-percent-people-will-plug-a-random-usb-into-their-computer/
18. MITRE ATT&CK. *Replication Through Removable Media (T1091)*. https://attack.mitre.org/techniques/T1091
19. Security Magazine. *Security Experts Discuss CISA's Insider Threat Guide Updates*. https://www.securitymagazine.com/articles/102570-security-experts-discuss-cisas-insider-threat-guide-updates
20. CISA. *Insider Threat Mitigation Guide*. https://cisa.gov/sites/default/files/publications/Insider%20Threat%20Mitigation%20Guide_Final_508.pdf
21. Living Internet. *Kevin Mitnick*. https://livinginternet.com/i/ia_hackers_mitnick.htm
22. Shimomura, T.; Markoff, J. *Takedown: the pursuit and capture of Kevin Mitnick, America's most wanted computer outlaw – by the man who did it*. Hyperion, 1996 (registro bibliográfico). https://krimdok.uni-tuebingen.de/Record/1607387484?lng=de
23. Copes, Flavio. *What your photos leak: EXIF metadata and GPS*. https://flaviocopes.com/exif-metadata-privacy/
24. Comparitech. *EXIF metadata privacy*. https://comparitech.com/blog/vpn-privacy/exif-metadata-privacy
25. Elastic. *Statistical Model Detected C2 Beaconing Activity* (documentação de regras de detecção). https://www.elastic.co/docs/reference/security/prebuilt-rules/rules/integrations/beaconing/command_and_control_beaconing_high_confidence
26. Forssén, P.-E. *Computer Vision, lecture 12: Structure from Motion* (Universidade de Linköping). https://www.cvl.isy.liu.se/education/undergraduate/tsbb15/lectures/lecture-12.pdf
27. 3Dflow. *How to scale and make measurements with Zephyr Free and Lite*. https://support.3dflow.net/support/solutions/articles/43000052981-how-to-scale-and-make-measurements-with-zephyr-free-and-lite
28. *Inertial-Based Scale Estimation for Structure from Motion* (arXiv:1611.09498). https://ar5iv.arxiv.org/html/1611.09498
29. NIST. *SP 800-86: Guide to Integrating Forensic Techniques into Incident Response*, 2006. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf
30. CyberDefenders. *Digital Forensics / DFIR* (glossário). https://cyberdefenders.org/cybersecurity-glossary/dfir/
31. Open Exam Prep. *Understand and Support Forensic Investigations* (guia SSCP). https://open-exam-prep.com/study-guides/isc2-sscp/incident-response-and-forensics/forensic-investigations
32. D-Central. *Dead Man's Switch* (glossário). https://d-central.tech/fr/mining-glossary/dead-mans-switch/
33. TecMundo. *Conheça os 7 maiores eventos para hackers do mundo; quatro são do Brasil*. https://www.tecmundo.com.br/seguranca/88667-conheca-7-maiores-eventos-hackers-mundo-quatro-do-brasil.htm
34. TV Insider. *How 'Mr. Robot' Gets Its Hacks Right*. https://www.tvinsider.com/32264/how-mr-robot-gets-its-hacks-right/
35. Fox Business. *How the TV show "Mr. Robot" won the prize for hacker realism*. https://www.foxbusiness.com/features/how-the-tv-show-mr-robot-won-the-prize-for-hacker-realism
36. Farnam Street. *The Feynman Learning Technique*. https://fs.blog/feynman-learning-technique/

*Nota de rigor: não consegui confirmar, em fontes independentes, alguns detalhes de cenas de* Operação Vingança *mencionados em análises informais (como o intervalo exato de um gatilho de emergência ou a reconstrução 3D com múltiplos aparelhos); por isso, usei essas ideias apenas como ponto de partida conceitual, e não como fatos do filme. Os números do laboratório vêm de simulações sintéticas com seed fixa e servem como ilustração didática.*

#SegurançaDaInformação #CyberSecurity #BlueTeam #DFIR #EngenhariaSocial #Pentest #Tecnologia
