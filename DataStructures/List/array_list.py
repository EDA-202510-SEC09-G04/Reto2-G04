def new_list():
    newlist = {
        'elements': [],
        'size': 0,
    }
    return newlist


def get_element(my_list, pos):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][pos]

def is_present(my_list,element, cmp_function):
    size = len(my_list['elements'])
    if size > 0:
        keyexist = False
        for keypos in range(0,size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0 :
                keyexist = True
                break
        if  keyexist:
            return keypos
    return -1


def size(my_list):
    value = my_list['size']
    return value

def add_first(my_list,element):
    if len(my_list['elements']) == 0:
        my_list['elements'] = [None]
        
    if my_list['size'] >= len(my_list['elements']):
        capacidad = 2 * len(my_list['elements'])
        elements = [None] * capacidad
        for i in range(my_list['size']):
            elements[i + 1] = my_list['elements'][i]
        my_list['elements'] = elements
    else:
        for i in range(my_list['size'], 0, -1):
            my_list['elements'][i] = my_list['elements'][i - 1]
    my_list['elements'][0] = element
    my_list['size'] += 1

    return my_list

def add_last(my_list, element):
    if 'elements' not in my_list:
        my_list['elements'] = []
        my_list['size'] = 0
    
    my_list['elements'].append(element)
    my_list['size'] += 1

def first_element(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][0]

def last_element(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    return my_list[size(my_list)-1]

def get_element(my_list,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][pos]

def delete_element(my_list,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    elemento = my_list['elements'][pos]
    for i in range(pos, my_list['size'] - 1):
        my_list['elements'][i] = my_list['elements'][i + 1]
    
    my_list['elements'][my_list['size'] - 1] = None
    my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    elemento = my_list['elements'][0]
    for i in range(1, my_list['size']):
        my_list['elements'][i-1] = my_list['elements'][i]
    
    my_list['elements'][my_list['size'] - 1] = None
    my_list['size'] -= 1
    return elemento
    
def remove_last(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    
    elemento = my_list['elements'][my_list['size']-1]
    my_list['elements'][my_list['size']-1] = None
    my_list['size'] -= 1
    return elemento

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list['size']:
        raise IndexError('list index out of range')
    new = [None] * (my_list['size'] + 1)
    for i in range(pos):
        new[i] = my_list['elements'][i]

    new[pos] = element

    for i in range(pos, my_list['size']):
        new[i + 1] = my_list['elements'][i]

    my_list['elements'] = new
    my_list['size'] += 1

    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list['size'] or my_list['size'] == 0:
        raise IndexError('list index out of range')
    my_list['elements'][pos] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    temp = my_list['elements'][pos_1]
    my_list['elements'][pos_1] = my_list['elements'][pos_2]
    my_list['elements'][pos_2] = temp
    return my_list


def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list['size']:
        raise IndexError('list index out of range')
    if pos_i + num_elements > my_list['size']:
        raise IndexError('list index out of range')
    
    sublist = {
        'elements': my_list['elements'][pos_i:pos_i + num_elements],
        'size': num_elements
    }
    return sublist

def is_empty(my_list):
    if my_list["size"] == 0 or my_list["size"] == None:
        return True
    else:
        return False

def partition(my_list, lo, hi, sort_crit):
    pivot = get_element(my_list, hi)
    i = lo

    for j in range(lo, hi):
        if sort_crit(get_element(my_list, j), pivot):
            exchange(my_list, i, j)
            i += 1

    exchange(my_list, i, hi)
    return i

def shell_sort(my_list, sort_crit):
    if size(my_list) > 1:
        n = size(my_list)
        h = 1
        while h < n/2:  
            h = 2*h + 1
        while (h >= 1):
            for i in range(h, n):
                j = i
                while (j >= h) and sort_crit(
                                    get_element(my_list, j),
                                    get_element(my_list, j-h)):
                    exchange(my_list, j, j-h)
                    j -= h
            h //= 2   
    return my_list

def insertion_sort(my_list, sort_crit):

    if size(my_list) > 1:
        n = size(my_list)
        pos1 = 0
        while pos1 < n:
            pos2 = pos1
            while (pos2 > 0) and (sort_crit(
                get_element(my_list, pos2), get_element(my_list, pos2-1))):
                exchange(my_list, pos2, pos2-1)
                pos2 -= 1
            pos1 += 1
    return my_list

def quick_sort(my_list, sort_crit):

    quick_sort_recursive(my_list, 0, size(my_list)-1, sort_crit)
    return my_list

def quick_sort_recursive(my_list, lo, hi, sort_crit):
 
    if (lo >= hi):
        return
    pivot = partition(my_list, lo, hi, sort_crit)
    quick_sort_recursive(my_list, lo, pivot-1, sort_crit)
    quick_sort_recursive(my_list, pivot+1, hi, sort_crit)
    
def merge_sort(records, key, descending=True, secondary_key=None):
    if len(records) <= 1:
        return records

    mid = len(records) // 2
    left_half = merge_sort(records[:mid], key, descending, secondary_key)
    right_half = merge_sort(records[mid:], key, descending, secondary_key)

    return merge(left_half, right_half, key, descending, secondary_key)

def merge(left_half, right_half, key, descending, secondary_key):
    sorted_list = []
    i = j = 0

    while i < len(left_half) and j < len(right_half):
        left_value = left_half[i][key]
        right_value = right_half[j][key]

        if left_value > right_value if descending else left_value < right_value:
            sorted_list.append(left_half[i])
            i += 1
        elif left_value < right_value if descending else left_value > right_value:
            sorted_list.append(right_half[j])
            j += 1
        else:  # Empate en key -> comparar por secondary_key (ascendente)
            if secondary_key:
                if left_half[i][secondary_key] < right_half[j][secondary_key]:
                    sorted_list.append(left_half[i])
                    i += 1
                else:
                    sorted_list.append(right_half[j])
                    j += 1

    sorted_list.extend(left_half[i:])
    sorted_list.extend(right_half[j:])
    return sorted_list



def merge_recursive_sort(arr, key, descending=True, secondary_key=None):
    """
    Implementación recursiva de Merge Sort para listas nativas (list[dict]).
    Se ordena por 'key', con opción de 'descending', y un 'secondary_key' opcional
    para resolver empates.

    Parámetros:
    - arr: list[dict] → lista de diccionarios.
    - key: str → clave principal para ordenar.
    - descending: bool → True para orden descendente, False para ascendente.
    - secondary_key: str → clave secundaria opcional para desempates.

    Retorna:
    - list[dict] ordenada según los criterios dados.
    """

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_recursive_sort(arr[:mid], key, descending, secondary_key)
    right = merge_recursive_sort(arr[mid:], key, descending, secondary_key)

    return merge_recursive(left, right, key, descending, secondary_key)

def merge_recursive(left, right, key, descending, secondary_key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = left[i][key]
        right_val = right[j][key]

        if descending:
            if left_val > right_val:
                result.append(left[i])
                i += 1
            elif left_val < right_val:
                result.append(right[j])
                j += 1
            else:  # empate
                if secondary_key:
                    if left[i][secondary_key] > right[j][secondary_key]:
                        result.append(left[i])
                        i += 1
                    else:
                        result.append(right[j])
                        j += 1
                else:
                    result.append(left[i])
                    i += 1
        else:
            if left_val < right_val:
                result.append(left[i])
                i += 1
            elif left_val > right_val:
                result.append(right[j])
                j += 1
            else:
                if secondary_key:
                    if left[i][secondary_key] < right[j][secondary_key]:
                        result.append(left[i])
                        i += 1
                    else:
                        result.append(right[j])
                        j += 1
                else:
                    result.append(left[i])
                    i += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
