class Circuit:

    id_counter = 0
    nodes = {}
    inputs = []
    queue = []

    def __init__(self):
        self.id = f'#{Circuit.id_counter}'
        Circuit.id_counter += 1
        Circuit.nodes[self.id] = self

    def simulate():
        Circuit.queue = [i for i in Circuit.inputs]
        for i in Circuit.queue:
            Circuit.nodes[i].update()

class Pin:

    pins = {}

    def __init__(self, id, name, type, canvas, x, y):
        self.id = id
        self.name = f'{self.id}_pin_{name}'
        self.type = type
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = 'x'
        self.connections = []
        Pin.pins[self.name] = self

    def add_connection(self, pin_id):
        self.connections.append(pin_id)

    def update(self):
        for i in self.connections:
            Pin.pins[i].state = self.state
            if Pin.pins[i].id not in Circuit.queue:
                Circuit.queue.append(Pin.pins[i].id)

    def create_pin(self):
        self.canvas.create_oval(self.x-4, self.y-4, self.x+4, self.y+4, outline='black', fill='black', tags=(self.id, 'pin', self.name))

    def move(self, x, y):
        self.x = x 
        self.y = y
        self.canvas.moveto(self.id, x, y)

class Figure:
    def __init__(self, id, canvas, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.canvas = canvas
        self.parts = []

    def create_figure(self):
        x, y = self.x, self.y
        for v in self.parts:
            k = v[0]
            if k == 'rect':
                x0, y0 = x+v[1], y+v[2]
                x1, y1 = x0+v[3], y0+v[4]
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='white', tags=self.id)
            elif k == 'oval':
                x0, y0 = x+v[1], y+v[1]
                x1, y1 = x0+v[3], y0+v[4]
                self.canvas.create_oval(x0, y0, x1, y1, outline='black', fill='white', tags=self.id)
            elif k == 'label':
                x0, y0 = x+v[1], y+v[2]
                self.canvas.create_text(x0, y0, text=v[4], tags=(self.id, f'{self.id}_label_{v[3]}'))
    
    def edit_label(self, label_id, text):
        self.canvas.itemconfigure(f'{self.id}_label_{label_id}', text=text)

    def move(self, x, y):
        self.x = x 
        self.y = y
        self.canvas.moveto(self.id, x, y)

class Element(Circuit):

    def __init__(self, canvas, x, y):
        super().__init__()
        self.figure = Figure(self.id, canvas, x, y)
        self.pins = {}

    def create_element(self):
        self.figure.create_figure()
        for v in self.pins.values():
            v.create_pin()

    def move(self, x, y):
        self.figure.move(x, y)
        for v in self.pins.values():
            v.move(x, y)

    def click(self):
        pass

    def update(self):
        for v in self.pins.values():
            v.update()

class Input(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.state = 0
        self.figure.parts = [
            ('rect', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'state', 0)
        ]
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+15, y+7.5)
        Circuit.inputs.append(self.id)

    def click(self):
        self.state ^= 1
        self.figure.edit_label('state', self.state)

    def update(self):
        self.pins['OUT'].state = self.state
        super().update()

class Output(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN'] = Pin(self.id, 'IN', 'IN', canvas, x, y+7.5)

        self.figure.parts = [
            ('oval', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'state', 'x'),
        ]
    
    def update(self):
        self.figure.edit_label('state', self.pins['IN'].state)

class AND(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, x, y+7)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, x, y+23)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+15, y+15)

        self.figure.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '&'),
        ]
    
    def update(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) & int(self.pins['IN2'].state)
        super().update()

class OR(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, x, y+7)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, x, y+23)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+15, y+15)

        self.figure.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '0'),
        ]
    
    def update(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) | int(self.pins['IN2'].state)
        super().update()

class XOR(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN1'] = Pin(self.id, 'IN1', 'IN', canvas, x, y+7)
        self.pins['IN2'] = Pin(self.id, 'IN2', 'IN', canvas, x, y+23)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+15, y+15)

        self.figure.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '='),
        ]
    
    def update(self):
        if self.pins['IN1'].state == 'x' or self.pins['IN2'].state == 'x':
            self.pins['OUT'].state = 0
        else:
            self.pins['OUT'].state = int(self.pins['IN1'].state) ^ int(self.pins['IN2'].state)
        super().update()

class NOT(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.pins['IN'] = Pin(self.id, 'IN', 'IN', canvas, x, y+7.5)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+15, y+7.5)

        self.figure.parts = [
            ('rect', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'name', '!'),
        ]
    
    def update(self):
        if self.pins['IN'].state == 'x':
            self.pins['OUT'].state = 0
            return
        
        self.pins['OUT'].state = not int(self.pins['IN'].state)
        super().update()

class Triger(Element):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.state = 0
        self.pins['D'] = Pin(self.id, 'D', 'IN', canvas, x, y+7)
        self.pins['C'] = Pin(self.id, 'C', 'IN', canvas, x, y+23)
        self.pins['OUT'] = Pin(self.id, 'OUT', 'OUT', canvas, x+30, y+15)

        self.figure.parts = [
            ('rect', 0, 0, 30, 30),
            ('label', 15, 15, 'name', 'D'),
        ]
    
    def update(self):
        if self.pins['C'].state == 1:
            self.state = self.pins['D'].state
        self.pins['OUT'].state = self.state
        super().update()