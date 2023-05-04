from tkinter import *
from elements import Input, Output, AND, OR, XOR, NOT

class App(Tk):
    
    wires = []
    first_el = None
    schem = {}
    selected_tool = "Выделение"
    elements = {'Вход': Input, 'Выход': Output, 'И': AND, 'ИЛИ': OR, 'Исключающее ИЛИ': XOR, 'НЕ': NOT}


    def __init__(self):
        super().__init__()
        
        self.title('PySchem')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        tools = ['Выделение', 'Палец', 'Вход', 'Выход', 'Провод', 'И', 'ИЛИ', 'Исключающее ИЛИ', 'НЕ']
        tools_var = Variable(value=tools)
        self.tool_box = Listbox(self, listvariable=tools_var, width=20)
        self.tool_box.grid(row=0, column=0, sticky=NS)
        self.tool_box.bind('<<ListboxSelect>>', self.select_tool)

        self.blueprint = Canvas(self)
        self.blueprint.grid(row=0, column=1, sticky=NSEW)
        self.after(10, self.update_schem)
        

    def update_schem(self):
        for i in self.wires:
            self.schem[i[1][0]].set_pin_value(i[1][1], self.schem[i[0][0]].get_pin_value(i[0][1]))
            self.schem[i[1][0]].update()
            self.schem[i[0][0]].update()
        self.after(10, self.update_schem)


    def make_element(self, event):
        x, y = event.x, event.y
        new_element = self.elements[self.selected_tool](self.blueprint, x, y)
        self.schem[new_element.id] = new_element
        new_element.create_element()


    def click_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        
        self.schem[group[0]].click()


    def select_element(self, event):
        group = self.blueprint.gettags(CURRENT)
        if len(group) == 0:
            return
        self.blueprint.bind('<Motion>', self.move_element)
        self.blueprint.bind('<ButtonRelease-1>', self.deselect)
        self.selected_element = self.schem[group[0]]

    def move_element(self, event):
        x, y = event.x, event.y
        self.selected_element.move(x, y)
        
    def deselect(self, event):
        self.blueprint.dtag('selected')
        self.blueprint.unbind('<Motion>')

    def wire_start(self, event):
        group = self.blueprint.gettags(CURRENT)

        if 'pin' not in group:
            return
        
        self.first_el = (group[0], group[2].split('_')[-1])
        self.blueprint.bind('<1>', self.wire_end)

    def wire_end(self, event):
        group = self.blueprint.gettags(CURRENT)

        if 'pin' not in group:
            return
        if group[0] == self.first_el[0]:
            self.blueprint.bind('<1>', self.wire_start)
            return
        second_el = (group[0], group[2].split('_')[-1])
        if self.first_el[1] in self.schem[self.first_el[0]].outputs:
            if second_el[1] in self.schem[second_el[0]].inputs:
                if (self.first_el, second_el) not in self.wires:
                    self.wires.append((self.first_el, second_el))
            else:
                self.blueprint.bind('<1>', self.wire_start)
                return
        else:
            if second_el[1] in self.schem[second_el[0]].outputs:
                if (second_el, self.first_el) not in self.wires:
                    self.wires.append((second_el, self.first_el))
            else:
                self.blueprint.bind('<1>', self.wire_start)
                return
        print(self.wires)
        self.blueprint.bind('<1>', self.wire_start)

    def select_tool(self, event):
        select_tool = self.tool_box.get(self.tool_box.curselection()[0])
        if select_tool in self.elements:
            self.selected_tool = select_tool
            self.blueprint.bind('<1>', self.make_element)
            self.blueprint.config(cursor='arrow')
        elif select_tool == 'Выделение':
            self.blueprint.bind('<1>', self.select_element)
            self.blueprint.config(cursor='arrow')
        elif select_tool == 'Палец':
            self.blueprint.bind('<1>', self.click_element)
            self.blueprint.config(cursor='hand2')
        elif select_tool == 'Провод':
            self.blueprint.bind('<1>', self.wire_start)
            self.blueprint.config(cursor='arrow')
        else:
            self.blueprint.unbind('<1>')
            self.blueprint.config(cursor='arrow')
        

if __name__ == '__main__':
    App().mainloop()