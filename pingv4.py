#!/usr/bin/env python3
"""
Envío de caracteres mediante paquetes ICMP
Cada carácter se envía en el campo data de un paquete ICMP request separado
"""

import socket
import struct
import time
import sys
import os

# Importar las funciones de cifrado desde cesar.py
from cesar import cifrar_cesar, descifrar_cesar

def calcular_checksum(data):
    checksum = 0
    
    # Asegurar que data tenga longitud par
    if len(data) % 2 == 1:
        data += b'\x00'
    
    # Sumar cada par de bytes
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
    
    # Manejar carry
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    
    # Complemento a uno
    checksum = ~checksum & 0xFFFF
    
    return checksum

def crear_paquete_icmp(id_paquete, secuencia, data):
    # Tipo ICMP (8 = Echo Request), Código (0), Checksum (temporal), ID, Secuencia
    tipo = 8
    codigo = 0
    checksum = 0
    
    # Crear header ICMP temporal (sin checksum)
    header = struct.pack('!BBHHH', tipo, codigo, checksum, id_paquete, secuencia)
    
    # Crear el paquete completo temporal
    paquete_temporal = header + data.encode('utf-8')
    
    # Calcular checksum real
    checksum_real = calcular_checksum(paquete_temporal)
    
    # Crear header final con checksum correcto
    header_final = struct.pack('!BBHHH', tipo, codigo, checksum_real, id_paquete, secuencia)
    
    # Paquete ICMP final
    paquete_icmp = header_final + data.encode('utf-8')
    
    return paquete_icmp

def enviar_caracteres_icmp(texto, destino, delay=0.5):
    try:
        # Crear socket raw (requiere privilegios de administrador)
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(5)
        
        print(f"Enviando '{texto}' a {destino}")
        print(f"Total de caracteres: {len(texto)}")
        print("-" * 50)
        
        id_paquete = os.getpid() & 0xFFFF  # ID del proceso como identificador
        
        for i, caracter in enumerate(texto):
            # Crear y enviar paquete ICMP
            paquete = crear_paquete_icmp(id_paquete, i + 1, caracter)
            
            try:
                sock.sendto(paquete, (destino, 0))
                print(f"Paquete {i+1:2d}: '{caracter}' enviado")
                
                # Pequeña pausa entre envíos
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error enviando carácter '{caracter}': {e}")
        
        print("-" * 50)
        print("Envío completado")
        
    except PermissionError:
        print("Error: Se requieren privilegios de administrador para crear sockets raw")
        print("Ejecuta el script con sudo: sudo python3 pingv4.py")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if 'sock' in locals():
            sock.close()

def main():
    """
    Función principal
    """
    print("=== ENVÍO DE CARACTERES VÍA ICMP ===")
    print()
    
    # Preguntar si desea cifrar el texto
    usar_cifrado = input("¿Desea cifrar el texto antes de enviarlo? (s/n): ").lower().strip()
    
    if usar_cifrado.startswith('s'):
        # Cifrar texto
        print("\n=== CIFRADO CÉSAR ===")
        texto_original = input("Ingrese el texto a cifrar: ")
        desplazamiento = int(input("Ingrese el desplazamiento: "))
        
        texto_a_enviar = cifrar_cesar(texto_original, desplazamiento)
        print(f"Texto cifrado: {texto_a_enviar}")
        print(f"Se enviará el texto cifrado: '{texto_a_enviar}'")
    else:
        # Usar texto sin cifrar
        texto_a_enviar = input("Ingrese el texto a enviar: ")
    
    print()
    
    # Destino
    destino = input("Ingrese la dirección IP destino (por defecto 8.8.8.8): ").strip()
    if not destino:
        destino = "8.8.8.8"
    
    # Delay entre paquetes
    try:
        delay = float(input("Delay entre paquetes en segundos (por defecto 0.5): ") or "0.5")
    except ValueError:
        delay = 0.5
    
    print()
    print("Iniciando envío...")
    print()
    
    # Enviar caracteres
    enviar_caracteres_icmp(texto_a_enviar, destino, delay)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario")
    except Exception as e:
        print(f"Error inesperado: {e}")
