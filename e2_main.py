import time
import colored

# Dimensions des containers en decimètres
LENGTH = int(115.83)
WIDTH = int(22.94)
HEIGHT = int(25.69)

DIM = {
    1: 'length',
    2: 'area',
    3: 'volume',
}


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
            self.map = [0 for _ in range(self.length)]
        elif dimension == 2:
            self.map = [[0 for _ in range(self.width)] for _ in range(self.length)]
        elif dimension == 3:
            self.map = [[[0 for _ in range(self.height)] for _ in range(self.width)] for _ in range(self.length)]

    def __str__(self):
        return f'({self.length} m * {self.width} m * {self.height} m)'

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
            for y in range(j, j + item.length):
                for x in range(i, i + item.width):
                    for z in range(k, k + item.height):
                        if self.map[y][x][z] != 0:
                            return False
            return True

    def fill_item(self, item):
        if self.dim == 1:
            for j in range(self.length - item.length + 1):
                if self.map[j] == 0:
                    if self.check_enough_space(item, j=j):
                        for y in range(item.length):
                            self.map[y + j] = item.id
                        return True
            return False
        if self.dim == 2:
            for j in range(self.length - item.length + 1):
                for i in range(self.width - item.width + 1):
                    if self.map[j][i] == 0:
                        if self.check_enough_space(item, i, j):
                            for y in range(item.length):
                                for x in range(item.width):
                                    self.map[y + j][x + i] = item.id
                            return True
            return False
        if self.dim == 3:
            for j in range(self.length - item.length + 1):
                for i in range(self.width - item.width + 1):
                    for k in range(self.height - item.height + 1):
                        if self.map[j][i][k] == 0:
                            if self.check_enough_space(item, i, j, k):
                                for y in range(j, j + item.length):
                                    for x in range(i, i + item.width):
                                        for z in range(k, k + item.height):
                                            self.map[y][x][z] = item.id
                                return True
            return False


    def add_item_1D(self, item):
        if self.fill_item(item):
            self.items.append(item)
            self.used_length += item.length
            return True
        return False

    def add_item_2D(self, item):
        if self.fill_item(item):
            self.items.append(item)
            self.used_area += item.area
            return True
        return False

    def add_item_3D(self, item):
        if self.fill_item(item):
            self.items.append(item)
            self.used_volume += item.volume
            return True
        return False

    def add_item(self, item):
        if self.dim == 1:
            return self.add_item_1D(item)
        if self.dim == 2:
            return self.add_item_2D(item)
        if self.dim == 3:
            return self.add_item_3D(item)
        return False

    def print_map(self):
        cell_width = 3  # Fixed width for each cell
        for row in self.map:
            print('| ', end='')
            for col in row:
                if col != 0:
                    color = colored.fg(col % 256)
                    print(colored.stylize(f'{col:>{cell_width}}', color), end='')
                else:
                    print('_', end='')
            print(' |')


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


def d(items: [Item], dim: int = 3, offline: bool = False) -> [Item]:
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


def get_non_used_volume(container: Container):
    if container.dim == 1:
        res = 0
        for i in container.map:
            if i == 0:
                res += 1
        return res
    if container.dim == 2:
        res = 0
        for i in container.map:
            for j in i:
                if j == 0:
                    res += 1
        return res
    if container.dim == 3:
        res = 0
        for i in container.map:
            for j in i:
                for k in j:
                    if k == 0:
                        res += 1
        return res


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
            non_occupee = sum(get_non_used_volume(c) for c in resultArray[i][d][0])
            temps_calcul = resultArray[i][d][1]

            table.append([dim, nombre_wagons, non_occupee, temps_calcul])

        for row in table:
            print("{:<10} {:<15} {:<25} {:<15}".format(*row))

        print()


def print_containers(containers):
    nb_rows = LENGTH
    cell_width = 3  # Fixed width for each cell
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


if __name__ == '__main__':
    items = Item.list_from_csv('Données_marchandises_2324.csv')

    # result[0].print_map()

    # print_containers(result)

    # start = time.time()
    # result = d(items, dim=2, offline=True)
    # result = d2_with_map_offline(items)
    # print(time.time() - start)
    # print(len(result))
    # c = 0
    # for container in result:
    #     for item in container.items:
    #         c += 1
    # print(c)

    resultArray = [[], []]

    for i in range(3):
        start_time = time.time()
        resultArray[0].append([d(items, dim=i + 1, offline=False)])
        resultArray[0][i].append(time.time() - start_time)

        start_time = time.time()
        resultArray[1].append([d(items, dim=i + 1, offline=True)])
        resultArray[1][i].append(time.time() - start_time)

    print_as_a_table(resultArray)