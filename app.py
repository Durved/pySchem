from tkinter import *
from node import Circuit, Pin, Input, Output, AND, OR, XOR, NOT, Triger

class App(Tk):
    
    elements = {'Вход': Input, 'Выход': Output, 'И': AND, 'ИЛИ': OR, 'Исключающее ИЛИ': XOR, 'НЕ': NOT, 'Триггер': Triger}

    def __init__(self):
        super().__init__()
        
        self.title('PySchem')

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        tools = ['Выделение', 'Палец', 'Провод']
        tools_var = Variable(value=tools)
        self.tool_box = Listbox(self, listvariable=tools_var, width=20, height=3)
        self.tool_box.grid(row=0, column=0, sticky=NS)
        self.tool_box.bind('<<ListboxSelect>>', self.select_tool)

        elements_var = Variable(value=list(self.elements.keys()))
        self.element_box = Listbox(self, listvariable=elements_var, width=20)
        self.element_box.grid(row=1, column=0, sticky=NS)
        self.element_box.bind('<<ListboxSelect>>', self.select_element_tool)

        self.blueprint = Canvas(self)
        self.blueprint.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        self.after(10, self.update_schem)
        

    def update_schem(self):
        Circuit.simulate()
        self.after(10, self.update_schem)

    def make_element(self, event, select):
        x, y = event.x, event.y
        new_element = self.elements[select](self.blueprint, x, y)
        new_element.create_element()

    def click_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        
        Circuit.nodes[group[0]].click()

    def select_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        x, y = event.x, event.y
        dx, dy = self.blueprint.coords(group[0])[0] - x, self.blueprint.coords(group[0])[1] - y
        self.blueprint.bind('<Motion>', lambda ev: self.move_element(ev, dx, dy))
        self.blueprint.bind('<ButtonRelease-1>', self.deselect)
        self.selected_element = Circuit.nodes[group[0]]

    def move_element(self, event, dx, dy):
        x, y = event.x, event.y
        self.selected_element.move(x+dx, y+dy)
        
    def deselect(self, event):
        self.selected_element = None
        self.blueprint.dtag('selected')
        self.blueprint.unbind('<Motion>')

    def delete_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        
        print(group)
        self.blueprint.delete(group[0])
        Circuit.nodes.pop(group[0])


    def wire_start(self, event):
        group = self.blueprint.gettags(CURRENT)
        if 'pin' not in group:
            return
        
        first_pin = group[2]
        self.blueprint.bind('<1>', lambda ev: self.wire_end(ev, first_pin))

    def wire_end(self, event, first_pin):
        group = self.blueprint.gettags(CURRENT)
        if 'pin' not in group:
            self.blueprint.bind('<1>', self.wire_start)
            return
        
        second_pin = group[2]
        if first_pin == second_pin:
            self.blueprint.bind('<1>', self.wire_start)
            return
        
        if Pin.pins[first_pin].type == Pin.pins[second_pin].type:
            self.blueprint.bind('<1>', self.wire_start)
            return
        
        if Pin.pins[first_pin].type == 'OUT':
            Pin.pins[first_pin].add_connection(second_pin)
        else:
            Pin.pins[second_pin].add_connection(first_pin)
        self.blueprint.create_line(Pin.pins[first_pin].x, Pin.pins[first_pin].y, Pin.pins[second_pin].x, Pin.pins[second_pin].y, tags=(Pin.pins[first_pin].id, Pin.pins[second_pin].id))

        self.blueprint.bind('<1>', self.wire_start)
            


    def select_tool(self, event):
        if len(self.tool_box.curselection()) == 0:
            return
        
        select = self.tool_box.get(self.tool_box.curselection()[0])
        self.blueprint.config(cursor='arrow')
        self.blueprint.unbind('<3>')
        if select == 'Выделение':
            self.blueprint.bind('<1>', self.select_element)
            self.blueprint.bind('<3>', self.delete_element)
        elif select == 'Палец':
            self.blueprint.bind('<1>', self.click_element)
            self.blueprint.config(cursor='hand2')
        elif select == 'Провод':
            self.blueprint.bind('<1>', self.wire_start)
            self.blueprint.bind('<3>', lambda: self.blueprint.bind('<1>', self.wire_start))
        else:
            self.blueprint.unbind('<1>')

    def select_element_tool(self, event):
        if len(self.element_box.curselection()) == 0:
            return
        
        select = self.element_box.get(self.element_box.curselection()[0])
        self.blueprint.config(cursor='arrow')

        if select in self.elements:
            self.blueprint.bind('<1>', lambda ev: self.make_element(ev, select))
        else:
            self.blueprint.unbind('<1>')
        

if __name__ == '__main__':
    App().mainloop()