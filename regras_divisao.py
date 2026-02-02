from math import ceil

def deve_dividir(texto, numero_pagina, total_paginas, regras):
    if isinstance(regras[-1], int):
        if (numero_pagina + 1) % (ceil(total_paginas/5)) == 0:
            return True
    else:
        for regra in regras:
            if regra.lower() in texto.lower():
                return True
        
    return False
