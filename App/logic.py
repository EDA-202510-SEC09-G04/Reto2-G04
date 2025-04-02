import random
from re import I
import time
import os
import csv
import sys
import pprint as pprint
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
        
        load_year =  int(row['load_time'][:4])
        collected_year = int(row['year_collection'])
        diferencia = load_year-collected_year
        
        row['diferencia'] = diferencia
        row["load_time"] = datetime.strptime(row["load_time"], "%Y-%m-%d %H:%M:%S")
        
        
        year = int(row['year_collection'])
        departamento = row['state_name']
        producto = row['commodity']
        categoria = row['statical_category']
        
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
        
        #GENERACION TABLA POR CATEGORIA ESTADISTICA -> AÑO 
        # Asegurar que el producto existe en la tabla, añadir con el mapa interno
        if not msc.contains(catalog['por_categoria'], categoria):
            tabla_interna = msc.new_map(155, 0.75)
            msc.put(catalog['por_categoria'], categoria, tabla_interna)
            
        # acceder a tabla interna de la categoria estadistica
        tabla_categoria = msc.get(catalog['por_categoria'], categoria)
        #verificar si hay una llave del año en tabla interna
        if not msc.contains(tabla_categoria, year): 
            #si no hay una llave con el año, agregar inicializado con una lista vacia para los registros
            msc.put(tabla_categoria, year, [])
            
        # Agregar el registro de categoria a la lista del año
        stats_registros_anio = msc.get(tabla_categoria, year)
        stats_registros_anio.append(row)
        msc.put(tabla_categoria, year, stats_registros_anio) 
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
    
    print('Iniciando ordenamiento tabla doble categoria - años')
    #SORT A PARTIR DE LOAD TIME DE LA DOBLE TABLA CATEGORIA AÑO
    for categoria in msc.key_set(catalog['por_categoria'])['elements']:
        tabla_categoria = msc.get(catalog['por_categoria'], categoria)
        
        for year in msc.key_set(tabla_categoria)['elements']:
            registros = msc.get(tabla_categoria, year) 
            sorted_records = lt.merge_sort(registros, 'load_time', descending=False, secondary_key='state_name')
            msc.put(tabla_categoria, year, sorted_records)  
    print('Ordenamiento completo\n')
    
    
    
    

    
    
    
    return catalog, tiempo_total, size, menor, mayor, primeros, ultimos

# Funciones de consulta sobre el catálogo


#catalogo = new_logic()
#load_data(catalogo)




def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_2(catalog,n,departamento):
    """
    Retorna el resultado del requerimiento 2
    """
    tiempo_inicial =  get_time()
    
    registros , tamanio_registros = ultimos_registros_dep(catalog,n,departamento)
    
    tiempo_final = get_time()
    
    dif_tiempo = delta_time(tiempo_inicial,tiempo_final)
    
    return dif_tiempo, tamanio_registros, registros



def ultimos_registros_dep(catalog,n,departamento):
    
   elementos =  catalog['por_departamento']['table']
   tamanio = lt.size(elementos)
   i = 0
   flag = True
   registros = None
   
   
   while i < tamanio and flag :
       
       
        el = elementos['elements'][i]
       
        if not slist.is_empty(el):
         
         primero = slist.first_element(el)
         
         if me.get_key(primero['info']) == departamento:
          
          valor = me.get_value(primero['info'])
          registros = valor[:n]
          #print(el)
          #print(valor)
          
          flag = False
          
        i += 1
          
    
    
   return registros , len(registros)
          
          
#print(req_2(catalogo,10,'ARKANSAS'))
        
#print(catalogo['por_departamento'])
           
           
           
           
def find(catalogo,filtro,filtro2, filtro3):
    
 elementos = catalogo['por_producto']
 
 
 productos = msc.get(elementos,filtro)
 filtrado_año = None
 survey_count = 0 
 census_count = 0 
 num_resultados= 0
 mapa = msc.new_map(100,0.75)
 resultado_lista =[]
 
 for i in range(filtro2,filtro3+1):
     
     
     filtrado_año =msc.get(productos,i)
     num_resultados += len(filtrado_año)
     
     for j in filtrado_año:
         
         if msc.contains(mapa,j['load_time']):
            msc.get(mapa,j['load_time']).append(j)
            if j['source'] =='SURVEY':
                survey_count += 1
            
            elif j['source'] =='CENSUS':
                
                census_count += 1
         else:
             lista = []
             msc.put(mapa,j['load_time'],lista)
             if j['source'] =='SURVEY':
                survey_count += 1
            
             elif j['source'] =='CENSUS':
                
                census_count += 1
     
     
 llaves = sorted(msc.key_set(mapa)['elements'])
 
 primeros_cinco = msc.get(mapa,llaves[0])[:5]
 ultimos_cinco = msc.get(mapa,llaves[-1])[-5:]
 
 resultados = primeros_cinco + ultimos_cinco
 
 for i in resultados:
     
     nuevo_dato ={}
     
     nuevo_dato['SOURCE'] = i['source']
     nuevo_dato['YEAR_COLLECTION'] = i['year_collection']
     nuevo_dato['LOAD_TIME'] = i['load_time']
     nuevo_dato['FREQ_COLLECTION'] = i['freq_collection']
     nuevo_dato['STATE_NAME'] = i['state_name']
     nuevo_dato['UNIT_MEASUREMENT'] = i['unit_measurement']
     
     resultado_lista.append(nuevo_dato)
     
 
 return resultado_lista , survey_count, census_count, num_resultados
         
    
             
 
 
                      



def req_1(catalog,anio):
    """
    Requerimiento 1:
    Identifica el último registro cargado a la plataforma para un año de recolección específico.
    """

    tiempo_inicial = get_time()

    # Obtener todos los registros (nativa)
    todos = msc.value_set(catalog['registros'])['elements']

    # Filtrar por año de recolección
    filtrados = [registro for registro in todos if int(registro['year_collection']) == anio]

    total = len(filtrados)

    if total == 0:
        tiempo_final = get_time()
        return [], 0, delta_time(tiempo_inicial, tiempo_final)

    # Ordenar por load_time descendente
    ordenados = lt.merge_recursive_sort(filtrados, key='load_time', descending=True)

    # Tomar solo el más reciente
    ultimo_registro = ordenados[0]

    tiempo_final = get_time()
    return [ultimo_registro], total, delta_time(tiempo_inicial, tiempo_final)


  






   


   



def req_3(catalog, departamento, inicial, final):
    """
    Retorna el resultado del requerimiento 3
    """
    tiempo_inicial =  get_time()
    
    inicial = int(inicial)
    final = int(final)
    registros = lt.new_list()
    
    census = 0
    survey = 0
    
    for i in range(inicial, final+1):
        tabla_registro = msc.get(catalog['por_anioydep'], departamento)
        registro_anio = msc.get(tabla_registro, i)
        
        if registro_anio: 
            for registro in registro_anio: 
                if registro['source'] == "CENSUS":
                    census += 1
                elif registro['source'] == "SURVEY":
                    survey += 1
            
                lt.add_last(registros, registro)
    #sort los registros finales por el load time
    
    reg_list = registros['elements']  #segundo key es incoherente
    sorted_list = lt.merge_sort(reg_list, 'load_time', descending=False, secondary_key='state_name')
    registros['elements'] = sorted_list
    
    size = registros['size']
        
    tiempo_final = get_time()
    
    dif_tiempo = delta_time(tiempo_inicial,tiempo_final)
    
    
    return dif_tiempo, size, census, survey, registros
    


def req_4(catalog,producto,año_inicial,año_final):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    
    tiempo_inicial = get_time()
    resultado, survey, census, num_results = find(catalog,producto,año_inicial,año_final)
    tiempo_final = get_time()
    
    delta_time = tiempo_final- tiempo_inicial
    return delta_time, resultado, survey, census , num_results






def req_5(catalog,producto,año_inicial,año_final):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass



def req_6(catalog, departamento, fecha_carga_inicial, fecha_carga_final):
    tiempo_inicial = get_time()
    
    registros = msc.get(catalog['por_departamento'], departamento)
    resultados = lt.new_list()
        
    fecha_carga_inicial = datetime.strptime(fecha_carga_inicial, "%Y-%m-%d")
    fecha_carga_final = datetime.strptime(fecha_carga_final, "%Y-%m-%d")
    
    survey = 0
    census = 0
    
    for i in registros:
        
        if fecha_carga_inicial <= i['load_time'] <= fecha_carga_final:
            lt.add_last(resultados, i)
            if i['source'] == "CENSUS":
                    census += 1
            elif i['source'] == "SURVEY":
                    survey += 1
            
    
    total_registros = resultados['size']
            
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    reg_list = resultados['elements']
    sorted_list = lt.merge_sort(reg_list, 'load_time', descending=False, secondary_key='state_name')
    resultados['elements'] = sorted_list
        
    return tiempo_total, total_registros, survey, census, resultados
            
        
    
    
    

    """ # Obtener todos los registros del mapa general
        todos = msc.value_set(catalog['registros'])

        # Convertir strings del usuario a objetos datetime.date
        inicial = datetime.strptime(fecha_carga_inicial.strip(), "%Y-%m-%d").date()
        final = datetime.strptime(fecha_carga_final.strip(), "%Y-%m-%d").date()

        census = 0
        survey = 0

        for i in range(lt.size(todos)):
            registro = lt.get_element(todos, i)

            # Validar que el estado coincida
            if registro['state_name'] != departamento:
                continue
            # Obtener y validar el campo 'load_time'
            load_time = registro.get('load_time')

            if isinstance(load_time, str):
                try:
                    load_time = datetime.strptime(load_time.strip(), "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

            if not isinstance(load_time, datetime):
                continue

            # Comparar solo por la fecha (sin hora)
            fecha_carga = load_time.date()
            if inicial <= fecha_carga <= final:
                lt.add_last(registros, registro)

                if registro.get('source') == "CENSUS":
                    census += 1
                elif registro.get('source') == "SURVEY":
                    survey += 1

        # Ordenar por 'load_time' descendente y desempatar con 'state_name' ascendente
        registros_nativos = registros['elements']
        mitad = len(registros_nativos) // 2

        registros_ordenados = lt.merge_recursive(
            registros_nativos[:mitad],
            registros_nativos[mitad:],
            key='load_time',
            descending=True,
            secondary_key='state_name'
        )

        registros['elements'] = registros_ordenados

        tiempo_final = get_time()
        tiempo_total = delta_time(tiempo_inicial, tiempo_final)
        size = lt.size(registros) """

    return tiempo_total, size, census, survey, registros





        
        

def req_7(catalog, departamento, inicial, final, ordenamiento):
    """
    Retorna el resultado del requerimiento 7
    """
    tiempo_inicial =  get_time()
    
    inicial = int(inicial)
    final = int(final)
    resultados = msc.new_map(55,0.75)
    
    min_anio = None
    max_anio = None
    min_valor = float('inf')
    max_valor = float('-inf')
    
    tabla_registro = msc.get(catalog['por_anioydep'], departamento)
    for i in range(inicial, final+1):
        registro_anio = msc.get(tabla_registro, i)
        
        if registro_anio: 
            census = 0
            survey = 0
            invalidos = 0
            valor = 0
            #Númeroderegistrosquecumplenelperiododelfiltrodelaño osea todso los q entren en el prox loop
            validos = 0
            for registro in registro_anio: 
            
                if registro['source'] == "CENSUS":
                    census += 1
                elif registro['source'] == "SURVEY":
                    survey += 1
                    
                if es_numero((registro['value'])) == True and '$' in registro['unit_measurement']: 
                    valor += float(registro['value'].replace(',', ''))
                    validos += 1
                    #print(registro)
                else:
                    invalidos += 1
               
                    
            #verificar si es menor o mayor
            if valor > max_valor:
                max_valor = valor
                max_anio = i
            if valor < min_valor:
                min_valor = valor
                min_anio = i
                    
            
        msc.put(resultados, i, {
            'anio':i,
            'census': census,
            'survey': survey,
            'validos': validos,
            'invalidos':invalidos,
            'valor': valor
        })
        
    #sort los registros finales por su valor ascendente o descendente
    #segundo parámetro de ordenamiento el número de registros que cumplen el periodo de año de manera descendente
    od = False
    if ordenamiento == 'DESCENDENTE':
        od = True
    reg_list = msc.value_set(resultados)
    
    sorted_list = lt.merge_sort(reg_list['elements'], 'valor', descending=od, secondary_key='validos')
    
    validos_total = resultados['size']
        
    tiempo_final = get_time()
    
    dif_tiempo = delta_time(tiempo_inicial,tiempo_final)
    
    return dif_tiempo, validos_total, sorted_list, min_anio, min_valor, max_anio, max_valor


def req_8(catalog, n, ordenamiento):
    """
    Retorna el resultado del requerimiento 8
    """
    tiempo_inicial =  get_time()
    
    departamentos = msc.key_set(catalog['por_departamento'])['elements']
    size = msc.key_set(catalog['por_departamento'])['size']
    
    
    resultados = lt.new_list()
    total_menor = float('inf')
    total_mayor = float('-inf')
    total_deps = size
    
    promedio_total = 0
        
    for dep in departamentos:
        dep_map = {}
        
        diferencias = 0
        elementos =  msc.get(catalog['por_departamento'], dep)
        nombre = dep
        registros = len(elementos)
        menor_anio = float('inf')
        mayor_anio = float('-inf')
        menor_tiempo = float('inf')
        mayor_tiempo = float('-inf')
        survey = 0
        census = 0
        
        for registro in elementos:
            if registro['source'] == "CENSUS":
                census += 1
            elif registro['source'] == "SURVEY":
                survey += 1
                    
            if int(registro['year_collection']) < menor_anio:
                menor_anio = int(registro['year_collection'])
                
            if int(registro['year_collection']) > mayor_anio:
                mayor_anio = int(registro['year_collection'])
                
            if registro['diferencia'] < menor_tiempo:
                menor_tiempo = registro['diferencia']
            
            if registro['diferencia'] > mayor_tiempo:
                mayor_tiempo = registro['diferencia']
                
                
            if int(registro['year_collection']) < total_menor:
                total_menor = int(registro['year_collection'])
                
            if int(registro['year_collection']) > total_mayor:
                total_mayor = int(registro['year_collection'])
                
            diferencias += registro['diferencia']
        
        promedio = diferencias/int(len(elementos))
        promedio_total += diferencias
        
        dep_map['nombre'] = nombre
        dep_map['promedio'] = promedio
        dep_map['registros'] = registros
        dep_map['menor_año'] = menor_anio
        dep_map['mayor_año'] = mayor_anio
        dep_map['menor_tiempo'] = menor_tiempo
        dep_map['mayor_tiempo'] = mayor_tiempo
        dep_map['survey'] = survey
        dep_map['census'] = census
        
        #añadir a lista de todos los deps
        lt.add_last(resultados, dep_map)
        
    #organizar lista de mapas segun ordenamiento
    od = False
    if ordenamiento == 'DESCENDENTE':
        od = True
        
    res_list = resultados['elements']
    sorted_list = lt.merge_sort(res_list, 'promedio', descending=od, secondary_key='nombre')        
    
    #falta arreglar este
    promedio_total = promedio_total/size
    
    tiempo_final = get_time()
    
    dif_tiempo = delta_time(tiempo_inicial,tiempo_final)
    
    res_final = sorted_list[:n]
    
    return dif_tiempo, total_deps, promedio_total, total_menor, total_mayor, res_final


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

def head_y_tail(registros):
    head = registros['elements'][:5]
    size = registros['size'] 
    tail = registros['elements'][size - 5:size]
    return head, tail

#ayuda a ver si un string es un numero
def es_numero(value):
    try:
        float(value.replace(',', ''))
        return True
    except ValueError:
        return False