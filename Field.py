class Field:
    def __init__(self, value=None):
        self.neighbours = []
        if value is None or value == 0:
            self.value = 0
            self.domain = list(range(1, 10))
        else:
            self.value = value
            self.domain = [value]

    def is_finalized(self):
        return self.value != 0

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.domain = [value]

    def get_domain(self):
        return self.domain

    def remove_from_domain(self, value):
        if value in self.domain:
            self.domain.remove(value)
            if len(self.domain) == 1:
                self.set_value(self.domain[0])
            return True
        return False

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def __str__(self):
        return "." if self.value == 0 else str(self.value)
