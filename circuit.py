import tkinter

class Circuit:

    id_counter = 0
    circuits = {}
    inputs = []
    queue = []

    def __init__(self, canvas, x, y):
        self.id = f'c{Circuit.id_counter}'
        Circuit.id_counter += 1
        Circuit.circuits[self.id] = self
        self.figure = Figure(self.id, canvas, x, y)
        self.pins = {}

    def create_element(self):
        self.figure.create_figure()
        for v in self.pins.values():
            v.create_pin()

    def delete(self):
        if self.id in Circuit.inputs:
            Circuit.inputs.remove(self.id)
        if self.id in Circuit.queue:
            Circuit.queue.remove(self.id)
        Circuit.circuits.pop(self.id)
        self.figure.canvas.delete(self.id)
        for v in self.pins.values():
            v.delete()


    def simulate():
        Circuit.queue = [i for i in Circuit.inputs]
        for i in Circuit.queue:
            Circuit.circuits[i].update()

    def move(self, x, y):
        self.figure.move(x, y)
        for v in self.pins.values():
            v.move(x, y)

    def click(self):
        pass

    def calc(self):
        pass

    def update(self):
        self.calc()
        for v in self.pins.values():
            v.update()

    
 

class Pin:

    pins = {}

    def __init__(self, id, name, type, canvas, x, y):
        self.id = id
        self.name = f'{self.id}p{name}'
        self.type = type
        self.canvas = canvas
        self.x = Circuit.circuits[id].figure.x + x
        self.y = Circuit.circuits[id].figure.y + y
        self.dx = x
        self.dy = y
        self.state = 'x'
        self.connections = []
        self.wires = []
        Pin.pins[self.name] = self

    def add_connection(self, pin_id):
        self.connections.append(pin_id)

    def update(self):
        for i in self.connections:
            if i not in Pin.pins:
                self.connections.remove(i)
                return
            Pin.pins[i].state = self.state
            if Pin.pins[i].id not in Circuit.queue:
                Circuit.queue.append(Pin.pins[i].id)

    def create_pin(self):
        self.canvas.create_oval(self.x-4, self.y-4, self.x+4, self.y+4, outline='black', fill='black', tags=(self.id, 'pin', self.name))

    def delete(self):
        for i in self.wires:
            Wire.wires[i].delete()
        Pin.pins.pop(self.name)

    def move(self, x, y):
        self.x = x + self.dx
        self.y = y + self.dy
        for i in self.wires:
            Wire.wires[i].move()
        self.canvas.moveto(self.id, x, y)


class Wire:

    id_counter = 0
    wires = {}

    def __init__(self, canvas, pin1_id, pin2_id):
        self.id = f'w{Wire.id_counter}'
        Wire.id_counter += 1
        Wire.wires[self.id] = self
        self.canvas:tkinter.Canvas = canvas
        self.pin1 = pin1_id
        self.pin2 = pin2_id
    
    def create_wire(self):
        x0, y0 = Pin.pins[self.pin1].x, Pin.pins[self.pin1].y
        x1, y1 = Pin.pins[self.pin2].x, Pin.pins[self.pin2].y
        self.canvas.create_line(x0, y0, x1, y1, tags=(self.id, 'wire'))

    def delete(self):
        Wire.wires.pop(self.id)
        self.canvas.delete(self.id)
        Pin.pins[self.pin1].wires.remove(self.id)
        Pin.pins[self.pin2].wires.remove(self.id)

    def move(self):
        self.canvas.coords(self.id, Pin.pins[self.pin1].x, Pin.pins[self.pin1].y, Pin.pins[self.pin2].x, Pin.pins[self.pin2].y)


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
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='white', tags=(self.id, 'circ'))
            elif k == 'oval':
                x0, y0 = x+v[1], y+v[1]
                x1, y1 = x0+v[3], y0+v[4]
                self.canvas.create_oval(x0, y0, x1, y1, outline='black', fill='white', tags=(self.id, 'circ'))
            elif k == 'label':
                x0, y0 = x+v[1], y+v[2]
                self.canvas.create_text(x0, y0, text=v[4], tags=(self.id, 'circ',  f'{self.id}_label_{v[3]}'))
    
    def edit_label(self, label_id, text):
        self.canvas.itemconfigure(f'{self.id}_label_{label_id}', text=text)

    def move(self, x, y):
        self.x = x 
        self.y = y
        self.canvas.moveto(self.id, x, y)

