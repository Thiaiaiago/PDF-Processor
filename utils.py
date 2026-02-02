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