from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np
import colored
import tkinter

LENGTH = int(115.83)
WIDTH = int(22.94)
HEIGHT = int(25.69)

root = tkinter.Tk()

# Composante alpha du RGBA du rendu 3D
ALPHA = 0.9


def get_color(number):
    """
    Renvoie une couleur RGBA en fonction de l'entier entré
    :param number: Un nombre qui correspond a une couleur
    :type number: int
    :return: Un RGBA avec l'alpha plus :
        Si le reste de la division par 3 vaut 0, seulement une composante Rouge
        Si le reste de la division par 3 vaut 1, seulement une composante Vert
        Si le reste de la division par 3 vaut 2, seulement une composante Bleu
    """
    return (
        (number * 10 % 256) / 256 if number % 3 == 0 else 0,
        (number * 10 % 256) / 256 if number % 3 == 1 else 0,
        (number * 10 % 256) / 256 if number % 3 == 2 else 0,
        ALPHA
    )


def init_interactive():
    """
    Initialisation de la fenêtre tkinter
    :return: None
    """
    # Titre de la fenêtre tkinter
    root.wm_title("Visualisation des containers")
    # Logo de la fenêtre tkinter
    root.iconbitmap("logo.ico")


# Barre de navigation custome du rendu 3D
class NavigationToolBarCustome(NavigationToolbar2Tk):
    """
    Barre de navigation tkinter pour matplotlib qui permet de changer de container en plus des fonctionalité de base
    """
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
        """

        :param containers: Tous les containers qui à afficher
        :type containers: list[Container]
        :param container_number: Le numero du container actif à afficher
        :type container_number: int
        :param args: Les arguments positionels que prend la classe NavigationToolbar2Tk
        :param kwargs: Les arguments nommés que prend la classe NavigationToolbar2Tk
        """
        super().__init__(*args, **kwargs)
        self.containers = containers
        self.container_number = container_number

    def prev_container(self):
        """
        Affiche le container précédent dans la liste. Si c'est le premier container qui est actif, affiche le dernier container
        :return: None
        """
        if self.container_number == 0:
            self.container_number = len(self.containers)
        self.container_number -= 1
        self._update_render()

    def next_container(self):
        """
        Affiche le container suivant dans la liste. Si c'est le dernier container qui est actif, affiche le premier container
        :return: None
        """
        self.container_number += 1
        if self.container_number == len(self.containers):
            self.container_number = 0
        self._update_render()

    def _update_render(self):
        """
        Supprime l'affichage de l'ancien container ainsi que ca navbar. Affiche le container actif avec ca navbar
        :return: None
        """
        if root.winfo_children():
            for child in root.winfo_children():
                child.destroy()
        root.update()
        self.containers[self.container_number].render(self.containers, self.container_number)


class Item:
    """
    Correspond a un objet à mettre dans les container
    Contient ces dimension et son espace occupé selon les 3 dimension.
    """

    def __init__(self, id: int, name: str, length: int, width: int, height: int):
        """

        :param id: L'id de l'item
        :type id: int
        :param name: Le nom de l'item
        :type name: str
        :param length: La longueur de l'item
        :type length: int
        :param width: La largeur de l'item
        :type width: int
        :param height: le hauteur de l'item
        :type height: int
        """
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height

    @staticmethod
    def list_from_csv(filename: str):
        """
        Permet de générer une liste d'item à partir d'un CSV
        :param filename: Non du fichier où lire les données
        :type filename: str
        :return: list[Item] -> Renvoie la liste des item du fichier CSV
        """
        item_list = []
        try:
            # Ouvre le fichier
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    # Crée les items
                    number, name, length, width, height = line.strip().split(';')
                    # Convertit les unité de mètre vers décimètre
                    item = Item(int(number), name, int(float(length) * 10), int(float(width) * 10),
                                int(float(height) * 10))
                    item_list.append(item)
        except FileNotFoundError:
            print(f'File {filename} not found')

        return item_list


class Container:
    """
    Contien l'ensemble des item dans un container ainsi que leur position sur une carte du container.
    """

    def __init__(self, length: int = LENGTH, width: int = WIDTH, height: int = HEIGHT, dimension=3):
        """

        :param length: Longueur du container
        :type length: int
        :param width: Largeur du container
        :type width: int
        :param height: Hauteur du container
        :type height: int
        :param dimension: Dimension du container : 1, 2 ou 3
        :type dimension: int
        """
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height
        # Liste des items dans le container
        self.items = []
        # Total de l'espace utilise en fonction de la dimension
        self.used_length = 0
        self.used_area = 0
        self.used_volume = 0
        # Dimension voulu pour le container
        self.dim = dimension
        # Matrice 1D ou 2D ou 3D en fonction de la dimension
        if dimension == 1:
            self.map = [0 for _ in range(length)]
        elif dimension == 2:
            self.map = [[0 for _ in range(width)] for _ in range(length)]
        elif dimension == 3:
            self.map = [[[0 for _ in range(width)] for _ in range(length)] for _ in range(height)]

    def __str__(self):
        return f'({self.length} m * {self.width} m * {self.height} m)'

    def check_enough_space(self, item, i=0, j=0, k=0):
        """
        Verifie si il y a assez de place pour poser l'objet à la position donné (le coin superieur au sol gauche de l'item correspond au (0, 0, 0))
        :param item: L'item pour le quel il faut verifié si l'espace est disponnible
        :type item: Item
        :param i: Première coordonée sur le repère du container
        :type i: int
        :param j: Deuxième coordonée sur le repère du container
        :type j: int
        :param k: Troisième coordonée sur le repère du container
        :type k: int
        :return: bool -> True si il y a assez de place, False sinon
        """
        # En dimension 1, verifie seulement si il reste assez de longueur.
        if self.dim == 1:
            return (self.length - j - item.length) >= 0
        # En dimension 2, regarde sur la map si les cases néscessaire ne sont pas utilisées
        if self.dim == 2:
            for y in range(j, j + item.length):
                for x in range(i, i + item.width):
                    if self.map[y][x] != 0:
                        return False
            return True
        # En dimension 3, regarde sur la map si les cases néscessaire ne sont pas utilisées
        if self.dim == 3:
            for z in range(k, k + item.height - 1):
                for y in range(j, j + item.length - 1):
                    for x in range(i, i + item.width - 1):
                        if self.map[z][y][x] != 0:
                            return False
            return True

    def fill_item(self, item):
        """
        Verifie si l'item peut être placé à un endroit et rempli le mapping avec l'ID de l'item à l'endroit où on le place
        Attention : En dimension 1, le check doit déjà avoir été fait avant d'appeler la fonction
        :param item: L'item a placé
        :type item: Item
        :return: bool -> True si l'item a pu être placé, False sinon
        """
        # En dimension 1, le check doit déjà avoir été fait avant d'appeler la fonction.
        if self.dim == 1:
            # Ecrit sur la map
            for j in range(self.used_length, self.used_length + item.length):
                self.map[j] = item.id
            return True
        # Dimension 2
        if self.dim == 2:
            for j in range(self.length - item.length + 1):
                for i in range(self.width - item.width + 1):
                    # Cherche un emplacement où il n'y a pas d'item
                    if self.map[j][i] == 0:
                        # Verifie si il y a assez de place pour l'item
                        if self.check_enough_space(item, j=j, i=i):
                            # Ecrit sur la map
                            for y in range(item.length):
                                for x in range(item.width):
                                    self.map[y + j][x + i] = item.id
                            return True
            return False
        #Dimension 3
        if self.dim == 3:
            for k in range(self.height - item.height + 1):
                for j in range(self.length - item.length + 1):
                    for i in range(self.width - item.width + 1):
                        # Cherche un emplacement où il n'y a pas d'item
                        if self.map[k][j][i] == 0:
                            # Verifie si il y a assez de place pour l'item
                            if self.check_enough_space(item, j=j, i=i, k=k):
                                # Ecrit sur la map
                                for z in range(k, k + item.height):
                                    for y in range(j, j + item.length):
                                        for x in range(i, i + item.width):
                                            self.map[z][y][x] = item.id
                                return True
            return False
        return False

    def add_item(self, item):
        """
        Ajoute un item selon le nombre de dimension choisi dans le container
        :param item: L'item à ajouter
        :type item: Item
        :return: True si l'itema été ajouté, False sinon
        """
        # Essaie d'ecrire à un endroit sur la carte l'item
        if self.fill_item(item):
            # Ajoute l'item dans la liste des items du container
            self.items.append(item)
            # Actualise l'espace utilisé
            # Dimension 1
            if self.dim == 1:
                self.used_length += item.length
                return True
            # Dimension 2
            if self.dim == 2:
                self.used_area += item.area
                return True
            # Dimension 3
            if self.dim == 3:
                self.used_volume += item.volume
                return True
        return False

    def get_not_used_volume(self):
        """
        Renvoie l'espace non utilisé dans le container selon la dimension
        :return: int en decimètre puissance la dimension
        """
        if self.dim == 1:
            return self.length - self.used_length
        if self.dim == 2:
            return self.area - self.used_area
        if self.dim == 3:
            return self.volume - self.used_volume

    def print_map(self):
        """
        Rendu 1D ou 2D du container dans la console
        :return: None
        """
        # Taille en charactère d'un nombre
        cell_width = 3
        # Dimension 1
        if self.dim == 1:
            print('| ', end='')
            for col in self.map:
                if col != 0:
                    # Couleur en fonction de l'id de l'item
                    color = colored.fg(col % 256)
                    print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                else:
                    print('_', end='')
            print(' |')
        # Dimension 2
        if self.dim == 2:
            for row in self.map:
                print('| ', end='')
                for col in row:
                    if col != 0:
                        # Couleur en fonction de l'id de l'item
                        color = colored.fg(col % 256)
                        print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                    else:
                        print('_', end='')
                print(' |')
        else:
            print(
                'Impossible de render un container en 3D dans la console. Merci d\'utiliser la fonction Container.render([Container])')

    def render(self, containers, container_number=0):
        """
        Rendu 3D de 1 à 3 dimension
        :param containers: La liste de container à render
        :type containers: list[Container]
        :param container_number: Le numéro du container à afficher
        :type container_number: int
        :return: None
        """
        # Figure dans laquelle faire le rendu
        fig = Figure(figsize=(10, 6), dpi=100)
        frame = FigureCanvasTkAgg(fig, master=root)
        # Les dimensions des axes de la figure qui correspondent aux dimensions du container en décimètres
        axes = [23, 116, 26]
        # Matrice 3D contenant les items à coloré
        render_map = np.empty(axes, dtype=bool)
        # Matrice 3D contenant les couleurs des items
        colors = np.empty(axes + [4], dtype=np.float32)
        # Dimension 3
        if self.dim == 3:
            for k in range(self.height):
                for j in range(self.length):
                    for i in range(self.width):
                        # Si il y a un item sur la map
                        if self.map[k][j][i] != 0:
                            id = self.map[k][j][i]
                            # Met la case comme a coloré
                            render_map[i][j][k] = True
                            # Choisit une couleur selon l'id de l'item
                            colors[i][j][k] = get_color(id)
        # Dimension 2
        elif self.dim == 2:
            for j in range(self.length):
                for i in range(self.width):
                    if self.map[j][i] != 0:
                        id = self.map[j][i]
                        render_map[i][j][0] = True
                        colors[i][j][0] = get_color(id)
        # Dimension 1
        elif self.dim == 1:
            for j in range(self.length):
                if self.map[j] != 0:
                    id = self.map[j]
                    render_map[0][j][0] = True
                    colors[0][j][0] = get_color(id)
        # Ajout d'un plot sur la figure
        ax = fig.add_subplot(111, projection='3d')
        # Titre du plot
        ax.set_title(f'Container {container_number}')
        # Paramétrage des axes du rendu 3D
        # Parametrage des bornes des axes
        ax.axes.set_xlim([0, 22])
        ax.axes.set_ylim([115, 0])
        ax.axes.set_zlim([0, 25])
        ax.set_xticks([0, 5, 10, 15, 20])
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


def print_containers(containers):
    """
    Affiche les containers côte à côte dans la console en 2D et l'un sous l'autre en 1D
    :param containers: Les containers à afficher dans la console
    :type containers: list[Container]
    :return: None
    """
    # Taille d'un nombre
    cell_width = 3
    # Dimension 1
    if containers[0].dim == 1:
        for container in containers:
            row = container.map
            print('| ', end='')
            for col in row:
                if col != 0:
                    # Couleur selon l'id de l'item
                    color = colored.fg(col % 256)
                    print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                else:
                    print('_' * cell_width, end='')
            print(' |')
    # Dimension 2
    if containers[0].dim == 2:
        nb_rows = containers[0].length
        for i in range(nb_rows):
            for container in containers:
                row = container.map[i]
                print('| ', end='')
                for col in row:
                    if col != 0:
                        # Couleur selon l'id de l'item
                        color = colored.fg(col % 256)
                        print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                    else:
                        print('_' * cell_width, end='')
                print(' |   ', end='')
            print()
    # Dimension 3
    if containers[0].dim == 3:
        print(
            'Impossible de render des container en 3D dans la console. Merci d\'utiliser la fonction Container.render([Container])')


def print_as_a_table(resultArray):
    """
    Affiche dans la console les résultats des test dans les trois dimension en offline et en online de l'algorithme
    :param resultArray:
    :type resultArray: list
    :return: None
    """
    # Online / Offline
    for i in range(len(resultArray)):
        if i == 0:
            headers = ["Online", "Nombre wagons", "dimension non occupée (dm)", "Temps calcul"]
        else:
            headers = ["Offline", "Nombre wagons", "dimension non occupée (dm)", "Temps calcul"]
        table = [headers]
        # Chaque dimension
        for d in range(len(resultArray[i])):
            dim = f"d={d + 1}"
            nombre_wagons = len(resultArray[i][d][0])
            non_occupee = sum(c.get_not_used_volume() for c in resultArray[i][d][0])
            temps_calcul = resultArray[i][d][1]

            table.append([dim, nombre_wagons, non_occupee, temps_calcul])

        for row in table:
            print("{:<10} {:<15} {:<25} {:<15}".format(*row))

        print()


def d(items: [Item], dim: int = 3, offline: bool = False) -> [Container]:
    """
    Calcul de facon heuristique la facon de remplir un container de 1 à 3 dimension et online ou offline.
    Le mode offline tri les items selon l'espace occuper dans la dimension choisit puis utilise l'algorithme du online
    :param items: La liste des item à ordonnée dans des containers
    :type items: list[Item]
    :param dim: La dimension dans la quel travailler. La dimension va de 1 à 3
    :type dim: int
    :param offline: Si il faut ordonné les item au fur et à meusure qu'il arrive ou non
    :type offline: bool
    :return: list[Container] -> Les containers néscessaire pour ordonné tous les items
    """
    containers = []
    # Si offline, try selon la dimension
    if offline:
        if dim == 1:
            items = sorted(items, reverse=True, key=lambda x: x.length)
        elif dim == 2:
            items = sorted(items, reverse=True, key=lambda x: x.area)
        else:
            items = sorted(items, reverse=True, key=lambda x: x.volume)
    for item in items:
        # Index du container
        j = 0
        keep_going = True
        # Tant que l'item n'a pas été mis dans un container, passe au container suivant
        while keep_going:
            # Si l'item n'a pu aller dans aucun des containers existant, crée en un nouveau
            if len(containers) == j:
                containers.append(Container(dimension=dim))
                inserted = containers[j].add_item(item)
                if inserted:
                    keep_going = False
            # Dimension 1
            elif dim == 1:
                # Si il n'y a pas assez de longueur dans le container pour l'item n'essaye meme pas de l'insérer
                if (containers[j].length - containers[j].used_length) >= item.length:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            # Dimension 2
            elif dim == 2:
                # Si il n'y a pas assez de surface dans le container pour l'item n'essaye meme pas de l'insérer
                if (containers[j].area - containers[j].used_area) >= item.area:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            # Dimension 3
            elif dim == 3:
                # Si il n'y a pas assez de volume dans le container pour l'item n'essaye meme pas de l'insérer
                if (containers[j].volume - containers[j].used_volume) >= item.volume:
                    inserted = containers[j].add_item(item)
                    if inserted:
                        keep_going = False
            j += 1
    return containers
