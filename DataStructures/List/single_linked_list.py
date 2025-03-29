def new_list():
    newlist ={
        'first': None,
        'last': None,
        'size': 0,
    }
    return newlist


def get_element(my_list, pos):
    if pos < 0 or pos >= size(my_list): 
        raise IndexError('list index out of range')  
    
    node = my_list["first"]
    searchpos = 0
    
    while searchpos < pos:
        if node is None:
            raise IndexError('list index out of range')
        node = node["next"]
        searchpos += 1

    if node is None:
        raise IndexError('list index out of range')

    return node["info"]



def is_present(my_list,element, cmp_function): 
    is_in_array = False
    temp = my_list['first']
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp['info']) == 0:
            is_in_array = True
        else:
            temp = temp['next']
            count += 1
            
    if not is_in_array:
        count = -1
    return count
    
    
def size(my_list):
    return my_list['size']


def add_first(my_list, element):
    dict_element = {
        'info': element,
        'next': my_list['first'] 
    }

    my_list['first'] = dict_element 
    
    if my_list['last'] is None: 
        my_list['last'] = dict_element

    my_list['size'] += 1
    
    return my_list




def add_last(my_list,element):
    
    dict_element = {}
    dict_element['info'] = element
    dict_element['next'] = None
    
    if my_list['last'] == None:
        my_list['first'] = dict_element
        my_list['last'] = dict_element
    else:
        my_list['last']['next'] = dict_element
        my_list['last'] = dict_element
        
    my_list['size'] += 1
    return my_list

def first_element(my_list):
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['first']
    
def last_element(my_list):
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['last']
    
    
def is_empty(my_list):
    if my_list['size'] == 0:
        return True
    else:
        return False
    
def remove_first(my_list):
    if size(my_list) == 0:
        raise IndexError('list index out of range')
    
    node = my_list['first']
            
    if my_list['first']['next'] is None:
        my_list['first'] = None
        my_list['last'] = None
    else:
        my_list['first'] = my_list['first']['next']
        
    my_list['size'] -= 1
    return node['info']
        
        
def remove_last(my_list):
    if my_list['first'] is None:
        raise IndexError('list index out of range')
    
    temp = my_list['first']
    
    if temp['next'] is None:
        return remove_first(my_list)
    
    while temp['next']['next'] is not None:
        temp = temp['next']
        
    node = temp['next']
    temp['next'] = None
    my_list['last'] = temp
    my_list['size'] -= 1

    return node['info']

  
    
def insert_element(my_list,element,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    
    new_node = {
        'info': element,
        'next': None
    }
    if pos == 0:
        return add_first(my_list,element)
    elif pos == size(my_list):
        return add_last(my_list,element)
    else:
        temp = my_list['first']
        for i in range(pos - 1):
            temp = temp['next']

        new_node['next'] = temp['next']
        temp['next'] = new_node
        
    my_list['size'] += 1
    return my_list
    
def delete_element(my_list,pos):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
  
    if pos == 0:
        remove_first(my_list)
        return my_list
    elif pos == size(my_list) -1:
        remove_last(my_list)
        return my_list
    else:
        
        temp = my_list['first']
        for i in range(pos - 1):
            temp = temp['next']

        node = temp['next']
        temp['next'] = node['next']
        
    my_list['size'] -= 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    
    node = my_list["first"]
    for i in range(pos):
        node = node["next"]

    node["info"] = new_info 
    return my_list

def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 > my_list['size'] or
        pos_2 < 0 or pos_2 > my_list['size']):
        raise Exception('list index out of range')
    
    if pos_1 == pos_2:
        return my_list

    node_1 = get_element(my_list,pos_1)
    node_2 = get_element(my_list,pos_2)

    node_1['info'], node_2['info'] = node_2['info'], node_1['info']

    return my_list

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= size(my_list):
        raise Exception('IndexError: list index out of range')
    if pos_i + num_elements > size(my_list):
        raise Exception('IndexError: list index out of range')
    
    node_1 = get_element(my_list,pos_i)

    sublist ={
        'first': node_1,
        'last': None,
        'size': num_elements,
    }
    
    node_2 = get_element(my_list,num_elements)
    sublist['last'] = node_2
        
    return sublist