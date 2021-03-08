import os

os.system('color')

class BRAILLE_LINE:
    F_SLOPE_0 = '⠤'

class CUIPY_COLOR:
    _RESET = '\u001b[0m'
    RED = '\u001b[31m'
    BLACK = '\u001b[30m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'

    GREY = '\u001b[30;1m'
    GRAY = '\u001b[30;1m'
    B_RED = '\u001b[31;1m'
    B_GREEN = '\u001b[32;1m'
    B_YELLOW = '\u001b[33;1m'
    B_BLUE = '\u001b[34;1m'
    B_MAGENTA = '\u001b[35;1m'
    B_CYAN = '\u001b[36;1m'
    B_WHITE = '\u001b[37;1m'

    BG_BLACK = '\u001b[40m'
    BG_RED = '\u001b[41m'
    BG_GREEN = '\u001b[42m'
    BG_YELLOW = '\u001b[43m'
    BG_BLUE = '\u001b[44m'
    BG_MAGENTA = '\u001b[45m'
    BG_CYAN = '\u001b[46m'
    BG_WHITE = '\u001b[47m'

    BG_GREY = '\u001b[40;1m'
    BG_GRAY = '\u001b[40;1m'
    BG_B_RED = '\u001b[41;1m'
    BG_B_GREEN = '\u001b[42;1m'
    BG_B_YELLOW = '\u001b[43;1m'
    BG_B_BLUE = '\u001b[44;1m'
    BG_B_MAGENTA = '\u001b[45;1m'
    BG_B_CYAN = '\u001b[46;1m'
    BG_B_WHITE = '\u001b[47;1m'

class Layer:
    def __init__(self, size_x, size_y, fill=CUIPY_COLOR.BLACK + '▒' + CUIPY_COLOR._RESET):
        self.size_x = size_x
        self.size_y = size_y
        
        self.grid = []

        for i in range(0, size_y):
            new_row = []
            for k in range(0, size_x):
                new_row.append(fill)
            self.grid.append(new_row)

    def unite(self, layer):
        for y in range(0, len(layer.grid)):
            for x in range(0, len(layer.grid[y])):
                if layer.grid[y][x]:
                    self.grid[y][x] = layer.grid[y][x]

    def draw(self):
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                print(self.grid[y][x], end='')
            print()

    def transparent(self):
        for i in range(0, len(self.grid)):
            for k in range(0, len(self.grid[i])):
                self.grid[i][k] = False
        return self

class Rectangle:
    def __init__(self, x, y, width, height, symbol=CUIPY_COLOR.BG_WHITE + '▓' + CUIPY_COLOR._RESET):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height
        self.symbol = symbol

    def draw_for_layer(self, layer):
        for i in range(self.x1, self.x2 + 1):
            layer.grid[self.y1][i] = self.symbol
            layer.grid[self.y2][i] = self.symbol
        for i in range(self.y1, self.y2):
            layer.grid[i][self.x1] = self.symbol
            layer.grid[i][self.x2] = self.symbol

    def fill_area(self, layer):
        for i in range(self.y1, self.y2):
            for k in range(self.x1, self.x2):
                layer.grid[i][k] = self.symbol

class Line:
    def __init__(self, x1, y1, x2, y2, symbol=CUIPY_COLOR.BG_WHITE + '▓' + CUIPY_COLOR._RESET):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.symbol = symbol

    def draw_for_layer(self, layer):
        deltax = abs(self.x2 - self.x1)
        deltay = abs(self.y2 - self.y1)
        error = 0
        deltaerr = (deltay + 1) / (deltax + 1)
        y = self.y1
        diry = self.y2 - self.y1
        if diry > 0:
            diry = 1
        if diry < 0:
            diry = -1
        for x in range(self.x1, self.x2):
            layer.grid[y][x] = self.symbol
            error = error + deltaerr
            if error >= 1:
                y = y + diry
                error = error - 1.0

class TextBox:


    def __init__(self, size_x, size_y, label=False, text='Lorem impsum dolor sit amet', word_wrap=True):
        self.size_x = size_x
        self.size_y = size_y
        self.label = label
        self.text = text
        self.word_wrap = word_wrap

        self.binded_coords = False
        self.stretch = False

    def draw_for_layer(self, layer, origin_x, origin_y):
        baseRect = Rectangle(origin_x, origin_y, self.size_x, self.size_y)
        baseRect.draw_for_layer(layer)

        text_split = self.text.split(sep=' ')

        index_y = origin_y + 1
        index_x = origin_x + 1

        for i in range(0, len(self.label)):
            layer.grid[origin_y][i + origin_x + 1] = CUIPY_COLOR.BG_WHITE + CUIPY_COLOR.BLACK + self.label[i] + CUIPY_COLOR._RESET

        for i in range(0, len(text_split)):
            for k in text_split[i]:
                if index_x <= origin_x + self.size_x:
                    layer.grid[index_y][index_x] = k
                    index_x += 1
                else:
                    if index_y < origin_y + self.size_y:
                        index_y += 1
                        index_x = origin_x + 1
                    else:
                        return False

class ProgressBar:
    
    def __init__(self, size_x, size_y, val, label=False):
        self.size_x = size_x
        self.size_y = size_y
        self.label = label
        self.val = val

        self.binded_coords = False
        self.stretch = False

    def draw_for_layer(self, layer, origin_x, origin_y):
        baseRect = Rectangle(origin_x, origin_y, self.size_x, self.size_y)
        baseRect.draw_for_layer(layer)

        step = self.size_x / 100

        progressRect = Rectangle(origin_x + 1, origin_y + 1, round(self.val * step), self.size_y - 1, '░' + CUIPY_COLOR._RESET)
        

        progressRect.fill_area(layer)

        for i in range(0, len(str(self.val) + '%')):
            layer.grid[origin_y + (round(self.size_y / 2))][round(self.size_x / 2) + i] = (str(self.val) + '%')[i]
        for i in range(0, len(self.label)):
            layer.grid[origin_y][i + origin_x + 1] = CUIPY_COLOR.BG_WHITE + CUIPY_COLOR.BLACK + self.label[i] + CUIPY_COLOR._RESET

class Root:
    def __init__(self, res_x=100, res_y=40):
        os.system(f'mode con: cols={res_x} lines={res_y}')
        self.res_x = res_x
        self.res_y = res_y
        self.layers = []
        self.widgets = []

    def add_layer(self, layer):
        self.layers.append(layer)
    def del_last_layer(self):
        return self.layers.pop(len(self.layers))

    def generate_grid(self, cell_size_x, cell_size_y, margin=1):
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.margin = margin

    def draw_widget_fit(self, widget_index, cell_index_x=False, cell_index_y=False, layer_index=0):
        target = self.widgets[widget_index]
        if not target.stretch:
            target.size_x = self.cell_size_x - 1
            target.size_y = self.cell_size_y - 1
        else:
            target.size_x = (self.cell_size_x - 1) * target.stretch_factor_x
            target.size_y = (self.cell_size_y - 1) * target.stretch_factor_y

        if not (cell_index_x or cell_index_y):
            cell_index_x = target.binded_coords[0]
            cell_index_y = target.binded_coords[1]

        target_origin_x = (self.cell_size_x + self.margin) * cell_index_x + 1
        target_origin_y = (self.cell_size_y + self.margin) * cell_index_y + 1

        transp = Layer(self.res_x, self.res_y)
        transp.transparent()
        self.add_layer(transp)
            
        target.draw_for_layer(transp, target_origin_x, target_origin_y)

    def bind_widget(self, widget, cell_x, cell_y):
        widget.binded_coords = [cell_x, cell_y]
        self.widgets.append(widget)

    def bind_widget_stretched(self, widget, cell_x, cell_y, s_factor_x, s_factor_y):
        widget.stretch = True
        widget.binded_coords = [cell_x, cell_y]
        widget.stretch_factor_x = s_factor_x
        widget.stretch_factor_y = s_factor_y
        self.widgets.append(widget)

    def render(self):
        master_layer = Layer(self.res_x, self.res_y)
        for i in range(0, len(self.widgets)):
            self.draw_widget_fit(i)
        for i in self.layers:
            master_layer.unite(i)
        master_layer.draw()

root = Root()
root.generate_grid(20, 10)
text = ProgressBar(20, 10, 92, 'Bruh')

#root.bind_widget(text, 0, 0)

#root.render()

print(BRAILLE_LINE.F_SLOPE_0)
input()

                
