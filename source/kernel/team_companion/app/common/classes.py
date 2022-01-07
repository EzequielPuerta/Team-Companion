is_concrete = lambda subclass: len(subclass.__subclasses__()) == 0

def all_concrete_subclasses(a_class):
    all_subclasses = []
    concrete_subclasses_aux(a_class, all_subclasses)
    return all_subclasses

def concrete_subclasses_aux(a_class, a_subclass_collection):
    for subclass in a_class.__subclasses__():
        a_subclass_collection.append(subclass) if is_concrete(subclass) else concrete_subclasses_aux(subclass, a_subclass_collection)