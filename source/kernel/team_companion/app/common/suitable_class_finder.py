from team_companion.app.common.classes import all_concrete_subclasses

class SuitableClassFinder():
    def __init__(self, abstract_class):
        self.abstract_class = abstract_class
        super().__init__()

    def suitable_for(self, *suitable_object, default_subclass=None, suitable_method='can_handle'):
        all_subclasses = all_concrete_subclasses(self.abstract_class)
        filtered_subclasses = [subclass for subclass in all_subclasses if (getattr(subclass, suitable_method)(*suitable_object))]
        if (len(filtered_subclasses) == 0) and (default_subclass is not None):
            return default_subclass
        elif (len(filtered_subclasses) == 1):
            return filtered_subclasses[0]
        elif (len(filtered_subclasses) > 1):
            raise ValueError(f"Many subclasses can handle the suitable object '{suitable_object}'")
        else:
            raise ValueError(f"No subclass can handle the suitable object '{suitable_object}'")