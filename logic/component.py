from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self):
        self.entity = None

    def attach(self, entity):
        self.entity = entity

    @abstractmethod
    def update(self):
        pass