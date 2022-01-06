import itertools
import collections
from team_companion.app.system.persistence_system import PersistenceSystem
from team_companion.app.web.modules.lock.models import Lock
from team_companion.app.common.exceptions import CouldNotBeLocked

class LockingSystem(PersistenceSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def class_model(self):
        return Lock

    @classmethod
    def system_name(cls):
        return "locking_system"

    def _attributes_to_synchronize(self):
        self.should_not_implement()

    def _create(self, form, **kwargs):
        self.should_not_implement()
    
    def _key_for(self, element):
        return str(element)

    def add(self, locker=None, locked=None, on_success=lambda persisted_object : None):
        return super().add(
            Lock(
                locker_class=locker.__class__.__name__,
                locker_identifier=self._key_for(locker),
                locked_class=locked.__class__.__name__,
                locked_identifier=self._key_for(locked)),
            on_success=on_success)

    def modify(self, object_to_update, updated_values, on_success=lambda persisted_object : None):
        self.should_not_implement()

    def add_using(self, form, **kwargs):
        self.should_not_implement()

    def modify_using(self, object_to_update, updated_form, **kwargs):
        self.should_not_implement()

    def _apply_on_each(self, one, delegated_attributes):
        base_attribute, trailing_attributes = delegated_attributes[0], delegated_attributes[1:]
        related_object = getattr(one, base_attribute)
        for trailing_attribute in trailing_attributes:
            if related_object is not None:
                related_object = getattr(related_object, trailing_attribute)
            else:
                raise CouldNotBeLocked(f"No se pudo bloquear todos los objetos de los que depende {one}.")
        if not isinstance(related_object, collections.abc.Iterable):
            related_object = [related_object]
        return related_object

    def _apply_on_all(self, objects, attribute_collection_path):
        delegated_attributes = attribute_collection_path.split('.')
        return list(itertools.chain.from_iterable([self._apply_on_each(one, delegated_attributes) for one in objects]))

    def lock(self, locker=None, locked_attributes=[]):
        assert locked_attributes
        for attribute in locked_attributes:
            attribute_collection_paths = attribute.split('->')
            locked_objects = [locker]
            for attribute_collection_path in attribute_collection_paths:
                locked_objects = self._apply_on_all(locked_objects, attribute_collection_path)
            for locked_object in locked_objects:
                self.add(locker=locker, locked=locked_object)

    def unlock(self, locker=None):
        self.assert_is_unlocked(locker)
        for each_lock in self.select_all_filter_by(
            locker_class=locker.__class__.__name__,
            locker_identifier=self._key_for(locker)):
                self.delete(each_lock)

    def is_locked(self, persisted_object):
        return not self.is_unlocked(persisted_object)

    def is_unlocked(self, persisted_object):
        return not self.select_one_filter_by(
            locked_class=persisted_object.__class__.__name__,
            locked_identifier=self._key_for(persisted_object),
            using='first')
    
    def assert_is_unlocked(self, persisted_object):
        try:
            assert self.is_unlocked(persisted_object)
        except AssertionError:
            raise AssertionError(f"{persisted_object} se encuentra en uso.")