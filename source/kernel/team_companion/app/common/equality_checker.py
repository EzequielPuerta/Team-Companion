def equality_checker(myself, other):
    return (type(myself) == type(other)) and \
        ((myself.id is not None and (myself.id == other.id)) or (hash(myself) == hash(other)))