# -*- coding: utf-8 -*-

mi_variable = 12
MI_CONSTANTE = 25
print mi_variable
mi_cadena = "Hola mundo"
print mi_cadena
mi_cadena_multilinea = """Esta es una cadena
que contiene muchas líneas
también imprime acentos.
"""
print mi_cadena_multilinea

edad = 35
edad2 = 035
edad3 = 0x35
edad4 = 35.2

print edad
print edad2
print edad3
print edad4

verdadero = True
falso = False

print verdadero
print falso

suma = 10 + 5
resta = 10 - 5
negacion = -5
multiplicacion = 10 * 5
exponente = 10 ** 2
division = 10.3 / 2
division_entera = 10.3 // 2
modulo = 11 % 2

print suma
print resta
print negacion
print multiplicacion
print exponente
print division
print division_entera
print modulo

#comentario de una sola línea
"""Este es un
comentario de varias líneas"""

#Tuplas: son variables que pueden guardar varios
#tipos de datos que no pueden ser modificados.

tupla_ejemplo = ('uno', 'dos', 3, 128, "tupla", 24)

print tupla_ejemplo[2]

print tupla_ejemplo[2:5]
print tupla_ejemplo[:4]
print tupla_ejemplo[2:]

print tupla_ejemplo[-1]
print tupla_ejemplo[-4:]

#Listas, permiten guardar nuevos valores

mi_lista = ['cadena de texto', 15, 2.8, 'otro dato', 25]

print mi_lista[2]
mi_lista[2] = 20
print mi_lista[2]
print mi_lista[1:4]
print mi_lista[-2]

mi_lista.append('dato final')
print mi_lista

#Diccionario
