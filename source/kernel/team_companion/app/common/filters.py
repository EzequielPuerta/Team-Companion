def formatted_boolean(boolean_value):
    return 'Sí' if boolean_value else 'No'

def formatted_list(list_value, separator):
    return separator.join(list(map(lambda element: str(element), list_value)))