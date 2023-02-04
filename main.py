from logic import *
from tkinter import *
from PIL import Image, ImageTk

CIRCLE_SIZE: int = 75
HORIZONTAL_TEXT_MARGIN: int = 2
VERTICAL_CIRCLE_MARGIN: int = 25
VERTICAL_TEXT_MARGIN: int = 20
VERTICAL_RESULTS_MARGIN: int = 80
HORIZONTAL_RESULTS_MARGIN: int = 20
Current_Point: tuple[int, int] = (335, 190)

COLOR: dict[str, str] = {
    'True': '#00903c',
    'False': '#bb0823',
    'Almost': '#f7b53e',
    'Coordinate': '#57abdd',
    'Submit': '#555555',
    'Background': '#fafafa'}


class View(Canvas):
    def __init__(self, parent: Tk):
        super().__init__(parent, width=1050, height=650, background=COLOR['Background'])
        self.grid()
        self.parent: Tk = parent
        self.main_page()

    def top_view(self):
        self.text(525, 30, 'COUNTRYLE', 25, 'Black')
        self.create_line(325, 65, 725, 65, width=1, fill='Black')

    def main_page(self):
        self.top_view()

        self.create_line(325, 540, 725, 540, width=1, fill='Black')
        self.create_line(400, 602, 650, 602, width=1, fill='Black')

        self.entry = Entry(self.parent, width=20, fg='Black', bg='#fafafa', bd=0, justify=CENTER)
        self.entry.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])

        self.create_window(525, 590, window=self.entry, anchor=CENTER)

        self.images()

        self.create_rectangle(390, 560, 660, 620, width=1, outline='Black')

        self.button_submit = Button(self, image=self.image_submit, command=country_name, activebackground='White', bd=0)
        self.button_submit.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])
        self.create_window(700, 590, window=self.button_submit)

        self.button_resign = Button(self, image=self.image_resign, command=resign, activebackground='White', bd=0)
        self.button_resign.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])
        self.create_window(350, 590, window=self.button_resign)

        self.button_results = Button(self, image=self.image_results, command=results, activebackground='White', bd=0)
        self.button_results.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])
        self.create_window(690, 30, window=self.button_results)

    def results_page(self, games: int, wins: int, discovered: str, continents: dict[str, str]):
        self.image_map = PhotoImage(file='Img/map.png')
        self.create_image(525, 325, image=self.image_map, anchor=CENTER)

        self.top_view()

        self.text(525, 100, 'Statistics', 25, 'Black')

        self.text(485, 150, games, 20, 'Black')
        self.text(485, 180, 'Played\ngames', 15, 'Black')

        self.text(565, 150, wins, 20, 'Black')
        self.text(565, 170, 'Wins', 15, 'Black')

        self.text(525, 500, 'Discovered', 25, 'Black')
        self.text(525, 540, discovered, 40, 'Black')
        self.text(525, 580, 'of Countryle', 25, 'Black')

        cordinates: dict[str, tuple[int, int]] = {'Asia': (608, 275), 'Australia': (658, 385), 'Africa': (530, 335),
                                                  'Europe': (530, 275), 'America': (415, 330)}

        for c in cordinates.keys():
            x, y = cordinates[c]
            self.text(x, y, c, 15, 'Black')
            self.text(x, y + HORIZONTAL_RESULTS_MARGIN, continents[c], 15, 'Black')

        self.restart()


    def images(self):
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

        self.image_submit = image_resizer('Img/submit.png')
        self.image_resign = image_resizer('Img/resign.png')
        self.image_lower = image_resizer('Img/lower.png', 10, 10)
        self.image_higher = image_resizer('Img/higher.png', 10, 10)
        self.image_found = image_resizer('Img/location.png', 30, 30)
        self.image_win = image_resizer('Img/win.png', 25, 25)
        self.image_results = image_resizer('Img/results.png', 35, 35)
        self.image_restart = image_resizer('Img/restart.png')


    def restart(self):
        self.button_restart = Button(self, image=self.image_restart, command=restart_game, activebackground='White', bd=0)
        self.button_restart.config(highlightbackground=COLOR['Background'], highlightcolor=COLOR['Background'])
        self.create_window(800, 590, window=self.button_restart)

    def game_update(self, game_status: tuple):
        global Current_Point
        x, y = Current_Point
        if game_status[0][1] == NewGame.Target.name:
            self.create_image(x - 5, y - 5, image=self.image_win, anchor=CENTER)
            self.text(x + 10, y, NewGame.Target.name, 20, 'Black', W)
        else:
            self.text(x - 10, y, '. '.join(game_status[0]), 20, 'Black', W)
        Current_Point = (x, y + VERTICAL_TEXT_MARGIN)
        self.oval(game_status[1:])

    def oval(self, game_status: tuple):
        global Current_Point
        x, y = Current_Point
        for c, d in game_status:
            if isinstance(d, tuple):
                self.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, width=0, fill=COLOR[d[0]])
                if d[1] != 0:
                    img, image_coordinate = self.comparing_temperatures(d[1])
                    self.create_image(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2 + image_coordinate, image=img)
            else:
                self.create_oval(x, y, x + CIRCLE_SIZE, y + CIRCLE_SIZE, width=0, fill=COLOR[d])
            if c == 'Target is found':
                self.create_image(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2, image=self.image_found, anchor=CENTER)
            else:
                self.text(x + CIRCLE_SIZE // 2, y + CIRCLE_SIZE // 2, str(c), 10, 'White')
            x += CIRCLE_SIZE + HORIZONTAL_TEXT_MARGIN
        y += CIRCLE_SIZE + VERTICAL_CIRCLE_MARGIN
        Current_Point = (335, y)

    def text(self, x: int, y: int, text: str, size: int, color: str, anc=CENTER, **args):
        self.create_text(x, y, text=text, font=('Helvetica', size), fill=color, anchor=anc, **args)

    def comparing_temperatures(self, num: int) -> tuple:
        return (self.image_higher, -20) if num < 0 else (self.image_lower, 20)

    def redraw_board(self):
        self.delete('all')
        self.main_page()
        global Current_Point
        Current_Point = (335, 190)
        n: int = len(NewGame.data_guessed_countries)
        i: int = 0 if n <= 3 else n - 3
        for e in NewGame.data_guessed_countries[i:]:
            self.game_update(e)


def set_game():
    global NewGame
    NewGame = Game()


def restart_game():
    canvas.delete('all')
    canvas.main_page()
    set_game()


def image_resizer(img: str, x: int = 50, y: int = 50) -> PhotoImage:
    given_img = (Image.open(img))
    resized_img = given_img.resize((x, y), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_img)


def formatting_input(name: str) -> str:
    return ' '.join(map(lambda x: x[0].upper() + x[1:].lower(), name.split(' ')))


def country_name():
    name: str = canvas.entry.get()
    if len(name) > 0:
        entered_country(formatting_input(name))


def entered_country(name: str):
    current_country: Country = NewGame.new_country(name)
    if current_country is not None:
        canvas.entry.delete(0, END)
        compare_countries(current_country)
        if current_country.name == NewGame.Target.name:
            NewGame.win_results(current_country)
            NewGame.end_game()
            canvas.restart()
    if NewGame.attempts == 0:
        resign()


def compare_countries(country: Country):
    if not NewGame.is_finished:
        NewGame.check(country, NewGame.Target)
        canvas.redraw_board()


def resign():
    compare_countries(NewGame.Target)
    NewGame.end_game()
    canvas.restart()


def results():
    res = ResultsTable()
    canvas.delete('all')
    canvas.results_page(res.game_number(), res.win_number(), res.discovered(), res.continents())


set_game()

root: Tk = Tk()
root.title('Countryle')
canvas = View(root)
root.mainloop()
