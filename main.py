from utils import encontrar_pdfs, regra_divisao, extrair_tabela_por_linhas_vermelhas
from leitor_pdf import dividir_pdf
import pdfplumber, json

# regras = regra_divisao("arquivos")
# print("Regras de divisão:", regras)

for arquivo in encontrar_pdfs("arquivos/pastateste"):          
    if arquivo.lower().endswith(".pdf"):
        # print("Arquivo encontrado:", arquivo.split("/")[-1])
        # # dividir_pdf(arquivo, regras)
        # with pdfplumber.open(arquivo) as pdf:
            # page = pdf.pages[24]
            # largura = page.width
            # altura = page.height

            # coluna_esquerda = page.crop((0, 0, largura/2, altura))
            # coluna_direita = page.crop((largura/2, 0, largura, altura))

        #     texto_esq = coluna_esquerda.extract_text()
        #     texto_dir = coluna_direita.extract_text()

            
        # print("Texto da coluna da esquerda:\n", texto_esq)
        # print("Texto da coluna da direita:\n", texto_dir)
        # print("--------------------------------------------------")
        # formatted_esq_texto = json.dumps(texto_esq, indent=2, ensure_ascii=False).replace('-\\n', '')
        # for linha in texto_esq.split('\n'):
        #     if not linha.endswith(('.', '!', '?')) and linha.count(' ') >= 1:
        #         linha = linha.replace('\\n', ' ')
        #         formatted_esq_texto = formatted_esq_texto.replace(linha + '\\n', linha + ' ')
                
        
        # formatted_dir_texto = json.dumps(texto_dir, indent=2, ensure_ascii=False).replace('-\\n', '')
        # for linha in texto_dir.split('\n'):
        #     if not linha.endswith(('.', '!', '?')) and linha.count(' ') >= 1:
        #         linha = linha.replace('\\n', ' ')
        #         formatted_dir_texto = formatted_dir_texto.replace(linha + '\\n', linha + ' ')
                
        # formatted_texto_completo = formatted_esq_texto + '\n' + formatted_dir_texto  
        # print("Texto completo formatado como JSON:\n", formatted_texto_completo)
        
        with pdfplumber.open(arquivo) as pdf:
            class Topico:
                def __init__(self, texto, tamanho_fonte=None, cor_fonte=None):
                    self.texto = texto
                    self.tamanho_fonte = tamanho_fonte
                    self.cor_fonte = cor_fonte if cor_fonte is None else cor_fonte
                    
                    # Garantir que as cores sejam arrays de 3 posições [R, G, B]
                    if self.cor_fonte is not None and not isinstance(self.cor_fonte, list):
                        self.cor_fonte = [0, 0, 0]
            class Titulo:
                def __init__(self, texto, tamanho_fonte=None, cor_fonte=None):
                    self.texto = texto
                    self.tamanho_fonte = tamanho_fonte
                    self.cor_fonte = cor_fonte if cor_fonte is None else cor_fonte
                    
                    # Garantir que as cores sejam arrays de 3 posições [R, G, B]
                    if self.cor_fonte is not None and not isinstance(self.cor_fonte, list):
                        self.cor_fonte = [0, 0, 0]
            class Subtitulo:
                def __init__(self, texto, tamanho_fonte=None, cor_fonte=None):
                    self.texto = texto
                    self.tamanho_fonte = tamanho_fonte
                    self.cor_fonte = cor_fonte if cor_fonte is None else cor_fonte
                    
                    # Garantir que as cores sejam arrays de 3 posições [R, G, B]
                    if self.cor_fonte is not None and not isinstance(self.cor_fonte, list):
                        self.cor_fonte = [0, 0, 0]
            class Tabela:
                def __init__(self, texto, tamanho_fonte=None, cor_fonte=None):
                    self.texto = texto
                    self.tamanho_fonte = tamanho_fonte
                    self.cor_fonte = cor_fonte if cor_fonte is None else cor_fonte
                    
                    # Garantir que as cores sejam arrays de 3 posições [R, G, B]
                    if self.cor_fonte is not None and not isinstance(self.cor_fonte, list):
                        self.cor_fonte = [0, 0, 0]

            # titulo_obj = Titulo("Meu Título")
            # subtitulo_obj = Subtitulo("Meu Subtítulo")

            # topico_obj = Topico(titulo_obj, subtitulo_obj)

            # print(f"Título: {topico_obj.titulo.texto}")
            # print(f"Subtítulo: {topico_obj.subtitulo.texto}")

            page = pdf.pages[23]
            largura = page.width
            altura = page.height-32 # cortar rodapé

            coluna_esquerda = page.crop((0, 0, largura/2, altura))
            coluna_direita = page.crop((largura/2, 0, largura, altura))

            pagina_completa = coluna_esquerda.extract_text_lines() + coluna_direita.extract_text_lines()
            for linha in pagina_completa:
                R, G, B, tam_fonte = linha['chars'][0]['non_stroking_color'][0], linha['chars'][0]['non_stroking_color'][1], linha['chars'][0]['non_stroking_color'][2], linha['chars'][0]['size']
                params_title = all(pixel_color*255 > 200 for pixel_color in (R, G, B)) and tam_fonte >= 15
                
                # print(params_title)
                if 'Tabela' in linha['text']:
                    list_tabela = Tabela(linha['text'], tam_fonte, [R, G, B])
                    # print(linha['chars'][0])
                if (params_title):
                    print(linha['text'])
                    print(tam_fonte)

                    

            # for linha in coluna_direita.extract_text_lines():
            #     cores_por_char = [
            #         (R, G, B)
            #         for char in linha['chars']
            #         if any(pixel_color != 0 for pixel_color in char['non_stroking_color'])
            #         for R, G, B in [tuple(pixel_color * 255 for pixel_color in char['non_stroking_color'])]
            #         if R > G and R > B
            #     ]
            #     if cores_por_char != []:
            #         print(linha['text'])

            cropped = extrair_tabela_por_linhas_vermelhas(pdf.pages[23])
            # cropped.to_image(resolution=200).show()