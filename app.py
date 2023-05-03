from tkinter import *

class App(Tk):

    width = 15
    height = 30
    element_id = 0

    def __init__(self):
        super().__init__()
        
        self.title('PyShcem')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        tools = ['Выделение', 'Палец', 'Вход', 'Выход', 'Провод', 'И', 'ИЛИ', 'Исключающее ИЛИ']
        tools_var = Variable(value=tools)
        self.tool_box = Listbox(self, listvariable=tools_var, width=20)
        self.tool_box.grid(row=0, column=0, sticky=NS)
        self.tool_box.bind('<<ListboxSelect>>', self.selected_tool)


        self.blueprint = Canvas(self)
        self.blueprint.grid(row=0, column=1, sticky=NSEW)


    def make_input(self, event):
        x, y, w, h = event.x, event.y, self.width, self.width
        self.blueprint.create_rectangle(x, y, x+w, y+h, outline='black', fill='white', tags=f'elem{self.element_id}')
        self.blueprint.create_text(x+w/2, y+h/2, text='0', tags=f'elem{self.element_id}')
        self.blueprint.create_line(x+w, y+h/2, x+w+2, y+h/2, tags=f'elem{self.element_id}')
        self.element_id += 1

    def make_output(self, event):
        x, y, w, h = event.x, event.y, self.width, self.width
        self.blueprint.create_oval(x, y, x+w, y+h, outline='black', fill='white', tags=f'elem{self.element_id}')
        self.blueprint.create_text(x+w/2, y+h/2, text='x', tags=f'elem{self.element_id}')
        self.blueprint.create_line(x-2, y+h/2, x, y+h/2, tags=f'elem{self.element_id}')
        self.element_id += 1

    def make_AND(self, event):
        x, y, w, h = event.x, event.y, self.width, self.height
        self.blueprint.create_rectangle(x, y, x+w, y+h, outline='black', fill='white', tags=f'elem{self.element_id}')
        self.blueprint.create_text(x+w/2, y+h/2, text='&', tags=f'elem{self.element_id}')
        self.blueprint.create_line(x+w, y+h/2, x+w+2, y+h/2, tags=f'elem{self.element_id}')
        self.blueprint.create_line(x-5, y+h/4, x, y+h/4, tags=f'elem{self.element_id}')
        self.blueprint.create_line(x-5, y+h/4*3, x, y+h/4*3, tags=f'elem{self.element_id}')
        self.element_id += 1

    def select_element(self, event):
        self.blueprint.bind('<Motion>', self.move_element)
        self.blueprint.bind('<ButtonRelease-1>', self.deselect)

        group = self.blueprint.gettags(CURRENT)
        for i in group:
            self.blueprint.addtag_withtag('selected', i)

    def move_element(self, event):
        x, y, w, h = event.x, event.y, self.width, self.height
        self.blueprint.moveto('selected', x-w/2, y-h/2)
        
    def deselect(self, event):
        self.blueprint.dtag('selected')
        self.blueprint.unbind('<Motion>')

    def selected_tool(self, event):
        select_tool = self.tool_box.curselection()[0]
        if select_tool == 0:
            self.blueprint.bind('<1>', self.select_element)

        if select_tool == 1:
            self.blueprint.unbind('<1>')
            self.blueprint.config(cursor='hand2')
        else:
            self.blueprint.config(cursor='arrow')

        if select_tool == 2:
            self.blueprint.bind('<1>', self.make_input)

        if select_tool == 3:
            self.blueprint.bind('<1>', self.make_output)

        if select_tool == 5:
            self.blueprint.bind('<1>', self.make_AND)
        

if __name__ == '__main__':
    App().mainloop()