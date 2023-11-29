from domain.model.base_object import BaseObject


class AntennaModule(BaseObject):

    def __init__(self, address, *, attributes):
        super().__init__(address)
        self.antenna_specific_attributes = attributes

    def set_dimensions(self, *args):
        pass
