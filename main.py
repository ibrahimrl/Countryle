from logic import *
from tkinter import *
from PIL import Image, ImageTk
from tkintermapview import TkinterMapView

CIRCLE_SIZE: int = 75
HORIZONTAL_TEXT_MARGIN: int = 2
VERTICAL_CIRCLE_MARGIN: int = 25
VERTICAL_TEXT_MARGIN: int = 20
Current_Point: tuple = (335, 190)

COLOR: dict = {
    'True': '#00903c',
    'False': '#bb0823',
    'Almost': '#f7b53e',
    'Coordinate': '#57abdd',
    'Submit': '#555555',
    'Background': '#fafafa'}

class View(Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=1050, height=650, background=COLOR['Background'])
        self.grid()
        self.parent = parent
        self.start_view()

    def start_view(self):
        self.text(525, 30, 'COUNTRYLE', 25, 'Black')

        self.create_line(325, 65, 725, 65, width=1, fill='Black')
        self.create_line(325, 540, 725, 540, width=1, fill='Black')
        self.create_line(400, 602, 650, 602, width=1, fill='Black')

        self.entry = Entry(self.parent, width=20, fg='Black', bg='#fafafa', bd=0, justify=CENTER)
        self.entry.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])

        self.create_window(525, 590, window=self.entry, anchor=CENTER)

        self.image_placer()

        self.create_rectangle(390, 560, 660, 620, width=1, outline='Black')
        self.image_submit = image_resizer('Img/submit.png')
        self.button_submit = Button(self, image=self.image_submit, command=country_name, activebackground='red', bd=0)
        self.button_submit.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])
        self.create_window(700, 590, window=self.button_submit)

    def image_placer(self):
        self.image_map = PhotoImage(file='Img/map.png')
        self.create_image(525, 325, image=self.image_map, anchor=CENTER)

        self.image_hem = image_resizer('Img/hemisphere.png')
        self.create_image(335, 110, image=self.image_hem, anchor=W)
        self.text(360, 145, 'Hemisphere', 10, 'Black', justify=CENTER)

        self.image_con = image_resizer('Img/continent.png')
        self.create_image(417, 110, image=self.image_con, anchor=W)
        self.text(442, 145, 'Continent', 10, 'Black', justify=CENTER)

        self.image_temp = image_resizer('Img/avg-temperature.png')
        self.create_image(525, 110, image=self.image_temp, anchor=CENTER)
        self.text(525, 145, 'Avg.\nTemperature', 10, 'Black', justify=CENTER)

        self.image_pop = image_resizer('Img/population.png')
        self.create_image(582, 110, image=self.image_pop, anchor=W)
        self.text(607, 145, 'Population', 10, 'Black', justify=CENTER)

        self.image_cord = image_resizer('Img/direction.png')
        self.create_image(715, 110, image=self.image_cord, anchor=E)
        self.text(690, 145, 'Coordinates', 10, 'Black', justify=CENTER)

        self.image_lower = image_resizer('Img/lower.png', 10, 10)
        self.image_higher = image_resizer('Img/higher.png', 10, 10)
        self.image_found = image_resizer('Img/location.png', 30, 30)

    def game_update(self, game_status):
        global Current_Point
        x, y = Current_Point
        self.create_text(x - 10, y, text=game_status[0], anchor=W, font=('Helvetica', 20), fill='Black')
        Current_Point = (x, y + VERTICAL_TEXT_MARGIN)
        self.oval(game_status[1:])

    def oval(self, game_status):
        global Current_Point
        x, y = Current_Point
        for c, d in game_status:
            if isinstance(d, tuple):
                self.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, width=0, fill=COLOR[str(d[0])])
                if d[1] != 0:
                    img, image_coordinate = self.higher_lower(d[1])
                    self.create_image(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2 + image_coordinate, image=img)
            else:
                self.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, width=0, fill=COLOR[str(d)])
            if c == 'Target is found':
                self.create_image(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2, image=self.image_found, anchor=CENTER)
            else:
                self.create_text(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2, text=str(c), font=('Helvetica', 10), fill='White')
            x += CIRCLE_SIZE + HORIZONTAL_TEXT_MARGIN
        y += CIRCLE_SIZE + VERTICAL_CIRCLE_MARGIN
        Current_Point = (335, y)

    def text(self, x: int, y: int, text: str, size: int, color: str, **args):
        self.create_text(x, y, text=text, font=('Helvetica', size), fill=color, **args)

    def higher_lower(self, num) -> tuple:
        return (self.image_higher, -20) if num < 0 else (self.image_lower, 20)

    def redraw_board(self):
        self.delete('all')
        self.start_view()
        global Current_Point
        Current_Point = (335, 190)
        n = len(NewGame.DataGuessedCountries)
        i = 0 if n <= 3 else n - 3
        for e in NewGame.DataGuessedCountries[i:]:
            self.game_update(e)

    def map(self, name):
        root_tk = Tk()
        root.title(name)
        root_tk.geometry(f"{600}x{400}")
        map_widget = TkinterMapView(root_tk, width=300, height=200, corner_radius=0)
        map_widget.set_address(name, marker=True)

def image_resizer(img, x=50, y=50):
    given_img = (Image.open(img))
    resized_img = given_img.resize((x, y), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)

def format_input(name):
    return ' '.join(map(lambda x: x[0].upper() + x[1:].lower(), name.split(' ')))

def country_name() -> str:
    name: str = canvas.entry.get()
    if len(name) > 0:
        entered_country(format_input(name))


NewGame: Game = Game()

def entered_country(name):
    CurrentCountry: Country = NewGame.new_country(name)
    if CurrentCountry is not None:
        canvas.entry.delete(0, END)
        NewGame.check(CurrentCountry, NewGame.Target)
        canvas.redraw_board()
        if CurrentCountry.Name == NewGame.Target.Name:
            NewGame.win_results(CurrentCountry)
            NewGame.end_game()
            # canvas.map(CurrentCountry)


root: Tk = Tk()
root.title('Countryle')
canvas = View(root)
root.mainloop()


# f = ResultsTable()
# print(f'Played games: {f.FileLoad["NumberOfGames"]}')
# print(f'Wins: {f.FileLoad["Wins"]}')
