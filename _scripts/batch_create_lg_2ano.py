#!/usr/bin/env python3
"""
Script para criar múltiplos objetos de leitura guiada do 2º ano em lote
"""
import os
import shutil
import subprocess
import json
from pathlib import Path

# Diretório base
BASE_DIR = Path(r"C:\programacao\od_leituras_guiadas")

# Mapeamento de páginas para roteiros
ROTEIROS = {
    "15": {
        "titulo": "Receita de Brigadeiro",
        "texto": [
            {"tipo": "h1", "conteudo": "RECEITA DE BRIGADEIRO"},
            {"tipo": "h2", "conteudo": "INGREDIENTES"},
            {"tipo": "p", "conteudo": "2 LATAS DE LEITE CONDENSADO 8 COLHERES (SOPA) DE CHOCOLATE EM PÓ 4 COLHERES (SOPA) DE MANTEIGA CHOCOLATE GRANULADO"},
            {"tipo": "h2", "conteudo": "PREPARO"},
            {"tipo": "p", "conteudo": "COLOQUE O LEITE CONDENSADO, O CHOCOLATE EM PÓ E A MANTEIGA EM UMA PANELA. LEVE AO FOGO E MEXA ATÉ QUE A MISTURA SE DESPRENDA DO FUNDO DELA. ESPERE ESFRIAR E, COM AS MÃOS UNTADAS, FAÇA BOLINHAS E PASSE-AS NO CHOCOLATE GRANULADO."},
            {"tipo": "p", "conteudo": "RENDIMENTO: 50 BRIGADEIROS"},
            {"tipo": "p", "conteudo": "CADERNO DE RECEITAS DA AUTORA."}
        ]
    },
    "17": {
        "titulo": "O Que É, O Que É?",
        "texto": [
            {"tipo": "h1", "conteudo": "O QUE É, O QUE É?"},
            {"tipo": "p", "conteudo": "VENHO AO MUNDO RASTEJANDO, TUDO OBRA DA NATUREZA. UM BELO DIA SAIO VOANDO, MOSTRANDO MINHA BELEZA."}
        ]
    },
    "22": {
        "titulo": "A Pia e o Pinto",
        "texto": [
            {"tipo": "h1", "conteudo": "A PIA E O PINTO"},
            {"tipo": "p", "conteudo": "A PIA PERTO DO PINTO, O PINTO PERTO DA PIA. QUANTO MAIS A PIA PINGA MAIS O PINTO PIA. A PIA PINGA, O PINTO PIA, PINGA A PIA, PIA O PINTO. O PINTO PERTO DA PIA, A PIA PERTO DO PINTO."}
        ]
    },
    "25": {
        "titulo": "Diário da Carol",
        "texto": [
            {"tipo": "h1", "conteudo": "SALVADOR, 17 DE DEZEMBRO."},
            {"tipo": "p", "conteudo": "QUERIDO DIÁRIO, HOJE ESTOU MUITO FELIZ! DEPOIS DE MUITO TEMPO, ENCONTREI MINHA MELHOR AMIGA, JULIANA. ELA SE MUDOU PARA OUTRA CIDADE E VEIO PASSAR AS FÉRIAS NA CASA DE SUA AVÓ. FOMOS TOMAR SORVETE JUNTAS E, DEPOIS, BRINCAMOS NO PARQUE PERTO DA MINHA CASA. COMBINAMOS DE SAIR NOVAMENTE NO SÁBADO DO PRÓXIMO FINAL DE SEMANA, DAQUI A QUATRO DIAS. ESPERO QUE SEJA UM DIA ESPECIAL COMO FOI HOJE."},
            {"tipo": "p", "conteudo": "CAROL"}
        ]
    },
    "28": {
        "titulo": "Diário do Caetano",
        "texto": [
            {"tipo": "h1", "conteudo": "PIRAQUARA, 25 DE JANEIRO."},
            {"tipo": "p", "conteudo": "E AÍ, AMIGÃO! NOSSA, HOJE ACONTECEU ALGO SURPREENDENTE COMIGO. ESTOU ATÉ AGORA EM CHOQUE. EU VI UM BEZERRO NASCER! SIM! OU MELHOR, VI? NÃO. EU AJUDEI UM ANIMAL A NASCER. FOI ESPETACULAR. AJUDEI MEU PAI A FAZER O PARTO DA NOSSA VAQUINHA, A QUERIDA MIMOSA. EU AINDA NÃO ACREDITO NO QUE VIVI. QUE LEGAL!!! NUNCA MAIS VOU ME ESQUECER DESSE DIA. POR ISSO, VIM CORRENDO AQUI ESCREVER, POIS ESSA LEMBRANÇA MERECE SER GUARDADA."},
            {"tipo": "p", "conteudo": "VALEU, ATÉ AMANHÃ. CAETANO"}
        ]
    },
    "35": {
        "titulo": "O Macaco Foi à Feira",
        "texto": [
            {"tipo": "h1", "conteudo": "O MACACO FOI À FEIRA"},
            {"tipo": "p", "conteudo": "O MACACO FOI À FEIRA NÃO SABIA O QUE COMPRAR COMPROU UMA CADEIRA PARA A COMADRE SE SENTAR A COMADRE SE SENTOU A CADEIRA ESBORRACHOU COITADA DA COMADRE FOI PARAR NO CORREDOR"}
        ]
    },
    "38": {
        "titulo": "Jogos e Alimentação Saudável",
        "texto": [
            {"tipo": "h1", "conteudo": "JOGOS MOSTRAM ÀS CRIANÇAS COMO MANTER ALIMENTAÇÃO SAUDÁVEL"},
            {"tipo": "p", "conteudo": "APRENDER A COMER BEM É UMA LIÇÃO PARA A VIDA INTEIRA. TANTO EM CASA QUANTO NA ESCOLA, É IMPORTANTE QUE AS CRIANÇAS SIGAM UMA DIETA EQUILIBRADA PARA SE MANTEREM SAUDÁVEIS. MAS COMO ESTIMULAR ESSE PÚBLICO A CONSUMIR ALIMENTOS MAIS NUTRITIVOS? UMA IDEIA PARA DESPERTAR O CUIDADO COM A ALIMENTAÇÃO É POR MEIO DA UTILIZAÇÃO DE JOGOS EDUCATIVOS. EXISTEM OPÇÕES DISPONÍVEIS GRATUITAMENTE PELA INTERNET E OFERECEMOS ALGUMAS SUGESTÕES DELAS [...]: FOME DE QUÊ? – NESTE JOGO, O USUÁRIO RECEBE INFORMAÇÕES SOBRE UM DETERMINADO ALIMENTO E PRECISA ESCOLHER QUAL OPÇÃO CORRESPONDE A CADA DESCRIÇÃO, SOMANDO, ASSIM, ERROS E ACERTOS. JOGO DA PIRÂMIDE DOS ALIMENTOS – ENQUANTO DIVERSOS ALIMENTOS PASSAM POR UMA ESTEIRA E O CONTADOR DE TEMPO CORRE, A CRIANÇA DEVE ESCOLHER EM QUAL CATEGORIA CADA UM SE ENCAIXA."}
        ]
    },
    "42": {
        "titulo": "Uniforme",
        "texto": [
            {"tipo": "h1", "conteudo": "II – UNIFORME"},
            {"tipo": "p", "conteudo": "É OBRIGATÓRIO O USO DO UNIFORME PARA OS ALUNOS DOS TURNOS DA MANHÃ E DA TARDE, CONFORME INDICADO NA CARTEIRINHA. QUALQUER SITUAÇÃO QUE IMPOSSIBILITE O USO DO UNIFORME DEVE SER COMUNICADA PELOS RESPONSÁVEIS VIA AGENDA."}
        ]
    },
    "44": {
        "titulo": "Recreio",
        "texto": [
            {"tipo": "h1", "conteudo": "III – RECREIO"},
            {"tipo": "p", "conteudo": "DURANTE O RECREIO, OS ALUNOS NÃO PODEM PERMANECER EM SALA DE AULA, NOS CORREDORES E NAS ESCADARIAS DOS BLOCOS. NESSE PERÍODO, DEVEM FICAR NOS ESPAÇOS DESTINADOS AO RECREIO, OU SEJA, NA QUADRA, NO PÁTIO E NA ÁREA DA CANTINA."}
        ]
    },
    "46": {
        "titulo": "Convite Safari",
        "texto": [
            {"tipo": "h1", "conteudo": "SOFIA,"},
            {"tipo": "p", "conteudo": "VAMOS NOS AVENTURAR EM UM SAFARI PARA FESTEJAR O ANIVERSÁRIO DE 7 ANOS DO PEDRO!"},
            {"tipo": "p", "conteudo": "DIA: 12 DE MAIO HORÁRIO: 14 HORAS LOCAL: RUA VIOLETA, Nº 100"}
        ]
    },
    "49": {
        "titulo": "Convite Bazar Solidário",
        "texto": [
            {"tipo": "h1", "conteudo": "CONVITE PARA BAZAR SOLIDÁRIO"},
            {"tipo": "p", "conteudo": "VOCÊ É NOSSO CONVIDADO ESPECIAL! A ASSOCIAÇÃO DE MORADORES VILA FELIZ CONVIDA PARA O BAZAR SOLIDÁRIO. VENHA NOS AJUDAR E APROVEITE PARA ENCONTRAR ROUPAS, ACESSÓRIOS, BRINQUEDOS, ARTIGOS DE DECORAÇÃO E MUITO MAIS! A ARRECADAÇÃO SERÁ DESTINADA À COMPRA DE ALIMENTOS PARA O NATAL DAS FAMÍLIAS. PARA MAIS INFORMAÇÕES, ENTRE EM CONTATO COM NOSSOS VOLUNTÁRIOS."},
            {"tipo": "p", "conteudo": "INFORMAÇÕES: DATA: 09/12 HORÁRIO: DAS 10 H ÀS 17 H. LOCAL: QUADRA DA ESCOLA SÃO LEOPOLDO."}
        ]
    },
    "62": {
        "titulo": "Colecionador de Cheiros",
        "texto": [
            {"tipo": "h1", "conteudo": "COLECIONADOR DE CHEIROS"},
            {"tipo": "p", "conteudo": "COLECIONADOR DE CHEIROS TROCA UM CHEIRO DE CIDADE POR UM CHEIRO DE NEBLINA UM CHEIRO DE GASOLINA POR UM CHEIRO DE CHUVA FINA UM CHEIRO DE CIMENTO POR UM CHEIRO DE ORVALHO NO VENTO"}
        ]
    },
    "64": {
        "titulo": "A Semana Inteira",
        "texto": [
            {"tipo": "h1", "conteudo": "A SEMANA INTEIRA"},
            {"tipo": "p", "conteudo": "A SEGUNDA FOI À FEIRA, PRECISAVA DE FEIJÃO; A TERÇA FOI À FEIRA, PRA COMPRAR UM PIMENTÃO; A QUARTA FOI À FEIRA, PRA BUSCAR QUIABO E PÃO; A QUINTA FOI À FEIRA, POIS GOSTAVA DE AGRIÃO; A SEXTA FOI À FEIRA, TEM BANANA? TEM MAMÃO? SÁBADO NÃO TEM FEIRA E DOMINGO TAMBÉM NÃO."}
        ]
    },
    "66": {
        "titulo": "Entrevista Mauricio de Sousa",
        "texto": [
            {"tipo": "h1", "conteudo": "EM ENTREVISTA, MAURICIO DE SOUSA ASSOCIA A OBRA À AMIZADE E À INGENUIDADE"},
            {"tipo": "p", "conteudo": "[...] AOS 83 ANOS, E À FRENTE DE EMPRESA QUE COMPLETA 60 ANOS, MAURICIO DE SOUSA SOUBE ESTUDAR, ESQUEMATIZAR UM PROCESSO DE PRODUÇÃO E, AO MESMO TEMPO, ENTENDER COMO CONTA, O QUE PEGA O LEITOR NO CORAÇÃO, NA MENTE, NAS SENSAÇÕES E ATÉ NAS SAUDADES. [...] QUE TIPO DE CINEMA CHAMA A SUA ATENÇÃO? O QUE ME PRENDE AO FILME, QUANDO EU VOU AO CINEMA, É O ROTEIRO. ALIÁS, É O MAIS IMPORTANTE TAMBÉM NA HISTÓRIA EM QUADRINHO. ENTÃO, EU VEJO FILME DESDE CRIANÇA, MUITO CRIANÇA; MEU PAI ME LEVAVA QUASE TODA NOITE AO CINEMA, ATRAVESSEI ANOS ASSISTINDO A FILMES, PRINCIPALMENTE NOS ANOS 1940 E 1950. O QUE MANTÉM TANTA UNIÃO EM SEUS PERSONAGENS? : # 'EU TIVE UMA INFÂNCIA PRIVILEGIADA. EM TERMOS DE FAMÍLIA, DE BRINCAR NA RUA, AINDA SEM MUITO MOVIMENTO DE CARROS. TIVE AMIGOS DE TODAS ETNIAS POSSÍVEIS, NA MINHA RUA; EM DOIS QUARTEIRÕES, TINHA GENTE DO MUNDO INTEIRO, E EU BRINCAVA E BRIGAVA COM ESTE PESSOAL. TIVE UMA FAMÍLIA QUE ME APOIOU EM TUDO, DESDE QUANDO EU COMECEI A DESENHAR, BEM PEQUENO. MEU PAI ME ENSINAVA TRUQUES DE DESENHO, DE PINTURA TAMBÉM. MINHA MÃE ERA POETISA. '"}
        ]
    },
    "73": {
        "titulo": "A Formiga, a Cigarra e a Centopeia",
        "texto": [
            {"tipo": "h1", "conteudo": "A FORMIGA, A CIGARRA E A CENTOPEIA"},
            {"tipo": "p", "conteudo": "A FORMIGA, A CIGARRA E A CENTOPEIA COMBINARAM UM ENCONTRO NA CASA DA FORMIGA. A CIGARRA CHEGOU NA HORA MARCADA, MAS A CENTOPEIA SÓ DEPOIS DE UMA HORA. A FORMIGA PERGUNTOU: – POR QUE VOCÊ DEMOROU TANTO? – É PORQUE TEM UM AVISO NA PORTA ESCRITO ASSIM: 'POR FAVOR, LIMPE OS PÉS'."}
        ]
    },
    "81": {
        "titulo": "O Cão e a Sombra",
        "texto": [
            {"tipo": "h1", "conteudo": "O CÃO E A SOMBRA"},
            {"tipo": "p", "conteudo": "UM CÃO LEVAVA NA BOCA UM PEDAÇO DE CARNE QUANDO, AO PASSAR POR UM RIACHO, VIU NO FUNDO DA ÁGUA A SOMBRA DE UMA CARNE QUE PARECIA MAIOR. SOLTOU A QUE LEVAVA NOS DENTES PARA TENTAR PEGAR A QUE VIA NA ÁGUA. O RIACHO LEVOU PARA SUA CORRENTEZA A VERDADEIRA CARNE E A SOMBRA, FICANDO O CÃO SEM UMA NEM OUTRA."}
        ]
    },
    "83": {
        "titulo": "A Lebre e a Tartaruga",
        "texto": [
            {"tipo": "h1", "conteudo": "A LEBRE E A TARTARUGA"},
            {"tipo": "p", "conteudo": "A TARTARUGA DESAFIA A LEBRE PARA UMA CORRIDA. ESTA, MESMO ACHANDO A PROPOSTA ABSURDA, ACEITA A DISPUTA. É DADA A LARGADA, A TARTARUGA SAI NA FRENTE, ENQUANTO A LEBRE FAZ QUESTÃO DE DEMORAR; ELA BRINCA, COME, DESCANSA, ATÉ QUE RESOLVE ENCARAR A CORRIDA. MAS AÍ JÁ É TARDE, E A TARTARUGA CHEGA ANTES DELA. CORRER NÃO É A SOLUÇÃO – A PESSOA PRECAVIDA NÃO SE ATRASA NA SAÍDA."}
        ]
    },
    "91": {
        "titulo": "A Princesa e a Ervilha - Parte 1",
        "texto": [
            {"tipo": "h1", "conteudo": "A PRINCESA E A ERVILHA - PARTE 1"},
            {"tipo": "p", "conteudo": "ERA UMA VEZ UM PRÍNCIPE. ELE DESEJAVA TER A SUA PRINCESA, MAS UMA QUE FOSSE PRINCESA DE VERDADE. POR ISSO VIAJOU PELO MUNDO TODO À PROCURA DE UMA ASSIM, MAS SEMPRE HAVIA ALGUMA COISA DE ERRADO. [...] UMA NOITE, UMA TEMPESTADE TERRÍVEL DESABOU SOBRE O REINO. [...] INESPERADAMENTE, OUVIU-SE UMA BATIDA NO PORTÃO DA CIDADE E O REI EM PESSOA FOI ABRI-LO. HAVIA UMA PRINCESA PARADA LÁ FORA. MAS VALHA-ME DEUS! QUE FIGURA ELA ERA DEBAIXO DAQUELE AGUACEIRO, SOB UM TEMPO DAQUELES! A ÁGUA ESCORRIA PELO SEU CABELO E SUAS ROUPAS. JORRAVA PELAS PONTAS DOS SAPATOS E ENTRAVA DE NOVO PELOS CALCANHARES. E, MESMO ASSIM, ELA INSISTIU QUE ERA UMA VERDADEIRA PRINCESA. 'BEM, ISSO É O QUE VAMOS VER, DAQUI A POUCO!' PENSOU A RAINHA. NÃO DISSE UMA PALAVRA, MAS FOI DIRETO AO QUARTO, DESFEZ A CAMA TODA E PÔS UMA ERVILHA SOBRE O ESTRADO. SOBRE A ERVILHA EMPILHOU VINTE COLCHÕES E DEPOIS ESTENDEU MAIS VINTE EDREDONS DOS MAIS FOFOS POR CIMA DOS COLCHÕES. FOI ALI QUE A PRINCESA DORMIU AQUELA NOITE. [...]"}
        ]
    },
    "93": {
        "titulo": "A Princesa e a Ervilha - Parte 2",
        "texto": [
            {"tipo": "h1", "conteudo": "A PRINCESA E A ERVILHA - PARTE 2"},
            {"tipo": "p", "conteudo": "[...] DE MANHÃ, TODOS PERGUNTARAM COMO ELA HAVIA DORMIDO. 'AH, PESSIMAMENTE!', RESPONDEU A PRINCESA. 'MAL CONSEGUI PREGAR O OLHO A NOITE INTEIRA! SABE DEUS O QUE HAVIA NAQUELA CAMA! ERA UMA COISA TÃO DURA QUE FIQUEI TODA CHEIA DE MANCHAS PRETAS E AZUIS. É REALMENTE MEDONHO.' ENTÃO, É CLARO, TODOS PUDERAM VER QUE ELA ERA REALMENTE UMA PRINCESA, PORQUE TINHA SENTIDO A ERVILHA ATRAVÉS DE VINTE COLCHÕES E DE VINTE EDREDONS. SÓ UMA VERDADEIRA PRINCESA PODIA TER A PELE ASSIM TÃO SENSÍVEL. DIANTE DISSO O PRÍNCIPE SE CASOU COM ELA, POIS AGORA SABIA QUE TINHA UMA PRINCESA DE VERDADE. [...]"}
        ]
    },
    "95": {
        "titulo": "Pedra, Papel, Tesoura",
        "texto": [
            {"tipo": "h1", "conteudo": "PEDRA, PAPEL, TESOURA"},
            {"tipo": "p", "conteudo": "A BRINCADEIRA DE 'PEDRA, PAPEL, TESOURA' É UM JOGO DE MÃOS, EM QUE DOIS JOGADORES ESCOLHEM UMA DAS TRÊS OPÇÕES (PEDRA, PAPEL OU TESOURA) E FAZEM O GESTO CORRESPONDENTE AO MESMO TEMPO. AS REGRAS PARA DETERMINAR QUEM VENCE SÃO: PEDRA GANHA DA TESOURA (PEDRA QUEBRA TESOURA). TESOURA GANHA DO PAPEL (TESOURA CORTA PAPEL). PAPEL GANHA DA PEDRA (PAPEL EMBRULHA PEDRA). SE OS DOIS JOGADORES ESCOLHEREM A MESMA OPÇÃO, A JOGADA FICA EMPATADA. DEPOIS DE CINCO JOGADAS, QUEM GANHOU MAIS VEZES É O GRANDE VENCEDOR."}
        ]
    }
}

def gerar_timestamps(audio_path, pagina):
    """Gera os timestamps para um arquivo de áudio"""
    print(f"Gerando timestamps para 2ano/lgp{pagina}...")
    cmd = [
        "py", "-3.13",
        str(BASE_DIR / "_scripts" / "generate_timestamps.py"),
        str(audio_path),
        "--language", "pt"
    ]
    result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao gerar timestamps: {result.stderr}")
        return None

    # Ler o JSON de timestamps gerado
    timestamp_file = BASE_DIR / "_timestamps" / "2_ano" / f"21_lgp{pagina}.json"
    if timestamp_file.exists():
        with open(timestamp_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def criar_pasta_lgp(pagina):
    """Cria a pasta do objeto de leitura guiada"""
    # Criar estrutura 2_ano
    ano_dir = BASE_DIR / "2_ano"
    ano_dir.mkdir(exist_ok=True)

    dest = ano_dir / f"lgp{pagina}"
    template = BASE_DIR / "lgp21"

    if dest.exists():
        print(f"Pasta 2_ano/lgp{pagina} já existe, pulando...")
        return False

    print(f"Criando pasta 2_ano/lgp{pagina}...")
    shutil.copytree(template, dest)
    return True

def copiar_arquivos(pagina):
    """Copia áudio, imagem e timestamps"""
    print(f"Copiando arquivos para 2_ano/lgp{pagina}...")

    # Áudio
    audio_src = BASE_DIR / "_assets" / "audios" / "2_ano" / f"21_lgp{pagina}.mp3"
    audio_dest = BASE_DIR / "2_ano" / f"lgp{pagina}" / "assets" / "audio" / f"21_lgp{pagina}.mp3"
    if audio_src.exists():
        shutil.copy2(audio_src, audio_dest)

    # Imagem (pode ter ou não o prefixo "21_")
    img_src = BASE_DIR / "_assets" / "imagens" / "2_ano" / f"lgp{pagina}.png"
    if not img_src.exists():
        img_src = BASE_DIR / "_assets" / "imagens" / "2_ano" / f"21_lgp{pagina}.png"

    img_dest = BASE_DIR / "2_ano" / f"lgp{pagina}" / "assets" / "images" / f"21_lgp{pagina}.png"
    if img_src.exists():
        shutil.copy2(img_src, img_dest)

    # Timestamps
    ts_src = BASE_DIR / "_timestamps" / "2_ano" / f"21_lgp{pagina}.json"
    ts_dest = BASE_DIR / "2_ano" / f"lgp{pagina}" / "timestamps.json"
    if ts_src.exists():
        shutil.copy2(ts_src, ts_dest)

def criar_html_spans(timestamps_data, roteiro):
    """Cria os spans HTML com timestamps baseado no roteiro"""
    words = timestamps_data['words']
    word_index = 0
    html_parts = []

    for bloco in roteiro:
        tipo = bloco['tipo']
        texto = bloco['conteudo']
        palavras_texto = texto.split()

        spans = []
        for palavra in palavras_texto:
            if word_index < len(words):
                word_data = words[word_index]
                span = f'<span data-start="{word_data["start"]}" data-end="{word_data["end"]}">{palavra}</span>'
                spans.append(span)
                word_index += 1
            else:
                # Sem mais timestamps, usar o último
                if word_index > 0:
                    last_word = words[word_index - 1]
                    spans.append(f'<span data-start="{last_word["end"]}" data-end="{last_word["end"] + 0.5}">{palavra}</span>')

        html_parts.append((tipo, '\n                    '.join(spans)))

    return html_parts

def atualizar_html(pagina, roteiro_info, timestamps_data):
    """Atualiza o arquivo HTML com o novo roteiro"""
    print(f"Atualizando HTML para 2_ano/lgp{pagina}...")

    html_file = BASE_DIR / "2_ano" / f"lgp{pagina}" / "index.html"

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Atualizar título
    content = content.replace(
        '<title>Leitura Guiada - Regras de Convivência da Turma</title>',
        f'<title>Leitura Guiada - {roteiro_info["titulo"]}</title>'
    )

    # Criar spans HTML
    html_spans = criar_html_spans(timestamps_data, roteiro_info['texto'])

    # Construir novo conteúdo
    h1_content = ""
    h2_contents = []
    p_contents = []

    for tipo, spans in html_spans:
        if tipo == 'h1':
            h1_content = spans
        elif tipo == 'h2':
            h2_contents.append(spans)
        else:
            p_contents.append(spans)

    # Montar o HTML do artigo
    novo_artigo = f'''            <h1 class="title">
                {h1_content}
            </h1>
            <div class="text-content" id="lyrics" aria-live="polite">
'''

    # Adicionar h2 se houver
    for h2_content in h2_contents:
        novo_artigo += f'''                <h2 class="subtitle">
                    {h2_content}
                </h2>
'''

    for p_content in p_contents:
        novo_artigo += f'''                <p>
                    {p_content}
                </p>
'''

    novo_artigo += '            </div>'

    # Substituir o conteúdo do artigo usando regex
    import re
    pattern = r'<h1 class="title">.*?</div>'
    content = re.sub(pattern, novo_artigo, content, flags=re.DOTALL)

    # Atualizar caminhos de arquivos
    content = content.replace('11_lgp21.mp3', f'21_lgp{pagina}.mp3')
    content = content.replace('11_lgp21.png', f'21_lgp{pagina}.png')
    content = content.replace('Página 21', f'Página {pagina}')
    content = content.replace('página 21', f'página {pagina}')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def processar_pagina(pagina):
    """Processa uma página completa"""
    print(f"\n{'='*60}")
    print(f"Processando 2ano/lgp{pagina}")
    print(f"{'='*60}")

    # Verificar se áudio existe
    audio_path = BASE_DIR / "_assets" / "audios" / "2_ano" / f"21_lgp{pagina}.mp3"
    if not audio_path.exists():
        print(f"Audio nao encontrado: {audio_path}")
        return False

    # Gerar timestamps
    timestamps_data = gerar_timestamps(audio_path, pagina)
    if not timestamps_data:
        print(f"Falha ao gerar timestamps para 2ano/lgp{pagina}")
        return False

    # Criar pasta
    if not criar_pasta_lgp(pagina):
        print(f"Pasta 2_ano/lgp{pagina} ja existe, continuando...")

    # Copiar arquivos
    copiar_arquivos(pagina)

    # Atualizar HTML
    roteiro = ROTEIROS.get(pagina)
    if roteiro:
        atualizar_html(pagina, roteiro, timestamps_data)
    else:
        print(f"Roteiro nao encontrado para lgp{pagina}")
        return False

    print(f"[OK] 2ano/lgp{pagina} criado com sucesso!")
    return True

def main():
    """Função principal"""
    paginas = ["15", "17", "22", "25", "28", "35", "38", "42", "44", "46", "49", "62", "64", "66", "73", "81", "83", "91", "93", "95"]

    print("Iniciando criacao em lote de objetos de leitura guiada do 2o ano...")
    print(f"Total de paginas a processar: {len(paginas)}")

    sucesso = 0
    falhas = 0

    for pagina in paginas:
        try:
            if processar_pagina(pagina):
                sucesso += 1
            else:
                falhas += 1
        except Exception as e:
            print(f"Erro ao processar 2ano/lgp{pagina}: {e}")
            import traceback
            traceback.print_exc()
            falhas += 1

    print(f"\n{'='*60}")
    print(f"Processamento concluido!")
    print(f"Sucesso: {sucesso}")
    print(f"Falhas: {falhas}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
