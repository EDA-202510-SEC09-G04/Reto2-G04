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
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


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
    # TODO: Imprimir el resultado del requerimiento 4
    pass


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
    pass


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


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

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
            print_req_8(control)

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