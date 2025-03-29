from DataStructures.List import array_list as lt



def new_stack():
     
   new = {
        'size': 0,
        'First':None,
        'Last':None
   }
     
   return new


# Push añade un nuevo elemento a la lista


def push(my_stack,element):
     
     dict_element = {
          'info':element,
          'next':my_stack['First']
     }
     
   
     
     my_stack['First'] = dict_element
     
     if my_stack['size'] == 0:
          
          my_stack['Last'] = dict_element
     
     my_stack['size'] += 1
     
     return my_stack






def pop(my_stack):
     
    if my_stack['First'] == None:
        raise Exception('EmptyStructureError: stack is empty')
    
    ultimo_el = my_stack['First']['info']
    my_stack['First'] = my_stack['First']['next']
    my_stack['size'] -= 1
    
    return ultimo_el


def is_empty(my_stack):
     
     
     if my_stack['First'] == None:
          
          return True
     
     else:
          
          return False



def top(my_stack):
     
     if my_stack['First'] == None:
          
          raise Exception('EmptyStructureError: stack is empty')
     else:
          
      return my_stack['First']['info']


def size(my_stack):
     
     return my_stack['size']




