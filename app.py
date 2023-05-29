from tkinter import *
from circuit import Circuit, Pin, Wire
from elements import Input, Output, AND, OR, XOR, NOT, Triger, Counter

class App(Tk):
    
    elements = {'Вход': Input, 'Выход': Output, 'И': AND, 'ИЛИ': OR, 'Исключающее ИЛИ': XOR, 'НЕ': NOT, 'Триггер': Triger, 'Счётчик': Counter}

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
        self.blueprint.tag_lower('wire')
        self.after(10, self.update_schem)
        
    def update_schem(self):
        Circuit.simulate()
        self.after(10, self.update_schem)



#############################################################
# Setup element
#############################################################

    def make_element(self, select):
        new_element = self.elements[select](self.blueprint, -100, -100)
        new_element.create_element()
        self.blueprint.bind('<Motion>', lambda ev: self.move_element(ev, -10, -10))
        self.blueprint.bind('<1>', self.deselect)
        self.selected_element = new_element



#############################################################
# Delete element
#############################################################

    def delete_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        
        Circuit.circuits[group[0]].delete()



##############################################################
# Use element
##############################################################

    def click_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        
        Circuit.circuits[group[0]].click()



##############################################################
# Drag and drop
##############################################################

    def select_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        x, y = event.x, event.y
        dx, dy = self.blueprint.coords(group[0])[0] - x, self.blueprint.coords(group[0])[1] - y
        self.blueprint.bind('<Motion>', lambda ev: self.move_element(ev, dx, dy))
        self.blueprint.bind('<ButtonRelease-1>', self.deselect)
        self.selected_element = Circuit.circuits[group[0]]

    def move_element(self, event, dx, dy):
        x, y = round((event.x+dx) / 10) * 10, round((event.y+dy) / 10) * 10
        self.selected_element.move(x, y)
        
    def deselect(self, event):
        self.selected_element = None
        self.blueprint.unbind('<Motion>')


##############################################################
# Wire tool
##############################################################

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
            if len(Pin.pins[second_pin].wires) > 0:
                self.blueprint.bind('<1>', self.wire_start)
                return
            Pin.pins[first_pin].add_connection(second_pin)
        else:
            if len(Pin.pins[first_pin].wires) > 0:
                self.blueprint.bind('<1>', self.wire_start)
                return
            Pin.pins[second_pin].add_connection(first_pin)

        new_wire = Wire(self.blueprint, first_pin, second_pin)
        new_wire.create_wire()
        Pin.pins[first_pin].wires.append(new_wire.id)
        Pin.pins[second_pin].wires.append(new_wire.id)

        self.blueprint.bind('<1>', self.wire_start)
            


####################################################################
# Tools/elements select
####################################################################

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
            self.make_element(select)
        else:
            self.blueprint.unbind('<1>')
        

if __name__ == '__main__':
    App().mainloop()