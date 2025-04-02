from pprint import pprint
import sys
from App import logic
from tabulate import tabulate

def new_logic():
    """
        Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("10- Probar ordenamiento quick_sort (de prueba)")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    catalog, tiempo_total, size, menor, mayor, primeros, ultimos= logic.load_data(control)
    return catalog, tiempo_total, size, menor, mayor, primeros, ultimos


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    print("\nRequerimiento 1: 10 registros más recientes por año de recolección")

    anio_input = input("Ingrese el año de recolección (por ejemplo, 2021): ")
    if not anio_input.isdigit():
        print("Año inválido. Debe ser un número entero.")
        return

    anio = int(anio_input)
    registros, size, dif_tiempo = logic.req_1(control, anio)

    print(f"\nTiempo de ejecución: {dif_tiempo:.6f} milisegundos")

    headers = ['year_collection', 'load_time', 'state_name', 'source', 'unit_measurement', 'value']

    if size == 0:
        print("No se encontraron registros para ese año.")
        return

    if size > 20:
        head, tail = logic.head_y_tail(registros)
        print("\nPrimeros 5 registros:")
        print(format_table(head['elements'], headers, max_col_width=12))

        print("\nÚltimos 5 registros:")
        print(format_table(tail['elements'], headers, max_col_width=12))
    else:
        print(format_table(registros['elements'], headers, max_col_width=12))

    print('Total registros encontrados: ' + str(size))





def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print(f'\nRequerimiento 2 : Listar los N últimos registros cargados dado un departamento de interés')
    n_input = int(input('Ingresa El número (N) de registros a listar (ej: 3, 5, 10 o 20): '))
    departamento_input = input('Ingresa Nombre del departamento a filtrar (ej.: “NEW MEXICO”, “CALIFORNIA” o “COLORADO”): ')
    
    dif_tiempo, registros,tamanio = logic.req_2(control,n_input,departamento_input)
    
    print(f'\nTiempo de ejecución {dif_tiempo}')
    headers = ['year_collection', 'load_time', 'state_name', 'source', 'unit_measurement', 'value']
    
    print(f'\n {n_input} registros:')
    print(format_table(registros,headers,max_col_width=12))
    print(f'Total de registros encontrados:{tamanio}')
    


def print_req_3(control, departamento, inicial, final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    dif_tiempo, size, census, survey, registros = logic.req_3(control, departamento, inicial, final)
    headers = ['source','year_collection','load_time','freq_collection','commodity','unit_measurement']
    print(f"\nTiempo de ejecución: {dif_tiempo:.6f} milisegundos")
    
    if size == 0:
        print('No se encontraron registros para esos parámetros. Intente de nuevo.')
    else:
        if size > 20:
            head, tail = logic.head_y_tail(registros)
            print("\nPrimeros 5 registros:")
            print(format_table(head,headers,max_col_width=12))

            print("\nÚltimos 5 registros:")
            print(format_table(tail,headers, max_col_width=12))
        else:
            print(format_table(registros, headers, max_col_width=12))
        print('Total registros encontrados: ' + str(size))
        print('Total registros encontrados con fuente census: ' + str(census))
        print('Total registros encontrados con fuente survey: ' + str(survey))
        
        
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    producto_input = input('Ingresar Tipo de producto a filtrar (ej.: “HOGS”, “SHEEP”, etc.):')
    año_inicial_input = int(input('Ingresar Año inicial del periodo a consultar (con formato "YYYY ", ej.: “2007”): '))
    año_final_input = int(input('Ingresar Año final del periodo a consultar (con formato "YYYY", ej.: “2010”): '))
    
    tiempo_eject,resultado,survey,census,num_results= logic.req_4(control,producto_input,año_inicial_input,año_final_input)
    headers = ['year_collection', 'load_time', 'state_name', 'source', 'unit_measurement', 'value']
    
    head, tail = logic.head_y_tail(resultado)
    print(f'\nTiempo de ejecución {tiempo_eject}')
    print('Primeros 5 datos:')
    print(format_table(head,headers,max_col_width=12))
    print('Ultimos 5 datos:')
    print(format_table(tail,headers,max_col_width=12))
    
    
    print(f'\n numero de elementos de origen "SURVEY": {survey}')
    print(f'\n numero de elementos de origen "CENSUS": {census}')
    print(f'\n numero de registros filtrados: {num_results}')


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    print("\nRequerimiento 6: Estadísticas por departamento en rango de fechas")
    print("Ingrese las fechas en formato 'YYYY-MM-DD' (por ejemplo, 2010-05-01)\n")

    departamento = input("Departamento: ").strip().upper()
    fecha_inicial = input("Fecha inicial (YYYY-MM-DD): ").strip()
    fecha_final = input("Fecha final (YYYY-MM-DD): ").strip()

    if len(fecha_inicial) != 10 or len(fecha_final) != 10:
        print("Formato de fecha inválido. Use el formato YYYY-MM-DD.")
        return

    tiempo, size, census, survey, registros = logic.req_6(control, departamento, fecha_inicial, fecha_final)

    headers = ['source', 'year_collection', 'load_time', 'freq_collection', 'state_name', 'unit_measurement', 'commodity']
    print(f"\nTiempo de ejecución: {tiempo:.6f} milisegundos")

    if size == 0:
        print("No se encontraron registros para ese rango de fechas y departamento.")
    else:
        if size > 20:
            head, tail = logic.head_y_tail(registros)
            print("\nPrimeros 5 registros:")
            print(format_table(head, headers, max_col_width=12, format_dates=True))

            print("\nÚltimos 5 registros:")
            print(format_table(tail, headers, max_col_width=12, format_dates=True))
        else:
            print(format_table(registros, headers, max_col_width=12, format_dates=True))

        print(f"\nTotal de registros: {size}")
        print(f"Registros tipo 'CENSUS': {census}")
        print(f"Registros tipo 'SURVEY': {survey}")


def print_req_7(control, departamento, inicial, final, ordenamiento):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    headers = ['anio','census','survey','validos','invalidos','valor']
    
    
    dif_tiempo, validos_total, sorted_list, min_anio, min_valor, max_anio, max_valor = logic.req_7(control, departamento, inicial, final, ordenamiento)
    if min_anio == max_anio:
        print('El menor y el mayor periodo de tiempo son el mismo.')
    print('Ordenamiento: ' + str(ordenamiento))
    
    if validos_total > 15:
        head, tail = logic.head_y_tail(sorted_list)
        print("\nPrimeros 5 registros:")
        print(format_table(head,headers,max_col_width=12))

        print("\nÚltimos 5 registros:")
        print(format_table(tail,headers, max_col_width=12))
    else:
        print(format_table(sorted_list, headers, max_col_width=12))
    
    print('Total registros encontrados: ' + str(validos_total))
    print('Periodo menor: ' + str(min_anio)) 
    print('Periodo mayor: ' + str(max_anio)) 
    print(f"\nTiempo de ejecución: {dif_tiempo:.6f} milisegundos")


def print_req_8(control, n, ordenamiento):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    dif_tiempo, total_deps, promedio_total, total_menor, total_mayor, res_final = logic.req_8(control, n, ordenamiento)
    print('Total departamentos: ' + str(total_deps))
    print('Año menor: ' + str(total_menor)) 
    print('Año mayor: ' + str(total_mayor)) 
    print('Promedio total: ' + str(promedio_total)) 
    print(f"\nTiempo de ejecución: {dif_tiempo:.6f} milisegundos")
    
    headers = ['nombre','promedio','registros','menor_año','mayor_año','menor_tiempo','mayor_tiempo','survey', 'census']
    print(format_table(res_final, headers, max_col_width=12))
    
    

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            headers = ['year_collection','load_time','state_name','source','unit_measurement','value']

            print("Cargando información de los archivos ....\n")
            catalog, tiempo_total, size, menor, mayor, primeros, ultimos= load_data(control)
            
            print(f"Total registros cargados: {size}")
            print(f"Tiempo de carga: {tiempo_total}")
            print(f"Menor año de recolección de registro: {menor}")
            print(f"Mayor año de recolección de registro: {mayor}")
            
            print("\nPrimeros 5 registros:")
            print(format_table(primeros,headers,max_col_width=12))

            print("\nÚltimos 5 registros:")
            print(format_table(ultimos,headers, max_col_width=12))
            
            
        elif int(inputs) == 10:
            logic.prueba_ordenamiento()
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            departamento = input('Ingrese el departamento que quiere consultar: ')
            inicial = int(input('Ingrese el año inicial de búsqueda: '))
            final = int(input('Ingrese el año final de búsqueda: '))
            print_req_3(control, departamento, inicial, final)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            departamento = input('Ingrese el departamento que quiere consultar: ')
            inicial = int(input('Ingrese el año inicial de búsqueda: '))
            final = int(input('Ingrese el año final de búsqueda: '))
            ordenamiento = (input('Ingrese el ordenamiento: '))
            print_req_7(control, departamento, inicial, final,ordenamiento)
            
            
        elif int(inputs) == 9:
            n = int(input('Ingrese el numero departamentos que quiere ver: '))
            ordenamiento = (input('Ingrese el ordenamiento: '))
            print_req_8(control, n, ordenamiento)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

def format_table(data, headers, max_col_width=15):
    """Funcion de formateo de la tabla"""
    formatted_data = [
        [str(row[col])[:max_col_width] + ("..." if len(str(row[col])) > max_col_width else "") for col in headers]
        for row in data
    ]

    return tabulate(formatted_data, headers=headers, tablefmt="grid")