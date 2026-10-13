class Entity:
    def __init__(self):
        self._components = {}

    def add_component(self, component_cls, component):
        component.attach(self)
        self._components[component_cls] = component

    def get_component(self, component_cls):
        return self._components.get(component_cls)

    def update(self):
        for component in self._components.values():
            component.update()