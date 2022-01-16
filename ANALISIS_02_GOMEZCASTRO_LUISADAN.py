import csv

# Importas la libreria pandas y accedes a ella con el identificador pd
import pandas as pd
import collections

# funcion principàl
def main():
   menu()

def menu():
    print("1. Rutas de Exportación más demandasdas")
    print("2. Rutas de Importación más demandadas")
    print("3. Medio de transporte más utilizado (Export/Import)")
    print("4. Valor por pais y categoria")
    
    respuesta = int(input("¿Que deseas consultar?"))
    
    
    if respuesta == 1:
        exportacion()
    elif respuesta == 2:
        importacion()
    elif respuesta == 3:
        print("Medios de Exportación mas usados")
        mediosexp()
        espacio(3)
        divisor()
        espacio(3)
        print("Medios de Importación mas usados")
        mediosimp()
        espacio(3)
    elif respuesta == 4:
        print("El costo por pais contemplando Importacion y Exportacion")
        costopais()
        
        espacio(3)
        divisor()
        espacio(3)
        valortotalexpo()
        divisor()
        valortotalimpo()
        divisor()
        valortotal()
    continuar()
        
def continuar():
    respuesta = int(input("¿Deseas continua? 1: Si - 2: No"))
    
    if respuesta == 1:
        menu()
    elif respuesta == 2:
        fin()
    else:
        print("Opcion invalida")
        continuar()
        
def fin():
    print("Gracias")
def espacio(x):
    for i in range(x):
        print("")


def divisor():
    print("-----------------------------------")
# convertir datos de csv a listas


def convertir():
    with open('synergy_logistics_database.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# obtener 10 rutas mas demandadas EXPORTACION


def exportacion():
    masdemandadas = []
    for rutas in convertir():
        if rutas[1] == "Exports":
            via = rutas[2]+"-"+rutas[3]
            masdemandadas.append(via)

    lista = pd.Series(masdemandadas)
    resultados = lista.value_counts().nlargest(10)
    return print(resultados)

# obtener 10 rutas mas demandadas IMPORTACION


def importacion():
    importdemandadas = []
    for rutas in convertir():
        if rutas[1] == "Imports":
            via = rutas[2]+"-"+rutas[3]
            importdemandadas.append(via)

    lista = pd.Series(importdemandadas)
    resultados = lista.value_counts().nlargest(10)
    return print(resultados)

# obtener el costo dependiendo el tipo(Expo/Impo) y  el tipo de medio
def costo_medio(tipo,medio):
    total = 0
    for rutas in convertir():
        if rutas[1] == tipo:
            if rutas[7] == medio:
                total = total + int(rutas[9])
    return total

# medios mas importantes Export y costo
def mediosexp():
    mediosexport = []
    for rutas in convertir():
        if rutas[1] == "Exports":
            medio = rutas[7]
            mediosexport.append(medio)
    c = collections.Counter(mediosexport).most_common(3)
    
    for datos in c:
        espacio(1)
        costo = costo_medio("Exports",datos[0])
        print("Medio: "+ str(datos[0])+"\nNumero de veces usado: "+str(datos[1])+"\nCosto Total: ${:,.2f}".format(costo))
        divisor()

# medios mas importantes Import y costo
def mediosimp():
    mediosimp = []
    for rutas in convertir():
        if rutas[1] == "Imports":
            medio = rutas[7]
            mediosimp.append(medio)
    c = collections.Counter(mediosimp).most_common(3)
    
    for datos in c:
        espacio(1)
        costo = costo_medio("Imports",datos[0])
        print("Medio: "+ str(datos[0])+"\nNumero de veces usado: "+str(datos[1])+"\nCosto Total: ${:,.2f}".format(costo))
        divisor()

def valortotalexpo():
    costo = []
    for rutas in convertir():
        if rutas[1] == "Exports":
            if rutas[9] == "total_value":
                continue
            else :
                costo.append(int(rutas[9]))
    costo = sum(costo)
    return print("El valor total de Exportacion es: ${:,.2f}".format(costo))


def valortotalimpo():
    costo = []
    for rutas in convertir():
        if rutas[1] == "Imports":
            if rutas[9] == "total_value":
                continue
            else :
                costo.append(int(rutas[9]))
    costo = sum(costo)
    return print("El valor total de Importacion es: ${:,.2f}".format(costo))

def valortotal():
    costo = []
    for rutas in convertir():
        if rutas[9] == "total_value":
            continue
        else :
            costo.append(int(rutas[9]))
    costo = sum(costo)
    return print("El valor total de Exportacion e importacion es: ${:,.2f}".format(costo))

    
def listapaises():
    paises = []
    for rutas in convertir():
            paises.append(rutas[2])
    return set(paises)
   
def costopais():
    from operator import itemgetter, attrgetter

    costopais = []
    total= 0
    for pais in listapaises():
        for rutas in convertir():
            if rutas[9] == "total_value":
                continue
            else :
                if pais == rutas[2]: 
                    total = total + int(rutas[9])
        costopais.append(pais+"-"+ str(total))
        total = 0
    ordenar = [] 
    for i in costopais:
        i = i.split("-")
        ordenar.append(i)
    ordenar = sorted(ordenar, key=itemgetter(1),reverse=True)
    for pais in ordenar:
        if pais[0] == "origin":
            continue
        else:
            
            costo = pais[1]
            print("El valor total de "+pais[0] +" es: ${:,.2f}".format(float(costo)))
main()