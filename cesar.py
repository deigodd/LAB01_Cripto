def cifrar_cesar(texto, desplazamiento):
    """
    Cifra texto usando el algoritmo César
    Convierte todo a minúsculas y maneja desplazamientos grandes
    """
    texto = texto.lower()
    texto_cifrado = ""
    
    # Calcular desplazamiento efectivo (módulo 26)
    desplazamiento_efectivo = desplazamiento % 26
    if desplazamiento_efectivo == 0:
        desplazamiento_efectivo = 26
    
    for caracter in texto:
        if caracter.isalpha():
            base = ord('a')
            codigo = ord(caracter) - base
            nuevo_codigo = (codigo + desplazamiento_efectivo) % 26
            nuevo_caracter = chr(base + nuevo_codigo)
            texto_cifrado += nuevo_caracter
        else:
            texto_cifrado += caracter
    
    return texto_cifrado

def descifrar_cesar(texto_cifrado, desplazamiento):
    """
    Descifra texto cifrado con César
    """
    desplazamiento_efectivo = (-desplazamiento) % 26
    if desplazamiento_efectivo == 0:
        desplazamiento_efectivo = 26
    
    texto = texto_cifrado.lower()
    texto_descifrado = ""
    
    for caracter in texto:
        if caracter.isalpha():
            base = ord('a')
            codigo = ord(caracter) - base
            nuevo_codigo = (codigo + desplazamiento_efectivo) % 26
            texto_descifrado += chr(base + nuevo_codigo)
        else:
            texto_descifrado += caracter
    
    return texto_descifrado

# Programa principal - solo se ejecuta si se llama directamente
if __name__ == "__main__":
    print("este es cesar.py")
    texto_original = input("Ingrese el texto a cifrar: ")
    desplazamiento = int(input("Ingrese el desplazamiento: "))

    texto_cifrado = cifrar_cesar(texto_original, desplazamiento)
    print(f"Texto cifrado: {texto_cifrado}")

    texto_descifrado = descifrar_cesar(texto_cifrado, desplazamiento)
    print(f"Texto descifrado: {texto_descifrado}")