import os
import shutil

# variables
typeLog = 'w'
LOG_FILE = 'log.txt'

# functions
def log(tex_t):
    global totalLog, typeLog
    text = tex_t + '\n'

    print(tex_t)

    try:
        with open(LOG_FILE, typeLog, encoding="utf-8") as arquivo:
            arquivo.write(text)
    except Exception as e:
        print(f'[log]: erro ao salvar log -> {e}')

    if typeLog == "w":
        typeLog = 'a'

def listar_arquivos(origem, extensao):
    arquivos_encontrados = []
    for root, _, files in os.walk(origem):
        for file in files:
            if file.lower().endswith(f'.{extensao}'):
                arquivos_encontrados.append(os.path.join(root, file))
    return arquivos_encontrados

def gerar_nome_unico(destino_arquivo):
    if not os.path.exists(destino_arquivo):
        log(f"gerar_nome_unico(): not exists {destino_arquivo}")
        return destino_arquivo
    
    base, ext = os.path.splitext(destino_arquivo)
    contador = 1
    novo_destino = f"{base}_{contador}{ext}"
    while os.path.exists(novo_destino):
        contador += 1
        novo_destino = f"{base}_{contador}{ext}"
    log(f'gerar_nome_unico(): return {novo_destino}')
    return novo_destino

def mover_arquivos_em_lotes(origem, destino, tamanho_lote=100, extensao="unitypackage"):
    if not os.path.exists(destino):
        log(f'mover_arquivos_em_lotes(): criando pasta {destino}')
        os.makedirs(destino)
    
    arquivos = listar_arquivos(origem, extensao)
    if not arquivos:
        log(f"Nenhum arquivo '{extensao}' encontrado na pasta de origem.")
        return
    
    log(f"Total de arquivos '{extensao}' encontrados: {len(arquivos)}")
    lote_atual = 0
    
    while arquivos:
        subpasta_destino = os.path.join(destino, f"lote_{lote_atual}")
        
        if not os.path.exists(subpasta_destino):
            os.makedirs(subpasta_destino)
            arquivos_na_pasta = 0
        else:
            arquivos_na_pasta = len([f for f in os.listdir(subpasta_destino) if f.lower().endswith(f'.{extensao}')])
        
        if arquivos_na_pasta >= tamanho_lote:
            lote_atual += 1
            continue
        
        while arquivos_na_pasta < tamanho_lote and arquivos:
            arquivo = arquivos.pop(0)
            destino_arquivo = os.path.join(subpasta_destino, os.path.basename(arquivo))
            destino_arquivo = gerar_nome_unico(destino_arquivo)
            shutil.move(arquivo, destino_arquivo)
            arquivos_na_pasta += 1
            
        log(f"Lote {lote_atual} agora tem {arquivos_na_pasta} arquivos.")
        lote_atual += 1
    
    log("Arquivos movidos com sucesso.")

def receba(origem1='null', destino1='null'):
    if origem1!='null':
        log(f'[Iniciando]: {type}')
        mover_arquivos_em_lotes(origem=f"{origem1}", destino=f"{destino1}", extensao=f'unitypackage')
    else:
        log('receba(): type sem valor, use receba("unitypackage")')

# Main code - Configurações
log('[log]: iniciando')

log('bota pasta de origem, ex: C:/Users/Pichau/Downloads/')
varorigem1 = input(": ")

log('bota pasta de destino, ex: C:/Users/Pichau/Desktop/')
vardesty = input(": ")

receba(origem1=varorigem1, destino1=vardesty)

log('[log]: end')
