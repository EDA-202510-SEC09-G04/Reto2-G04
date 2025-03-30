import random
import time
import os
import csv
import sys
import pprint
from tabulate import tabulate
from datetime import datetime
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slist
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Utils import error as error

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

defualt_limit = 1000
sys.setrecursionlimit(defualt_limit*10)
csv.field_size_limit(2147483647)

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
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    pass


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    pass

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

