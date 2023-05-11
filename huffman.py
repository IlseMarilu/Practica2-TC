#Universidad Autónoma Metropolitana 
#Unidad:Lerma 
#Docente: Mario Alberto Ramírez Reyna
#UEA: Teoria de la informacion 
#Tema: Codigo del metodo HUFFMAN 
#Elaboro: Ilse Marilu López Elías 

import heapq
from collections import Counter
import os

#Se crean los parametros que se utilizaran para despues el arbol
class Tree:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq #frecuencia que se utiliza para el metodo
        self.left = left #nodo 
        self.right = right #nodo
  
    def __lt__(self, other):
        return self.freq < other.freq
    
def build_tree(text):#La cadena toma un texto como entrada 
        counter = Counter(text) #Se crea un objeto, cuneta la frecuencia de cada caracter en el texto
        pq = [Tree(ch, counter[ch]) for ch in counter]
        """Se crea una cola de prioridad (`pq`) de nodos `Tree`,
        donde cada nodo representa un carácter y su frecuencia"""
        heapq.heapify(pq)#La cola de prioridad luego se amontona usando la función `heapify()` del módulo `heapq`.
        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            parent = Tree(None, left.freq+right.freq, left,right)
            heapq.heappush(pq, parent)
        return heapq.heappop(pq)
"""Luego, la función ingresa en un bucle que continúa hasta que solo queda un nodo en la cola 
de prioridad. En cada iteración del bucle, los dos nodos con la menor frecuencia se extraen de
la cola de prioridad mediante la función `heappop()`. Estos dos nodos luego se combinan en un
nodo padre, donde la frecuencia del nodo padre es la suma de las frecuencias de sus dos hijos
Luego, el nodo principal se vuelve a agregar a la cola de prioridad mediante la función
`heappush()`.Una vez que se completa el bucle, solo queda un nodo en la cola de prioridad,
que es la raíz del árbol de Huffman. Este nodo raíz se extrae de la cola de prioridad mediante
la función `heappop()` y la función lo devuelve."""
    
def  build_map(root):
        def dfs(root, code, encoding_map):
            if root.ch:
                encoding_map[root.ch] = ''.join(code)
            else:
                code.append('0')
                dfs(root.left, code, encoding_map)
                code.pop()
                code.append('1')
                dfs(root.right, code, encoding_map)
                code.pop()
        encoding_map = {}
        dfs(root, [], encoding_map)
        return encoding_map

"""La función `build_map()` toma el nodo raíz de un árbol de Huffman como entrada y devuelve
un diccionario que asigna cada carácter del árbol a su código binario correspondiente.

La función primero inicializa un diccionario vacío `encoding_map`. Luego define una función
interna `dfs` (abreviatura de "búsqueda primero en profundidad") que realiza un recorrido
recurrente en profundidad del árbol de Huffman, comenzando en el nodo raíz. La función `dfs`
toma tres argumentos: el nodo actual que se visita (`root`), el código binario actual (`code`)
y el diccionario que asigna caracteres a códigos binarios (`encoding_map`).

Si el nodo actual es un nodo hoja (es decir, representa un carácter), la función agrega una
entrada a `encoding_map` que asigna el carácter al código binario actual. De lo contrario,
recursivamente se llama a sí mismo en el hijo izquierdo del nodo actual, agregando un '0' al
código binario actual antes de la llamada, y luego recursivamente se llama a sí mismo en el
hijo derecho del nodo actual, agregando un '1' al código binario actual antes de la llamada.

Finalmente, la función llama a `dfs` con el nodo raíz del árbol de Huffman, una lista de
códigos binarios vacía `[]` y un diccionario `encoding_map` vacío, y devuelve el
`encoding_map` resultante. Este diccionario se puede usar para codificar el texto original
usando la codificación Huffman."""    
def encode(text) :
        root = build_tree(text)
        encoding_map = build_map(root)
        return ''.join([encoding_map[ch] for ch in text]) 

"""La función `encode` toma una cadena `text` como entrada y devuelve la cadena binaria
codificada por Huffman.
Primero, la función llama a `build_tree` con la cadena de entrada para generar el árbol
de Huffman para la cadena. Luego, llama a `build_map` con el nodo raíz del árbol Huffman para
generar un diccionario que asigna cada carácter a su código Huffman correspondiente.

Finalmente, la función itera sobre cada carácter en la cadena de entrada y agrega su código
Huffman a la cadena binaria de salida buscando el código del carácter en el diccionario
`encoding_map`,la función devuelve la cadena binaria resultante."""  

def decode(encode, root ):
        if root.ch:
            return root.ch * len(encode)
        decoded = []
        node = root
        for bit in encode:
            if bit == "0":
                node = node.left
            else: 
                node = node.right
            if node.ch:
                decoded.append(node.ch)
                node = root
        return ''.join(decoded) 

"""La función `decode` toma dos entradas: una cadena binaria codificada por Huffman `encode`
y el nodo raíz del árbol Huffman `root`. La función devuelve la cadena decodificada
recorriendo el árbol de Huffman en función de la cadena binaria de entrada.
Primero, la función verifica si el nodo raíz del árbol de Huffman tiene un valor de carácter.
Si es así, significa que el árbol de Huffman solo tiene un nodo y la cadena binaria de entrada
solo contiene un solo carácter que debe repetirse `len (codificar)` veces. La función devuelve
esta cadena de caracteres multiplicada por la longitud de la cadena binaria de entrada.
De lo contrario, la función inicializa una lista vacía para almacenar los caracteres
decodificados y un 'nodo' variable para realizar un seguimiento del nodo actual que se visita
en el árbol de Huffman. La función itera sobre cada bit en la cadena binaria de entrada,
comenzando desde el primer bit.
Si el bit actual es `0`, la función se mueve al hijo izquierdo del nodo actual en el árbol
de Huffman. Si el bit actual es `1`, la función se mueve al hijo derecho del nodo actual.
Luego, la función verifica si el nuevo nodo actual tiene un valor de carácter. Si lo hace,
significa que la secuencia binaria actual corresponde a un carácter en el texto original. La
función agrega este carácter a la lista "decodificada" y restablece el nodo actual a la raíz
del árbol de Huffman.
Finalmente, la función devuelve la lista `decodificada` como una cadena concatenada."""

def convierteBytes(bits):
    byte = bytearray()
    for i in range(0, len(bits), 8):
        byte.append(int(bits[i:i + 8], 2))
    return bytes(byte)         

bits="".join(f"{n:08b}" for n in open(r'geminis.jpg',"rb").read())
#print(bits) 
#print(len (bits))

grupos = [bits[i:i+16].zfill(16) for i in range(0, len(bits), 16)]
num_grupos= len(grupos)
#print(num_grupos)
print("Numero de bits original", num_grupos*16, "bits")
#print(grupos)

text = grupos
#print("Original text:", text)

# Codificar
encoded_text = encode(text)
#print("Encoded text:", encoded_text)
print("Numero de bits texto codificado:", len(encoded_text), "bits")

#Convertir bits codificados a bytes
bytes_codificados = convierteBytes(encoded_text)
#Guardar como .huffman 
with open('Codificados.huff', 'wb') as archivo:
    archivo.write(bytes_codificados)

# Decodificar
decoded_text = decode(encoded_text, build_tree(text))
#print("Decoded text:", decoded_text)
print("Numero de bits texto decodificado:", len(decoded_text), "bits") 

# Convertir los bits decodificados a bytes
bytes_decodificados = convierteBytes(decoded_text)

# Escribir los bytes decodificados en el archivo
with open('GeminisHuffman.jpg', 'wb') as archivo:
    archivo.write(bytes_decodificados)

