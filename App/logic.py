import random
import time
import os
import csv
import sys
import pprint
import uuid
from tabulate import tabulate
from datetime import datetime
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slist
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Utils import error as error

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

defualt_limit = 1000
sys.setrecursionlimit(defualt_limit*10)
csv.field_size_limit(2147483647)

def generate_unique_key():
    """Genera un UUID único para cada entrada"""
    return str(uuid.uuid4())

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def prueba_ordenamiento():
    lista = lt.new_list()

    lt.add_last(lista, {'load_time': '2018-01-01', 'state_name': 'A'})
    lt.add_last(lista, {'load_time': '2020-01-01', 'state_name': 'B'})
    lt.add_last(lista, {'load_time': '2019-01-01', 'state_name': 'C'})

    def criterio_fecha_desc(a, b):
        f1 = datetime.strptime(a['load_time'], "%Y-%m-%d")
        f2 = datetime.strptime(b['load_time'], "%Y-%m-%d")
        return f1 > f2  # más reciente primero

    print("\n🔽 Lista ANTES de ordenar:")
    for i in range(lt.size(lista)):
        print(lt.get_element(lista, i))

    lt.quick_sort(lista, criterio_fecha_desc)

    print("\n✅ Lista DESPUÉS de ordenar por load_time descendente:")
    for i in range(lt.size(lista)):
        print(lt.get_element(lista, i))









def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        'registros': msc.new_map(52428, 0.75),  
        'por_anio': msc.new_map(155, 0.75),  
        'por_departamento': msc.new_map(58, 0.75), 
        'por_anioydep': msc.new_map(58, 0.75), 
        'por_producto': msc.new_map(76, 0.75), 
        'por_categoria': msc.new_map(107, 0.75),
        #'tiempo_recoleccion': msc.new_map(997, 0.75)  
    }
    return catalog



# Funciones para la carga de datos

def load_data(catalog):
    """
    Carga los datos del reto
    """
    tiempo_inicial = get_time()
    files = data_dir + 'agricultural-20.csv'
    
    #GENERACION DE TABLA DE HASH GENERAL
    input_file = csv.DictReader(open(files, encoding='utf-8'))
    menor = float('inf')
    mayor = float('-inf')
    
    for row in input_file:
        row['unique_key'] = generate_unique_key()
        row["load_time"] = datetime.strptime(row["load_time"], "%Y-%m-%d %H:%M:%S")
        
        year = int(row['year_collection'])
        departamento = row['state_name']
        producto = row['commodity']
        
        menor = min(menor, year)
        mayor = max(mayor, year)
        
        msc.put(catalog['registros'], row['unique_key'], row)
        
        # GENERACION TABLA POR AÑO
        if not msc.contains(catalog['por_anio'], year):
            msc.put(catalog['por_anio'], year, [])

        #get la lista de registros asociada a la llave del año       
        year_list = msc.get(catalog['por_anio'], year)
        year_list.append(row)
        msc.put(catalog['por_anio'], year, year_list)
        
        #GENERACION TABLA POR DEPARTAMENTO
        if not msc.contains(catalog['por_departamento'], departamento):
            msc.put(catalog['por_departamento'], departamento, [])

        #get la lista de registros asociada a la llave del departamento y actualizarla con el registro nuevo
        dep_list = msc.get(catalog['por_departamento'], departamento)
        dep_list.append(row)
        msc.put(catalog['por_departamento'], departamento, dep_list)
        
        #GENERACION TABLA POR DEPARTAMENTO -> AÑO -> registros
        # Asegurar que el departamento existe en la tabla, añadir con el mapa interno
        if not msc.contains(catalog['por_anioydep'], departamento):
            tabla_interna = msc.new_map(155, 0.75)
            msc.put(catalog['por_anioydep'], departamento, tabla_interna)

        # acceder a tabla interna del departamento
        tabla_dep = msc.get(catalog['por_anioydep'], departamento)
        #verificar si hay una llave del año en tabla interna
        if not msc.contains(tabla_dep, year): 
            #si no hay una llave con el año, agregar inicializado con una lista vacia para los registros
            msc.put(tabla_dep, year, [])
            
        # Agregar el registro a la lista del año
        registros_anio = msc.get(tabla_dep, year)
        registros_anio.append(row)
        msc.put(tabla_dep, year, registros_anio) 
        
        #doble super tabla generada
        
        #GENERACION TABLA POR PRODUCTO -> AÑO 
        # Asegurar que el producto existe en la tabla, añadir con el mapa interno
        if not msc.contains(catalog['por_producto'], producto):
            tabla_interna = msc.new_map(155, 0.75)
            msc.put(catalog['por_producto'], producto, tabla_interna)
            
        # acceder a tabla interna del producto
        tabla_producto = msc.get(catalog['por_producto'], producto)
        #verificar si hay una llave del año en tabla interna
        if not msc.contains(tabla_producto, year): 
            #si no hay una llave con el año, agregar inicializado con una lista vacia para los registros
            msc.put(tabla_producto, year, [])
            
        # Agregar el registro de producto a la lista del año
        prod_registros_anio = msc.get(tabla_producto, year)
        prod_registros_anio.append(row)
        msc.put(tabla_producto, year, prod_registros_anio) 
        #doble  tabla generada
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    print('Carga de datos completa en :' + str(tiempo_total))
    print('\nIniciando ordenamiento tabla general')
    
    #SORT A PARTIR DEL LOAD TIME DE LA TABLA DE HASH GENERAL
    valores = msc.value_set(catalog['registros'])['elements']
    sorted_records = lt.merge_sort(valores, 'load_time', descending=True, secondary_key='state_name')
    size = catalog['registros']['size']
    primeros = sorted_records[:5]
    ultimos = sorted_records[-5:]
    
    print('Ordenamiento completo\n')
    
    print('Iniciando ordenamiento tabla de años')
    
    #SORT A PARTIR DE LOAD TIME LA TABLA DE AÑOS
    anio_llaves = msc.key_set(catalog['por_anio'])['elements']
    for year in anio_llaves:
        year_list = msc.get(catalog['por_anio'], year)
        sorted_list = lt.merge_sort(year_list, 'load_time', descending=False, secondary_key='state_name')

        msc.put(catalog['por_anio'], year, sorted_list)
    print('Ordenamiento completo\n')
    
    #SORT A PARTIR DE LOAD TIME LA TABLA DE DEPARTAMETOS
    #CUAL ES EL SEGNUDO PARAMETRO PARA EL SORT????? NO ESTA EN LA GUIA BROOO TT por ahora lo dejo como commodity
    print('Iniciando ordenamiento tabla departamentos')
    dep_llaves = msc.key_set(catalog['por_departamento'])['elements']
    for dep in dep_llaves:    
        dep_list = msc.get(catalog['por_departamento'], dep)
        sorted_list = lt.merge_sort(dep_list, 'load_time', descending=False, secondary_key='commodity')
        msc.put(catalog['por_departamento'], dep, sorted_list)
    print('Ordenamiento completo\n')
    
    print('Iniciando ordenamiento tabla doble departamento - años')
    
    #SORT A PARTIR DE LOAD TIME DE LA DOBLE TABLA DEPARTAMENTO AÑO
    for departamento in msc.key_set(catalog['por_anioydep'])['elements']:
        tabla_dep = msc.get(catalog['por_anioydep'], departamento)
        
        for year in msc.key_set(tabla_dep)['elements']:
            registros = msc.get(tabla_dep, year) #tampoco nos dice la guia el segundo criterio de ordenarmiento, en este caso el dep seria invalido
            sorted_records = lt.merge_sort(registros, 'load_time', descending=False, secondary_key='commodity')
            msc.put(tabla_dep, year, sorted_records)  
    print('Ordenamiento completo\n')
    
    print('Iniciando ordenamiento tabla doble producto - años')
    
    #SORT A PARTIR DE LOAD TIME DE LA DOBLE TABLA PRODUCTO AÑO
    for producto in msc.key_set(catalog['por_producto'])['elements']:
        tabla_prod = msc.get(catalog['por_producto'], producto)
        
        for year in msc.key_set(tabla_prod)['elements']:
            registros = msc.get(tabla_prod, year) 
            sorted_records = lt.merge_sort(registros, 'load_time', descending=False, secondary_key='state_name')
            msc.put(tabla_prod, year, sorted_records)  
    print('Ordenamiento completo\n')
    
    
    
    

    
    
    
    return catalog, tiempo_total, size, menor, mayor, primeros, ultimos

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

