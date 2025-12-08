# Tutorial: Criando Objetos de Leitura Guiada com Claude Code

Este tutorial explica como criar novas páginas de Leitura Guiada usando o Claude Code, partindo do template `lgp21` já existente.

## Índice

1. [Instalando o Claude Code](#1-instalando-o-claude-code)
2. [Uso Básico do Claude Code](#2-uso-básico-do-claude-code)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Criando um Novo Objeto](#4-criando-um-novo-objeto)
5. [Comandos Úteis](#5-comandos-úteis)

---

## 1. Instalando o Claude Code

### Pré-requisitos

- Node.js (versão 18 ou superior)
- npm (gerenciador de pacotes do Node.js)
- Python 3 (para geração de timestamps)
- ffmpeg (para processamento de áudio)

### Instalação

Abra o terminal e execute:

```bash
npm install -g @anthropic-ai/claude-code
```

### Autenticação

Na primeira execução, você precisará autenticar com sua conta Anthropic:

```bash
claude
```

Siga as instruções na tela para fazer login.

---

## 2. Uso Básico do Claude Code

### Iniciando o Claude Code

Navegue até a pasta do projeto e inicie o Claude Code:

```bash
cd /caminho/para/od_leituras_guiadas
claude
```

### Comandos Básicos

- **Digitar mensagens**: Simplesmente escreva o que você quer fazer e pressione Enter
- **Sair**: Digite `/exit` ou pressione `Ctrl+C`
- **Limpar conversa**: Digite `/clear`
- **Ajuda**: Digite `/help`

### Exemplo de Interação

```
> Crie uma nova pasta chamada lgp36 baseada no template lgp21

Claude irá criar a pasta e copiar os arquivos necessários...
```

---

## 3. Estrutura do Projeto

```
od_leituras_guiadas/
├── _assets/                    # Assets originais (fonte)
│   ├── audios/
│   │   ├── 1_ano/
│   │   └── 2_ano/
│   ├── imagens/
│   │   ├── 1_ano/
│   │   └── 2_ano/
│   └── fonts/
├── _roteiros/                  # Textos dos roteiros (.docx)
├── _timestamps/                # Timestamps gerados
├── scripts/                    # Scripts auxiliares
│   ├── generate_timestamps.py
│   └── requirements.txt
├── lgp21/                      # Exemplo de objeto completo
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── assets/
│       ├── audio/
│       ├── images/
│       └── fonts/
└── tutorial.md
```

### Estrutura de cada Objeto (pasta lgpXX)

Cada objeto é **auto-contido** e possui:

- `index.html` - Página principal
- `css/style.css` - Estilos
- `js/script.js` - Funcionalidades (karaoke, modal, zoom)
- `assets/audio/` - Arquivo de áudio (.mp3)
- `assets/images/` - Imagem do texto completo + logos
- `assets/fonts/` - Fontes Inter

---

## 4. Criando um Novo Objeto

### Passo 1: Identificar os Assets

Localize nos arquivos originais:
- **Áudio**: `_assets/audios/[ano]/[arquivo].mp3`
- **Imagem**: `_assets/imagens/[ano]/[arquivo].png`
- **Texto**: `_roteiros/[ano]ANO_leitura_guiada.docx`

### Passo 2: Gerar Timestamps

Primeiro, instale as dependências (apenas na primeira vez):

```bash
pip install -r scripts/requirements.txt
```

Gere os timestamps do áudio:

```bash
python scripts/generate_timestamps.py _assets/audios/1_ano/[arquivo].mp3 --language pt
```

O arquivo JSON será salvo em `_timestamps/1_ano/[arquivo].json`

### Passo 3: Pedir ao Claude Code para Criar o Objeto

Inicie o Claude Code e faça o pedido:

```
> Crie um novo objeto de leitura guiada chamado "lgp36" usando:
> - Áudio: _assets/audios/1_ano/11_lgp36.mp3
> - Imagem: _assets/imagens/1_ano/11_lgp36.png
> - Timestamps: _timestamps/1_ano/11_lgp36.json
> - Texto do roteiro: [cole o texto aqui ou referencie o arquivo]
>
> Use o lgp21 como template.
```

### Passo 4: Revisar e Ajustar

O Claude irá:
1. Criar a pasta `lgp36/`
2. Copiar os arquivos base do template
3. Atualizar os caminhos dos assets
4. Inserir o texto com os timestamps word-by-word

Revise o resultado e peça ajustes se necessário:

```
> O título está errado, deveria ser "NOME DO TEXTO"
```

```
> Ajuste o timestamp da palavra "EXEMPLO" para começar em 5.2 segundos
```

---

## 5. Comandos Úteis

### Pedidos Comuns ao Claude Code

**Criar novo objeto completo:**
```
Crie o objeto lgpXX baseado no template lgp21, usando o áudio XX_lgpXX.mp3
e a imagem XX_lgpXX.png da pasta 1_ano. O texto é: [texto aqui]
```

**Gerar timestamps:**
```
Gere os timestamps para o áudio _assets/audios/1_ano/XX_lgpXX.mp3
```

**Ajustar timestamp específico:**
```
No arquivo lgpXX/index.html, ajuste o timestamp da palavra "PALAVRA"
para data-start="X.XX" data-end="X.XX"
```

**Corrigir texto:**
```
No lgpXX/index.html, corrija a palavra "ERRADA" para "CORRETA"
```

**Verificar estrutura:**
```
Liste todos os arquivos dentro da pasta lgpXX
```

---

## Dicas

1. **Sempre use o lgp21 como referência** - É o template completo e testado

2. **Verifique os timestamps** - A IA pode errar algumas palavras. Teste o áudio e ajuste manualmente se necessário

3. **Teste localmente** - Use um servidor local para testar:
   ```bash
   cd lgpXX
   python3 -m http.server 8000
   ```
   Acesse: `http://localhost:8000`

4. **HandTalk só funciona online** - O widget de acessibilidade só aparece quando a página está hospedada no domínio autorizado

5. **Seja específico nos pedidos** - Quanto mais detalhes você der ao Claude, melhor será o resultado

---

## Exemplo Completo

```
> Preciso criar o objeto lgp36.
>
> O áudio está em _assets/audios/1_ano/11_lgp36.mp3
> A imagem está em _assets/imagens/1_ano/11_lgp36.png
>
> Primeiro gere os timestamps do áudio, depois crie a pasta lgp36
> copiando a estrutura do lgp21 e atualize o HTML com o texto e
> timestamps corretos.
>
> O título é: "TÍTULO DO TEXTO"
>
> O texto é:
> PRIMEIRA FRASE DO TEXTO.
> SEGUNDA FRASE DO TEXTO.
> TERCEIRA FRASE DO TEXTO.
```

O Claude irá executar todos os passos automaticamente e você terá um novo objeto pronto para uso.

---

## Suporte

Em caso de dúvidas sobre o Claude Code:
- Documentação oficial: https://docs.anthropic.com/claude-code
- Dentro do Claude Code, digite `/help` para ver comandos disponíveis
