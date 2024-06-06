import time
import colored

import numpy as np

import tkinter
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

root = tkinter.Tk()

# Dimensions des containers en decimètres
LENGTH = int(115.83)
WIDTH = int(22.94)
HEIGHT = int(25.69)
# Composante alpha du RGB du rendu 3D
ALPHA = 0.8
# Barre de navigation custome du rendu 3D
class NavigationToolBarCustome(NavigationToolbar2Tk):
    toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan',
         'Left button pans, Right button zooms\n'
         'x/y fixes axis, CTRL fixes aspect',
         'move', 'pan'),
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis', 'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
        (None, None, None, None),
        ('Previous', 'Containers précedent', 'back', 'prev_container'),
        ('Next', 'Containers suivant', 'forward', 'next_container'),
      )

    def __init__(self, containers, container_number=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.containers = containers
        self.container_number = container_number

    def prev_container(self, *args):
        if self.container_number == 0:
            self.container_number = len(self.containers)
        self.container_number -= 1
        self._update_render()

    def next_container(self, *args):
        self.container_number += 1
        if self.container_number == len(self.containers):
            self.container_number = 0
        self._update_render()

    def _update_render(self):
        if root.winfo_children():
            for child in root.winfo_children():
                child.destroy()
        root.update()
        self.containers[self.container_number].render(self.containers, self.container_number)

class Container:
    def __init__(self, length: int = LENGTH, width: int = WIDTH, height: int = HEIGHT, dimension=3, next=None):
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height

        self.items = []
        self.used_length = 0
        self.used_area = 0
        self.used_volume = 0

        self.dim = dimension

        if dimension == 1:
            self.map = [0 for _ in range(length)]
        elif dimension == 2:
            self.map = [[0 for _ in range(width)] for _ in range(length)]
        elif dimension == 3:
            self.map = [[[0 for _ in range(width)] for _ in range(length)] for _ in range(height)]

    def __str__(self):
        return f'({self.length} m * {self.width} m * {self.height} m)'
    # Verifie si il y a assez de place pour poser l'objet à la position donner (coin superieur gauche de l'item)
    def check_enough_space(self, item, i=0, j=0, k=0):
        if self.dim == 1:
            return (self.length - j - item.length) >= 0
        if self.dim == 2:
            for y in range(j, j + item.length):
                for x in range(i, i + item.width):
                    if self.map[y][x] != 0:
                        return False
            return True
        if self.dim == 3:
            for z in range(k, k + item.height-1):
                for y in range(j, j + item.length-1):
                    for x in range(i, i + item.width-1):
                        if self.map[z][y][x] != 0:
                            return False
            return True
    # Rempli le mapping avec l'ID de l'item à l'endroit ou on le pose
    def fill_item(self, item):
        if self.dim == 1:
            for j in range(self.used_length, self.used_length + item.length):
                self.map[j] = item.id
            return True
        if self.dim == 2:
            for j in range(self.length - item.length + 1):
                for i in range(self.width - item.width + 1):
                    if self.map[j][i] == 0:
                        if self.check_enough_space(item, j=j, i=i):
                            for y in range(item.length):
                                for x in range(item.width):
                                    self.map[y + j][x + i] = item.id
                            return True
            return False
        if self.dim == 3:
            for k in range(self.height - item.height + 1):
                for j in range(self.length - item.length + 1):
                    for i in range(self.width - item.width + 1):
                        if self.map[k][j][i] == 0:
                            if self.check_enough_space(item, j=j, i=i, k=k):
                                for z in range(k, k + item.height):
                                    for y in range(j, j + item.length):
                                        for x in range(i, i + item.width):
                                            self.map[z][y][x] = item.id
                                return True
            return False
    # Ajoute un item selon le nombre de dimension choisi dans le container
    # return False si impossible
    def add_item(self, item):
        if self.fill_item(item):
            if self.dim == 1:
                self.items.append(item)
                self.used_length += item.length
                return True
            if self.dim == 2:
                self.items.append(item)
                self.used_area += item.area
                return True
            if self.dim == 3:
                self.items.append(item)
                self.used_volume += item.volume
                return True
        return False
    # Renvoie l'espace non utilisé dans le container selon la dimension
    def get_not_used_volume(self):
        if self.dim == 1:
            return self.length - self.used_length
        if self.dim == 2:
            return self.area - self.used_area
        if self.dim == 3:
            return self.volume - self.used_volume
    # Rendu 2D dans la console
    def print_map(self):
        # Taille en charactère d'un nombre
        cell_width = 3
        for row in self.map:
            print('| ', end='')
            for col in row:
                if col != 0:
                    color = colored.fg(col % 256)
                    print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                else:
                    print('_', end='')
            print(' |')
    # Rendu 3D selon 1 à 3 dimension
    def render(self, containers, container_number=0):
        # Figure dans la quel faire le rendu
        fig = Figure(figsize=(10, 6), dpi=100)
        frame = FigureCanvasTkAgg(fig, master=root)
        # Les dimensions des axes de la figure qui correspondent aux dimensions du container
        axes = [23, 116, 26]
        # Matrice 3D contenant items à coloré
        render_map = np.empty(axes, dtype=bool)
        # Matrice 3D contenant les couleurs des items
        colors = np.empty(axes + [4], dtype=np.float32)
        if self.dim == 3:
            for k in range(self.height):
                for j in range(self.length):
                    for i in range(self.width):
                        if self.map[k][j][i] != 0:
                            id = self.map[k][j][i]
                            render_map[i][j][k] = True
                            # Choisit une couleur selon l'id de l'item
                            colors[i][j][k] = ((id*10%256)/256 if id%3==0 else 0, (id*10%256)/256 if id%3==1 else 0, (id*10%256)/256 if id%3==2 else 0, ALPHA)
        elif self.dim == 2:
            for j in range(self.length):
                for i in range(self.width):
                    if self.map[j][i] != 0:
                        id = self.map[j][i]
                        render_map[i][j][0] = True
                        colors[i][j][0] = (
                        (id * 10 % 256) / 256 if id % 3 == 0 else 0, (id * 10 % 256) / 256 if id % 3 == 1 else 0,
                        (id * 10 % 256) / 256 if id % 3 == 2 else 0, ALPHA)
        elif self.dim == 1:
            for j in range(self.length):
                for i in range(self.width):
                    if self.map[j] != 0:
                        id = self.map[j]
                        render_map[0][j][0] = True
                        colors[0][j][0] = (
                        (id * 10 % 256) / 256 if id % 3 == 0 else 0, (id * 10 % 256) / 256 if id % 3 == 1 else 0,
                        (id * 10 % 256) / 256 if id % 3 == 2 else 0, ALPHA)
        # Paramétrage des axes du rendu 3D
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(f'Container {container_number}')
        # Parametrage des bornes des axes
        ax.axes.set_xlim([0, 22])
        ax.axes.set_ylim([115, 0])
        ax.axes.set_zlim([0, 25])
        # Parametrage des label des axes
        ax.set_xlabel('Largeur')
        ax.set_ylabel('Longueur')
        ax.set_zlabel('Hauteur')
        # Parametres les axes pour être de meme norme
        ax.set_aspect('equal', adjustable='box')
        # Ajout du voxel contenant tous les items et leur couleur sur le rendu 3D
        ax.voxels(render_map, facecolors=colors)
        # Ajour d'une barre de navigation sous le rendu 3D
        toolbar = NavigationToolBarCustome(containers, container_number, frame, root)
        toolbar.update()

        frame.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


class Item:
    def __init__(self, id: int, name: str, length: int, width: int, height: int):
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height

    @staticmethod
    def list_from_csv(filename: str):
        item_list = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    number, name, length, width, height = line.strip().split(';')
                    item = Item(int(number), name, int(float(length) * 10), int(float(width) * 10),
                                int(float(height) * 10))
                    item_list.append(item)
        except FileNotFoundError:
            print(f'File {filename} not found')

        return item_list


def d1(items: [Item]) -> [Item]:
    containers = []
    items = sorted(items, reverse=True, key=lambda x: x.length)
    i = 0
    while len(items) != 0:
        j = i
        keep = True
        item = items[0]
        while keep:
            if len(containers) == j:
                containers.append(Container(dimension=1))
                containers[j].add_item(item)
                del items[0]
                keep = False
            elif (containers[j].length - containers[j].used_length) >= item.length:
                containers[j].add_item(item)
                del items[0]
                keep = False
            else:
                for item_to_replace in containers[j].items:
                    if containers[j].used_length - item_to_replace.length + item.length <= containers[
                        j].length and item_to_replace.length < item.length:
                        containers[j].remove_item(item_to_replace)
                        containers[j].add_item(item)
                        del items[0]
                        items.insert(0, item_to_replace)
                        keep = False
                        break
            j += 1
        if containers[i].used_length == containers[i].length:
            i += 1

    return containers


def d(items: [Item], dim: int = 3, offline: bool = False) -> [Container]:
    containers = []
    if offline:
        if dim == 1:
            items = sorted(items, reverse=True, key=lambda x: x.length)
        elif dim == 2:
            items = sorted(items, reverse=True, key=lambda x: x.area)
        else:
            items = sorted(items, reverse=True, key=lambda x: x.volume)
    for item in items:
        j = 0
        keep_going = True
        while keep_going:
            if len(containers) == j:
                containers.append(Container(dimension=dim))
                inserted = containers[j].add_item(item)
                if inserted:
                    keep_going = False
            elif dim == 1:
                if (containers[j].length - containers[j].used_length) >= item.length:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            elif dim == 2:
                if (containers[j].area - containers[j].used_area) >= item.area:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            elif dim == 3:
                if (containers[j].volume - containers[j].used_volume) >= item.volume:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            j += 1
    return containers


def print_as_a_table(resultArray):
    for i in range(len(resultArray)):
        if i == 0:
            headers = ["Online", "Nombre wagons", "dimension non occupée (dm)", "Temps calcul"]
        else:
            headers = ["Offline", "Nombre wagons", "dimension non occupée (dm)", "Temps calcul"]
        table = [headers]

        for d in range(len(resultArray[i])):
            dim = f"d={d + 1}"
            nombre_wagons = len(resultArray[i][d][0])
            non_occupee = sum(c.get_not_used_volume() for c in resultArray[i][d][0])
            temps_calcul = resultArray[i][d][1]

            table.append([dim, nombre_wagons, non_occupee, temps_calcul])

        for row in table:
            print("{:<10} {:<15} {:<25} {:<15}".format(*row))

        print()


def print_containers(containers):
    cell_width = 3
    if containers[0].dim == 1:
        for container in containers:
            row = container.map
            print('| ', end='')
            for col in row:
                if col != 0:
                    color = colored.fg(col % 256)
                    print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                else:
                    print('_' * cell_width, end='')
            print(' |')
    if containers[0].dim == 2:
        nb_rows = containers[0].length
        for i in range(nb_rows):
            for container in containers:
                row = container.map[i]
                print('| ', end='')
                for col in row:
                    if col != 0:
                        color = colored.fg(col % 256)
                        print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                    else:
                        print('_' * cell_width, end='')
                print(' |   ', end='')
            print()
    if containers[0].dim == 3:
        print('Impossible de render des container en 3D dans la console. Merci d\'utiliser la fonction Container.render([Container])')

def init_interactive():
    root.wm_title("Visualisation des containers")
    root.iconbitmap("logo.ico")

if __name__ == '__main__':
    items = Item.list_from_csv('Données_marchandises_2324.csv')

    INTERACTIVE_MODE = True
    CONSOLE_MODE = True

    resultArray = [[], []]

    for i in range(3):
        start_time = time.time()
        resultArray[0].append([d(items, dim=i + 1, offline=False)])
        resultArray[0][i].append(time.time() - start_time)

        start_time = time.time()
        resultArray[1].append([d(items, dim=i + 1, offline=True)])
        resultArray[1][i].append(time.time() - start_time)

    print_as_a_table(resultArray)

    result = d(items, dim=1, offline=False)
    if CONSOLE_MODE:
        print_containers(result)
    if INTERACTIVE_MODE:
        init_interactive()
        result[0].render(result)
        tkinter.mainloop()
