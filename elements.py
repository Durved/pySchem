from circuit import Circuit, Pin

class Input(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.state = 0
        self.figure.parts = [
            ('rect', 0, 0, 20, 20),
            ('label', 10, 10, 'state', 0)
        ]
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 20, 10)
        Circuit.inputs.append(self.id)

    def click(self):
        self.state ^= 1
        self.figure.edit_label('state', self.state)

    def calc(self):
        self.pins['OUT'].state = self.state

class Output(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN'] = Pin(self.id, 'IN', 'IN', canvas, 0, 10)

        self.figure.parts = [
            ('oval', 0, 0, 20, 20),
            ('label', 10, 10, 'state', 'x'),
        ]
    
    def calc(self):
        self.figure.edit_label('state', self.pins['IN'].state)

class AND(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, 0, 10)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, 0, 30)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 20, 20)

        self.figure.parts = [
            ('rect', 0, 0, 20, 40),
            ('label', 10, 10, 'name', '&'),
        ]
    
    def calc(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) & int(self.pins['IN2'].state)

class OR(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, 0, 10)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, 0, 30)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 20, 20)

        self.figure.parts = [
            ('rect', 0, 0, 20, 40),
            ('label', 10, 10, 'name', '0'),
        ]
    
    def calc(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) | int(self.pins['IN2'].state)

class XOR(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, 0, 10)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, 0, 30)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 20, 20)

        self.figure.parts = [
            ('rect', 0, 0, 20, 40),
            ('label', 10, 10, 'name', '='),
        ]
    
    def calc(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) ^ int(self.pins['IN2'].state)

class NOT(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN'] = Pin(self.id, 'IN', 'IN', canvas, 0, 10)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 20, 10)

        self.figure.parts = [
            ('rect', 0, 0, 20, 20),
            ('label', 10, 10, 'name', '!'),
        ]
    
    def calc(self):
        if self.pins['IN'].state == 'x':
            self.pins['OUT'].state = 0
            return
        
        self.pins['OUT'].state = not int(self.pins['IN'].state)

class Triger(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.state = 0
        self.pins['D'] = Pin(self.id, 'D', 'IN', canvas, 0, 10)
        self.pins['C'] = Pin(self.id, 'C', 'IN', canvas, 0, 30)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, 40, 20)

        self.figure.parts = [
            ('rect', 0, 0, 40, 40),
            ('label', 20, 20, 'name', 'D'),
        ]
    
    def calc(self):
        if self.pins['C'].state == 1:
            self.state = self.pins['D'].state
        self.pins['OUT'].state = self.state