class Subject:
    def __init__(self):
        self.events = {}

    def register(self, event_name, event_handler):
        self.events.setdefault(event_name, [])
        if event_handler not in self.events[event_name]:
            self.events[event_name].append(event_handler)

    def unregister(self, event_name, event_handler):
        handlers = self.events.get(event_name, [])
        if event_handler in handlers:
            handlers.remove(event_handler)

    def notify(self, event_name, context=None):
        for event_handler in tuple(self.events.get(event_name, [])):
            event_handler(context=context)
        
