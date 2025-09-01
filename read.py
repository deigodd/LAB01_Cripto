#!/usr/bin/env python3
"""
Extractor y descifrador de mensajes ICMP con cifrado César
Lee un archivo pcapng y prueba todos los desplazamientos posibles
"""

import pyshark
import sys
import time
from collections import OrderedDict

def descifrar_cesar(texto_cifrado, desplazamiento):
    """
    Descifra texto usando el algoritmo César
    """
    texto_descifrado = ""
    desplazamiento_efectivo = (-desplazamiento) % 26
    if desplazamiento_efectivo == 0:
        desplazamiento_efectivo = 26
    
    for caracter in texto_cifrado:
        if caracter.isalpha():
            base = ord('a')
            codigo = ord(caracter) - base
            nuevo_codigo = (codigo + desplazamiento_efectivo) % 26
            texto_descifrado += chr(base + nuevo_codigo)
        else:
            texto_descifrado += caracter
    
    return texto_descifrado

def extraer_datos_icmp(pcapng_file):
    """
    Extrae los datos de los paquetes ICMP del archivo pcapng
    """
    print(f"Leyendo archivo: {pcapng_file}")
    print("-" * 50)
    
    try:
        # Configurar la captura para leer solo ICMP Echo Request (tipo 8)
        cap = pyshark.FileCapture(pcapng_file, display_filter='icmp.type == 8')

        datos_icmp = []

        for pkt in cap:
            if hasattr(pkt, 'icmp'):
                # Extraer datos del ICMP (si existen)
                if hasattr(pkt.icmp, 'data'):
                    data_hex = pkt.icmp.data
                    # Convertir hex a texto
                    try:
                        data_texto = bytes.fromhex(data_hex.replace(':', '')).decode('utf-8', errors='ignore')
                        if data_texto.strip():  # Solo agregar si tiene contenido
                            datos_icmp.append(data_texto)
                            print(f"Paquete {len(datos_icmp)}: '{data_texto}' (hex: {data_hex})")
                    except:
                        continue

        cap.close()
        return ''.join(datos_icmp)

    except Exception as e:
        print(f"Error leyendo el archivo pcapng: {e}")
        return ""

def main():
    if len(sys.argv) == 2:
        pcapng_file = sys.argv[1]
    else:
        print("No se proporcionó archivo, usando 'paquetes_enviados_act2.pcapng' por defecto.")
        pcapng_file = "paquetes_enviados_act2.pcapng" #si se quiere leer otra captura cambiar acá
    
    # Extraer datos cifrados del archivo pcapng
    texto_cifrado = extraer_datos_icmp(pcapng_file)
    
    if not texto_cifrado:
        print("No se encontraron datos ICMP en el archivo")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(f"TEXTO CIFRADO EXTRAÍDO: '{texto_cifrado}'")
    print("="*60)
    print("\nPROBANDO TODOS LOS DESPLAZAMIENTOS:")
    print("-" * 40)
    
    # Probar todos los desplazamientos posibles (0-25)
    for desplazamiento in range(26):
        texto_descifrado = descifrar_cesar(texto_cifrado, desplazamiento)
        print(f"Desplazamiento {desplazamiento:2d}: {texto_descifrado}")
        # Mostrar el texto generado en cada desplazamiento en tiempo real
        time.sleep(0.3)
    
    print("-" * 40)
    print("NOTA: Revise manualmente cuál es el mensaje correcto")
    print("      (usualmente texto legible en español)")

if __name__ == "__main__":
    main()