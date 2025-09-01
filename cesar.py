def cifrar_cesar(texto, desplazamiento):
    texto = texto.lower()
    resultado = ""
    
    # Ajustar desplazamiento si es mayor a 26
    desplazamiento = desplazamiento % 26
    
    for caracter in texto:
        if caracter.isalpha():
            # Convertir a código ASCII y aplicar desplazamiento
            codigo = ord(caracter)
            codigo_cifrado = (codigo - ord('a') + desplazamiento) % 26 + ord('a')
            resultado += chr(codigo_cifrado)
        else:
            # Mantener caracteres no alfabéticos sin cambios
            resultado += caracter
    
    return resultado

def descifrar_cesar(texto_cifrado, desplazamiento):
    # Para descifrar, usamos un desplazamiento negativo
    return cifrar_cesar(texto_cifrado, -desplazamiento)

def main():
    print("=== CIFRADO CÉSAR ===")
    
    # Solicitar texto al usuario
    texto = input("Ingrese el texto: ")
    
    # Solicitar desplazamiento (manejar entrada no numérica)
    while True:
        try:
            desplazamiento = int(input("Ingrese el desplazamiento: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Cifrar el texto
    texto_cifrado = cifrar_cesar(texto, desplazamiento)
    print(f"\nTexto cifrado: {texto_cifrado}")
    
    # Descifrar para verificar
    texto_descifrado = descifrar_cesar(texto_cifrado, desplazamiento)
    print(f"Texto descifrado: {texto_descifrado}")
    
    # Verificar que el descifrado sea igual al original (en minúsculas)
    if texto_descifrado == texto.lower():
        print("✓ El descifrado coincide con el texto original")
    else:
        print("✗ Error: El descifrado no coincide")

if __name__ == "__main__":
    main()