from leitor_pdf import dividir_pdf
import os

def encontrar_pdfs(pasta):
    pdfs = []
    for arquivo in os.listdir(pasta):
        if arquivo.split(".")[0] == arquivo.split(".")[-1]:
            pdfs.append(encontrar_pdfs(pasta + "/" + arquivo)[-1])
        else:
            pdfs.append(pasta + "/" + arquivo)    
        
    return pdfs

def regra_divisao(pasta):
    for arquivo in os.listdir(pasta):
        print(arquivo)
        if arquivo.split('/')[-1] == "regras_divisao.txt":
            with open(pasta + "/" + arquivo, "r", encoding='utf-8') as f:
                return f.read().split(',')
            
    return ["divide by", 5]


def destaca_tabelas(pagina):
    """Detecta e recorta a área de uma tabela baseada em linhas vermelhas decorativas.

    Args:
        pagina: Um objeto `pdfplumber.page.Page`.
        rodape: Altura a ser cortada do rodapé (em pontos).
        mostrar: Se True, desenha círculos e imprime retângulos detectados.

    Returns:
        cropped_page: página recortada à área delimitada pelas linhas vermelhas (ou None se não encontrado).
    """

    largura = pagina.width
    altura = pagina.height - 32

    page_crop = pagina.crop((0, 0, largura, altura))

    def _eh_vermelho(color):
        if not color or len(color) < 3:
            return False
        r, g, b = color[:3]
        return 0.65 <= r <= 0.85 and 0.1 <= g <= 0.25 and 0.1 <= b <= 0.25

    elementos_vermelhos = [
        obj
        for obj in page_crop.rects + page_crop.curves
        if _eh_vermelho(obj.get("non_stroking_color"))
        or _eh_vermelho(obj.get("stroking_color"))
    ]

    red_rects = []
    for elem in sorted(elementos_vermelhos, key=lambda e: e.get("y1", 0)):
        if not red_rects:
            red_rects.append(elem.copy())
            continue

        last = red_rects[-1]
        if abs(elem.get("y1", 0) - last.get("y1", 0)) <= 5:
            last["x0"] = min(last.get("x0", 0), elem.get("x0", 0))
            last["y0"] = min(last.get("y0", 0), elem.get("y0", 0))
            last["x1"] = max(last.get("x1", 0), elem.get("x1", 0))
            last["y1"] = max(last.get("y1", 0), elem.get("y1", 0))
        else:
            red_rects.append(elem.copy())

    cropped = None
    if len(red_rects) >= 2:
        bbox = {
            "x0": min(r["x0"] for r in red_rects), "y0": min(r["top"] for r in red_rects),
            "x1": max(r["x1"] for r in red_rects), "y1": max(r["bottom"] for r in red_rects)
        }
        cropped = page_crop.crop((bbox["x0"], bbox["y0"], bbox["x1"], bbox["y1"]))

    return cropped

def crop_page(pagina, rodape, cabecalho, margemEsq, margemDir):
    
    largura = pagina.width -margemDir
    altura = pagina.height - rodape

    page_crop = pagina.crop((margemEsq, cabecalho, largura, altura))

    return page_crop


def ajustar_linha(x_teorico, words, margem=15):
        """ Tenta mover o x_teorico para um espaço vazio próximo """
            
        conflitos = [w for w in words if abs(w['x0'] - x_teorico) < margem or abs(w['x1'] - x_teorico) < margem]
        
        if not conflitos:
            return x_teorico 
        
        esquerdas = [w['x1'] for w in conflitos if w['x1'] < x_teorico]
        direitas = [w['x0'] for w in conflitos if w['x0'] > x_teorico]
        
        novo_x = x_teorico
        if esquerdas and direitas:
            novo_x = (max(esquerdas) + min(direitas)) / 2
        elif esquerdas:
            novo_x = max(esquerdas) + 2 
        elif direitas:
            novo_x = min(direitas) - 2
            
        return novo_x

def filtrar_e_ajustar_h_lines(h_coords, words, margem_busca=5):
    """ 
    Remove linhas horizontais que estão no 'vazio' 
    e ajusta as que sobraram para os limites do texto.
    """
    h_validadas = []
    
    if not h_coords: return []
    h_validadas.append(h_coords[0])
    
    for y_teorico in h_coords[1:-1]:
        palavras_perto = [
            w for w in words 
            if abs(w['bottom'] - y_teorico) < margem_busca 
            or abs(w['top'] - y_teorico) < margem_busca
        ]
        
        if palavras_perto:
            tops_abaixo = [w['top'] for w in palavras_perto if w['top'] > y_teorico]
            bottoms_acima = [w['bottom'] for w in palavras_perto if w['bottom'] < y_teorico]
            
            if tops_abaixo and bottoms_acima:
                y_ajustado = (max(bottoms_acima) + min(tops_abaixo)) / 2
                h_validadas.append(y_ajustado)
            else:
                h_validadas.append(y_teorico)
                
    h_validadas.append(h_coords[-1])
    return sorted(list(set(h_validadas)))