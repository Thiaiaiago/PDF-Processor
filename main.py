from utils import encontrar_pdfs, regra_divisao
from leitor_pdf import dividir_pdf

regras = regra_divisao("arquivos")
print("Regras de divisão:", regras)

for arquivo in encontrar_pdfs("arquivos/pastateste"):          
    if arquivo.lower().endswith(".pdf"):
        print("Arquivo encontrado:", arquivo.split("/")[-1])
        dividir_pdf(arquivo, regras)
