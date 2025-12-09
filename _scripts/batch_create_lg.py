#!/usr/bin/env python3
"""
Script para criar múltiplos objetos de leitura guiada em lote
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
    "40": {
        "titulo": "Bilhete da Mamãe",
        "texto": [
            {"tipo": "h1", "conteudo": "FILHA,"},
            {"tipo": "p", "conteudo": "SEU SANDUÍCHE ESTÁ NA GELADEIRA. FUI AO MERCADO E JÁ VOLTO."},
            {"tipo": "p", "conteudo": "BEIJOS, MAMÃE"}
        ]
    },
    "51": {
        "titulo": "De Onde Veio o Papel?",
        "texto": [
            {"tipo": "h1", "conteudo": "DE ONDE VEIO O PAPEL?"},
            {"tipo": "p", "conteudo": "SIM, FOI NA CHINA QUE SURGIU O PAPEL. É QUASE CERTO QUE SEU INVENTOR TENHA SIDO UM CHINÊS CHAMADO CAI LUN, QUE FOI ENCARREGADO PELO IMPERADOR DE DESENVOLVER E TESTAR VÁRIAS TECNOLOGIAS E EQUIPAMENTOS. [...]"}
        ]
    },
    "52": {
        "titulo": "Por Que os Camaleões Mudam de Cor?",
        "texto": [
            {"tipo": "h1", "conteudo": "POR QUE OS CAMALEÕES MUDAM DE COR?"},
            {"tipo": "p", "conteudo": "O CAMALEÃO POSSUI CÉLULAS EM SUA PELE QUE SÃO CAPAZES DE MUDAR DE COR DE ACORDO COM AS REAÇÕES DO SISTEMA NERVOSO DO ANIMAL. ISSO ACONTECE PELA NECESSIDADE DE SE CAMUFLAR E SE PROTEGER DE PREDADORES [...]."}
        ]
    },
    "74": {
        "titulo": "Relâmpago",
        "texto": [
            {"tipo": "h1", "conteudo": "RELÂMPAGO"},
            {"tipo": "p", "conteudo": "O MEU CACHORRO RELÂMPAGO ACORDOU-SE COM SARAMPO. VEIO A DONA MANUELA: DEVE SER VARICELA! VEIO A DONA DORA: DEVE SER CATAPORA! E A DONA FABÍOLA: PARECE SER VARÍOLA! POR FIM, A VETERINÁRIA: ACHO TUDO UM DISPARATE, POIS O CACHORRO SE MANCHOU FOI COM MOLHO DE TOMATE!"}
        ]
    },
    "76": {
        "titulo": "A Semana Inteira",
        "texto": [
            {"tipo": "h1", "conteudo": "A SEMANA INTEIRA"},
            {"tipo": "p", "conteudo": "A SEGUNDA FOI À FEIRA, PRECISAVA DE FEIJÃO; A TERÇA FOI À FEIRA, PRA COMPRAR UM PIMENTÃO; A QUARTA FOI À FEIRA, PRA BUSCAR QUIABO E PÃO; A QUINTA FOI À FEIRA, POIS GOSTAVA DE AGRIÃO; A SEXTA FOI À FEIRA, TEM BANANA? TEM MAMÃO? SÁBADO NÃO TEM FEIRA E DOMINGO TAMBÉM NÃO."}
        ]
    },
    "80": {
        "titulo": "Sofia e o Dente de Leite",
        "texto": [
            {"tipo": "h1", "conteudo": "SOFIA E O DENTE DE LEITE"},
            {"tipo": "p", "conteudo": "O QUE VOCÊ SENTIU QUANDO O PRIMEIRO DENTE DE LEITE COMEÇOU A AMOLECER? ELE CAIU DE UMA VEZ OU FICOU BALANÇANDO? DEU MEDO? PEDIU AJUDA A ALGUÉM, MESMO QUE FOSSE À FADA DO DENTE? POIS É. TODO MUNDO PASSA POR ESSAS SITUAÇÕES. SOFIA E O DENTE DE LEITE CONTA, DE FORMA POÉTICA, A AVENTURA DE UMA MENINA DIANTE DO DESAFIO DE ARRANCAR O SEU PRIMEIRO DENTINHO."}
        ]
    },
    "82_1": {
        "titulo": "Sobre o Autor",
        "texto": [
            {"tipo": "h1", "conteudo": "SOBRE O AUTOR"},
            {"tipo": "p", "conteudo": "HENRIQUE RODRIGUES NASCEU NO RIO DE JANEIRO, EM 1975. ESTUDOU LITERATURA POR MUITOS ANOS E PUBLICOU 15 LIVROS PARA CRIANÇAS, JOVENS E ADULTOS. QUANDO ERA PEQUENO, ARRANCOU SOZINHO TODOS OS SEUS DENTES DE LEITE."}
        ]
    },
    "82_2": {
        "titulo": "Sobre a Ilustradora",
        "texto": [
            {"tipo": "h1", "conteudo": "SOBRE A ILUSTRADORA"},
            {"tipo": "p", "conteudo": "BRUNA ASSIS BRASIL NASCEU EM CURITIBA, EM 1986. FORMADA EM JORNALISMO E DESIGN GRÁFICO E PÓS-GRADUADA EM ILUSTRAÇÃO CRIATIVA PELA EINA, DE BARCELONA, NA ESPANHA, SEMPRE TEVE GRANDE INTERESSE PELA ARTE DA FOTOGRAFIA. E FOI ASSIM, MISTURANDO CORES E TEXTURAS REAIS AO TRAÇADO DOS SEUS DESENHOS, QUE ELA SE DESCOBRIU ILUSTRADORA. BRUNA NÃO LARGA SEUS LÁPIS E PAPÉIS POR NADA, A NÃO SER PARA LER UM BOM LIVRO."}
        ]
    }
}

def gerar_timestamps(audio_path, pagina):
    """Gera os timestamps para um arquivo de áudio"""
    print(f"Gerando timestamps para lgp{pagina}...")
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
    timestamp_file = BASE_DIR / "_timestamps" / "1_ano" / f"11_lgp{pagina}.json"
    if timestamp_file.exists():
        with open(timestamp_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def criar_pasta_lgp(pagina):
    """Cria a pasta do objeto de leitura guiada"""
    dest = BASE_DIR / f"lgp{pagina}"
    template = BASE_DIR / "lgp21"

    if dest.exists():
        print(f"Pasta lgp{pagina} já existe, pulando...")
        return False

    print(f"Criando pasta lgp{pagina}...")
    shutil.copytree(template, dest)
    return True

def copiar_arquivos(pagina):
    """Copia áudio, imagem e timestamps"""
    print(f"Copiando arquivos para lgp{pagina}...")

    # Áudio
    audio_src = BASE_DIR / "_assets" / "audios" / "1_ano" / f"11_lgp{pagina}.mp3"
    audio_dest = BASE_DIR / f"lgp{pagina}" / "assets" / "audio" / f"11_lgp{pagina}.mp3"
    if audio_src.exists():
        shutil.copy2(audio_src, audio_dest)

    # Imagem (pode ter ou não o prefixo "11_")
    img_src = BASE_DIR / "_assets" / "imagens" / "1_ano" / f"lgp{pagina}.png"
    if not img_src.exists():
        img_src = BASE_DIR / "_assets" / "imagens" / "1_ano" / f"11_lgp{pagina}.png"

    img_dest = BASE_DIR / f"lgp{pagina}" / "assets" / "images" / f"11_lgp{pagina}.png"
    if img_src.exists():
        shutil.copy2(img_src, img_dest)

    # Timestamps
    ts_src = BASE_DIR / "_timestamps" / "1_ano" / f"11_lgp{pagina}.json"
    ts_dest = BASE_DIR / f"lgp{pagina}" / "timestamps.json"
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
                # Normalizar a palavra do JSON removendo pontuação extra
                palavra_json = word_data['word'].upper()
                palavra_limpa = palavra.upper().replace(',', '').replace('.', '').replace('!', '').replace('?', '').replace(';', '').replace(':', '').replace('[...]', '')

                # Verificar se corresponde (aproximadamente)
                if palavra_limpa in palavra_json or palavra_json in palavra_limpa:
                    span = f'<span data-start="{word_data["start"]}" data-end="{word_data["end"]}">{palavra}</span>'
                    spans.append(span)
                    word_index += 1
                else:
                    # Tentar encontrar a palavra correta
                    spans.append(f'<span data-start="{word_data["start"]}" data-end="{word_data["end"]}">{palavra}</span>')
                    word_index += 1
            else:
                # Sem mais timestamps, usar o último
                if word_index > 0:
                    last_word = words[word_index - 1]
                    spans.append(f'<span data-start="{last_word["end"]}" data-end="{last_word["end"] + 0.5}">{palavra}</span>')

        if tipo == 'h1':
            html_parts.append(('h1', '\n                '.join(spans)))
        else:
            html_parts.append(('p', '\n                    '.join(spans)))

    return html_parts

def atualizar_html(pagina, roteiro_info, timestamps_data):
    """Atualiza o arquivo HTML com o novo roteiro"""
    print(f"Atualizando HTML para lgp{pagina}...")

    html_file = BASE_DIR / f"lgp{pagina}" / "index.html"

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
    p_contents = []

    for tipo, spans in html_spans:
        if tipo == 'h1':
            h1_content = spans
        else:
            p_contents.append(spans)

    # Montar o HTML do artigo
    novo_artigo = f'''            <h1 class="title">
                {h1_content}
            </h1>
            <div class="text-content" id="lyrics" aria-live="polite">
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
    content = content.replace('11_lgp21.mp3', f'11_lgp{pagina}.mp3')
    content = content.replace('11_lgp21.png', f'11_lgp{pagina}.png')
    content = content.replace('Página 21', f'Página {pagina.replace("_", " ")}')
    content = content.replace('página 21', f'página {pagina.replace("_", " ")}')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

def processar_pagina(pagina):
    """Processa uma página completa"""
    print(f"\n{'='*60}")
    print(f"Processando lgp{pagina}")
    print(f"{'='*60}")

    # Verificar se áudio existe
    audio_path = BASE_DIR / "_assets" / "audios" / "1_ano" / f"11_lgp{pagina}.mp3"
    if not audio_path.exists():
        print(f"Áudio não encontrado: {audio_path}")
        return False

    # Gerar timestamps
    timestamps_data = gerar_timestamps(audio_path, pagina)
    if not timestamps_data:
        print(f"Falha ao gerar timestamps para lgp{pagina}")
        return False

    # Criar pasta
    if not criar_pasta_lgp(pagina):
        print(f"Pasta lgp{pagina} já existe, continuando...")

    # Copiar arquivos
    copiar_arquivos(pagina)

    # Atualizar HTML
    roteiro = ROTEIROS.get(pagina)
    if roteiro:
        atualizar_html(pagina, roteiro, timestamps_data)
    else:
        print(f"Roteiro não encontrado para lgp{pagina}")
        return False

    print(f"[OK] lgp{pagina} criado com sucesso!")
    return True

def main():
    """Função principal"""
    paginas = ["40", "51", "52", "74", "76", "80", "82_1", "82_2"]

    print("Iniciando criação em lote de objetos de leitura guiada...")
    print(f"Total de páginas a processar: {len(paginas)}")

    sucesso = 0
    falhas = 0

    for pagina in paginas:
        try:
            if processar_pagina(pagina):
                sucesso += 1
            else:
                falhas += 1
        except Exception as e:
            print(f"Erro ao processar lgp{pagina}: {e}")
            falhas += 1

    print(f"\n{'='*60}")
    print(f"Processamento concluído!")
    print(f"Sucesso: {sucesso}")
    print(f"Falhas: {falhas}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
