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

        #get la lista de registros asociada a la llave del departamento       
        dep_list = msc.get(catalog['por_departamento'], departamento)
        dep_list.append(row)
        msc.put(catalog['por_departamento'], departamento, dep_list)
        
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    
    #SORT A PARTIR DEL LOAD TIME DE LA TABLA DE HASH GENERAL
    valores = msc.value_set(catalog['registros'])['elements']
    sorted_records = lt.merge_sort(valores, 'load_time', descending=True, secondary_key='state_name')
    size = catalog['registros']['size']
    
    #SORT A PARTIR DE LOAD TIME LA TABLA DE AÑOS
    anio_llaves = msc.key_set(catalog['por_anio'])['elements']
    for year in anio_llaves:
        year_list = msc.get(catalog['por_anio'], year)
        sorted_list = lt.merge_sort(year_list, 'load_time', descending=False, secondary_key='state_name')

        msc.put(catalog['por_anio'], year, sorted_list)
    
    #SORT A PARTIR DE LOAD TIME LA TABLA DE DEPARTAMETOS
    #CUAL ES EL SEGNUDO PARAMETRO PARA EL SORT????? NO ESTA EN LA GUIA BROOO TT por ahora lo dejo como commodity

    dep_llaves = msc.key_set(catalog['por_departamento'])['elements']
    for dep in dep_llaves:    
        dep_list = msc.get(catalog['por_departamento'], dep)
        sorted_list = lt.merge_sort(dep_list, 'load_time', descending=False, secondary_key='commodity')
        msc.put(catalog['por_departamento'], dep, sorted_list)
    
    
    primeros = sorted_records[:5]
    ultimos = sorted_records[-5:]

    
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

