from PyPDF2 import PdfReader, PdfWriter
from regras_divisao import deve_dividir

def dividir_pdf(caminho_pdf, regras):
    leitor = PdfReader(caminho_pdf)
    escritor = PdfWriter()
    
    if not caminho_pdf.endswith(".pdf"):
        caminho_pdf = caminho_pdf.replace(caminho_pdf.split(".")[-1], ".pdf")
        
    nome_base = caminho_pdf.split("/")[-1].replace(".pdf", "")
    contador = 1

    for i, pagina in enumerate(leitor.pages):
        escritor.add_page(pagina)

        texto = pagina.extract_text() or ""
        if deve_dividir(texto, i, leitor._get_num_pages(), regras):
            salvar_pdf(escritor, nome_base, contador)
            escritor = PdfWriter()
            contador += 1

    if escritor.pages:
        salvar_pdf(escritor, nome_base, contador)

def salvar_pdf(escritor, nome_base, contador):
    nome_arquivo = f"{nome_base}_parte_{contador}.pdf"
    with open("saida/" + nome_arquivo, "wb") as f:
        escritor.write(f)
    print(f"Arquivo salvo: {nome_arquivo}")
