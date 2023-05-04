class GraphicalElement:
    id_counter = 0
    def __init__(self, canvas, x, y):
        self.id = f'#{GraphicalElement.id_counter}'
        GraphicalElement.id_counter += 1

        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        self.parts = []

    def create_element(self):
        x, y = self.x, self.y
        for v in self.parts:
            k = v[0]
            if k == 'rect':
                x0, y0 = x+v[1], y+v[2]
                x1, y1 = x0+v[3], y0+v[4]
                self.w = max(self.w, v[3])
                self.h = max(self.h, v[4])
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='white', tags=self.id)
            elif k == 'oval':
                x0, y0 = x+v[1], y+v[1]
                x1, y1 = x0+v[3], y0+v[4]
                self.w = max(self.w, v[3])
                self.h = max(self.h, v[4])
                self.canvas.create_oval(x0, y0, x1, y1, outline='black', fill='white', tags=self.id)
            elif k == 'label':
                x0, y0 = x+v[1], y+v[2]
                self.canvas.create_text(x0, y0, text=v[4], tags=(self.id, f'{self.id}_label_{v[3]}'))
            elif k == 'pin':
                x0, y0 = x+v[1], y+v[2]
                self.canvas.create_oval(x0-3, y0-3, x0+3, y0+3, outline='black', fill='black', tags=(self.id, 'pin', f'{self.id}_pin_{v[3]}'))

    def edit_label(self, label_id, text):
        self.canvas.itemconfigure(f'{self.id}_label_{label_id}', text=text)

    def move(self, x, y):
        self.x = x 
        self.y = y
        self.canvas.moveto(self.id, x-self.w/2, y-self.h/2)

class SchemElement(GraphicalElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs = {}
        self.outputs = {}

    def update(self):
        pass

    def click(self):
        pass

    def set_pin_value(self, pin, value):
        self.inputs[pin] = value

    def get_pin_value(self, pin):
        return self.outputs[pin]

class Input(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.outputs['OUT'] = 0

        self.parts = [
            ('rect', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'state', 0),
            ('pin', 15, 7.5, 'OUT')
        ]

    def click(self):
        self.outputs['OUT'] ^= 1
        self.edit_label('state', self.outputs['OUT'])

class Output(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs['IN'] = 'x'

        self.parts = [
            ('oval', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'state', 'x'),
            ('pin', 0, 7.5, 'IN')
        ]
    
    def update(self):
        self.edit_label('state', self.inputs['IN'])

class AND(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs['IN1'] = 'x'
        self.inputs['IN2'] = 'x'
        self.outputs['OUT'] = 'x'

        self.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '&'),
            ('pin', 0, 7, 'IN1'),
            ('pin', 0, 23, 'IN2'),
            ('pin', 15, 15, 'OUT'),
        ]
    
    def update(self):
        if self.inputs['IN1'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        if self.inputs['IN2'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        
        self.outputs['OUT'] = int(self.inputs['IN1']) & int(self.inputs['IN2'])

class OR(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs['IN1'] = 'x'
        self.inputs['IN2'] = 'x'
        self.outputs['OUT'] = 'x'

        self.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '0'),
            ('pin', 0, 7, 'IN1'),
            ('pin', 0, 23, 'IN2'),
            ('pin', 15, 15, 'OUT'),
        ]
    
    def update(self):
        if self.inputs['IN1'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        if self.inputs['IN2'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        
        self.outputs['OUT'] = int(self.inputs['IN1']) | int(self.inputs['IN2'])

class XOR(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs['IN1'] = 'x'
        self.inputs['IN2'] = 'x'
        self.outputs['OUT'] = 'x'

        self.parts = [
            ('rect', 0, 0, 15, 30),
            ('label', 7.5, 7.5, 'name', '=1'),
            ('pin', 0, 7, 'IN1'),
            ('pin', 0, 23, 'IN2'),
            ('pin', 15, 15, 'OUT'),
        ]
    
    def update(self):
        if self.inputs['IN1'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        if self.inputs['IN2'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        
        self.outputs['OUT'] = int(self.inputs['IN1']) ^ int(self.inputs['IN2'])

class NOT(SchemElement):

    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y)
        self.inputs['IN'] = 'x'
        self.outputs['OUT'] = 'x'

        self.parts = [
            ('rect', 0, 0, 15, 15),
            ('label', 7.5, 7.5, 'name', '!'),
            ('pin', 0, 7, 'IN'),
            ('pin', 15, 7, 'OUT'),
        ]
    
    def update(self):
        if self.inputs['IN'] == 'x':
            self.outputs['OUT'] = 'x'
            return
        
        self.outputs['OUT'] = not int(self.inputs['IN'])
