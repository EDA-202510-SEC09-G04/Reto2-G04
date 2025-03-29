from DataStructures.List import array_list as lt

def new_queue():
    new_queue = {
        'size': 0,
        'elements': []
    }
    return new_queue

def size(my_queue):
    return my_queue['size']
    
def is_empty(my_queue):
    if my_queue["size"] == 0 or my_queue["size"] == None:
        return True
    else:
        return False
    
     
def enqueue(my_queue, element):
    if my_queue['size'] == 0:
        my_queue['elements'] = [None] * (my_queue['size'] + 1) 
        my_queue['elements'][0] = element
    else:
        new_elements = [None] * (my_queue['size'] + 1) 
        
        for i in range(my_queue['size']):  
            new_elements[i] = my_queue['elements'][i]
        
        new_elements[my_queue['size']] = element  
        my_queue['elements'] = new_elements 
    
    my_queue['size'] += 1  #
    return my_queue

        

def dequeue(my_queue):
    if size(my_queue) == 0:
        raise Exception('IndexError: list index out of range')
    elif len(my_queue['elements']) == 1:
        elemento = my_queue['elements'][0]
        my_queue['elements'] = []
        my_queue['size'] = 0
        return elemento
    else:
        elemento = my_queue['elements'][0]
        for i in range(1, my_queue['size']):
            my_queue['elements'][i-1] = my_queue['elements'][i]
        my_queue['elements'][my_queue['size'] - 1] = None
        my_queue['size'] -= 1
        return elemento

def peek(my_queue):
    if size(my_queue) == 0:
        raise Exception('EmptyStructureError: queue is empty')
    return my_queue['elements'][0]
    