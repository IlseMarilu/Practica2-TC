#Universidad Autónoma Metropolitana 
#Unidad:Lerma 
#Docente: Mario Alberto Ramírez Reyna
#UEA: Teoria de la informacion 
#Tema: Codigo del metodo SHANNON
#Elaboro: Ilse Marilu López Elías

from collections import Counter

def dividir_lista_frecuencias(frecuencias):
    # Ordenar las frecuencias de forma decreciente
    frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)
    
    # Variables para mantener el seguimiento de las sumas de frecuencias
    suma_superior = 0
    suma_inferior = 0
    
    # Partes superior e inferior iniciales
    parte_superior = dict()
    parte_inferior = dict()
    
    # Dividir las frecuencias de manera óptima
    for simbolo, frecuencia in frecuencias_ordenadas:
        if suma_superior <= suma_inferior:
            parte_superior[simbolo] = frecuencia
            suma_superior += frecuencia
        else:
            parte_inferior[simbolo] = frecuencia
            suma_inferior += frecuencia
    
    return parte_superior, parte_inferior

def asignar_codigos_binarios(frecuencias):
    # Caso base: si hay un solo símbolo, asignar el código binario '0'
    if len(frecuencias) == 1:
        simbolo, frecuencia = frecuencias.popitem()
        return {simbolo: '0'}
    """El caso base de la recursión se maneja cuando solo queda un símbolo en el diccionario
    de frecuencias. En ese caso, se extrae el único símbolo y su frecuencia utilizando
    popitem(), y se devuelve un diccionario que asigna ese símbolo al código binario '0'."""
    
    # Dividir la lista de frecuencias en dos partes aproximadamente iguales
    parte_superior, parte_inferior = dividir_lista_frecuencias(frecuencias)
    
    # Asignar códigos binarios a cada parte recursivamente
    codigos_superior = asignar_codigos_binarios(parte_superior)
    codigos_inferior = asignar_codigos_binarios(parte_inferior)
    
    # Agregar '0' al código de la parte superior y '1' al código de la parte inferior
    codigos_actualizados = {}
    for simbolo, codigo in codigos_superior.items():
        codigos_actualizados[simbolo] = '0' + codigo
    for simbolo, codigo in codigos_inferior.items():
        codigos_actualizados[simbolo] = '1' + codigo
    
    return codigos_actualizados


def convierteBytes(bits):
    byte = bytearray()
    for i in range(0, len(bits), 8):
        byte.append(int(bits[i:i + 8], 2))
    return bytes(byte) 

#Implementacion 
bits="".join(f"{n:08b}" for n in open(r'geminis.jpg',"rb").read())
#print(bits) 
#print(len (bits))

secuencia= [bits[i:i+16].zfill(16) for i in range(0, len(bits), 16)]
#print("\n\n",secuencia)
print("Numero bits originales:", len(secuencia*16))
frecuencias = Counter(secuencia)
parte_superior, parte_inferior = dividir_lista_frecuencias(frecuencias)
#print("\n\n", parte_superior)
#print ("\n\n", parte_inferior, "\n\n")

codigos = asignar_codigos_binarios(frecuencias)

"""# Imprimir las partes de la lista
print("Parte superior:")
for simbolo, frecuencia in parte_superior.items():
    print(f"El símbolo '{simbolo}' aparece {frecuencia} veces")
print(f"Suma total de frecuencias: {sum(parte_superior.values())}")

print("Parte inferior:")
for simbolo, frecuencia in parte_inferior.items():
    print(f"El símbolo '{simbolo}' aparece {frecuencia} veces")
print(f"Suma total de frecuencias: {sum(parte_inferior.values())}")"""


# Imprimir los códigos binarios
#for simbolo, codigo in codigos.items():
 #   print(f"El símbolo '{simbolo}' tiene el código binario '{codigo}'")

mensaje_codificado = "".join(codigos[simbolo] for simbolo in secuencia)
#print("\n\n",mensaje_codificado)

print("Numero de bits codificados:" ,len(mensaje_codificado))

#Convertir bits codificados a bytes
bytes_codificados = convierteBytes(mensaje_codificado)
#Guardar como .shannon 
with open('Codificados2.shannon', 'wb') as archivo:
    archivo.write(bytes_codificados)

#DECODIFICACION

# Invertir el diccionario de códigos
diccionario_invertido = {codigo: simbolo for simbolo, codigo in codigos.items()}
#print("\n\n", diccionario_invertido)

# Decodificar el mensaje codificado
mensaje_decodificado = ''
bits_actuales = ''
for bit in mensaje_codificado:
    bits_actuales += bit
    if bits_actuales in diccionario_invertido:
        simbolo = diccionario_invertido[bits_actuales]
        mensaje_decodificado += simbolo
        bits_actuales =''

#print("\n\n", mensaje_decodificado)
print("Numero de bits decodificados:", len(mensaje_decodificado))

# Convertir los bits codificados a bytes
bytes_decodificados = convierteBytes(mensaje_decodificado)

# Escribir los bytes decodificados en el archivo
with open('geminisShannon.jpg', 'wb') as archivo:
    archivo.write(bytes_decodificados)
