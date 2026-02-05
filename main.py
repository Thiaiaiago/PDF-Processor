from utils import encontrar_pdfs, regra_divisao
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
            page = pdf.pages[24]
            largura = page.width
            altura = page.height

            coluna_esquerda = page.crop((0, 0, largura/2, altura))
            coluna_direita = page.crop((largura/2, 0, largura, altura))
            
            for linha in coluna_esquerda.extract_text_lines():
                if linha['text'].count(' ') < 1:
                    print(linha['text']) 
                    print([char['non_stroking_color'][3] for char in linha['chars']])     