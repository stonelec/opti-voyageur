# Dimensions des containers en millimètres
import time
import colored

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

        self.items = SortedLinkedList(DIM[dimension])
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

    def add_item(self, item):
        self.items.insert_sorted(item)
        self.used_length += item.length

    def remove_item(self, item):
        self.items.remove(item)
        self.used_length -= item.length


class Container2(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

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


class SortedLinkedList:
    def __init__(self, sorting):
        self.head = None
        self.sorting = sorting

    def insert_sorted(self, data):
        new_node = data
        if self.head is None or getattr(self.head, self.sorting) > getattr(data, self.sorting):
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next and getattr(current.next, self.sorting) <= getattr(data, self.sorting):
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def remove(self, data):
        if self.head is None:
            return
        if self.head == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next and current.next != data:
            current = current.next

        if current.next:
            current.next = current.next.next

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            data = self._current
            self._current = self._current.next
            return data

    def print_list(self):
        current = self.head
        while current:
            print(current)
            current = current.next

    def to_array(self):
        array = []
        current = self.head
        while current:
            array.append(current.data)
            current = current.next
        return array

    def __str__(self):
        return str(self.to_array())


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
                containers.append(Container2(dimension=dim))
                inserted = containers[j].add_item(item)
                if inserted:
                    keep_going = False
            elif dim == 1:
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


def d1_with_map_online(items: [Item]):
    containers = []
    for i in items:
        item_added = False
        for j in containers:
            if j.length - j.used_length >= i.length:
                for k in range(j.length - i.length + 1):
                    if check_if_can_add(j, i, k):
                        for l in range(i.length):
                            j.map[k + l] = i.id
                        j.items.insert_sorted(i)
                        j.used_length += i.length
                        item_added = True
                        break
                if item_added:
                    break

        if not item_added:
            containers.append(Container(dimension=1))
            containers[len(containers) - 1].items.insert_sorted(i)
            containers[len(containers) - 1].used_length += i.length
            for l in range(i.length):
                containers[len(containers) - 1].map[l] = i.id

    return containers


def d1_with_map_offline(items: [Item]):
    return d1_with_map_online(sorted(items, reverse=True, key=lambda x: x.length))


def d2_with_map_online(items: [Item]):
    containers = []
    for i in items:
        item_added = False
        for j in containers:
            if j.area - j.used_area >= i.area:
                for k in range(j.length - i.length + 1):
                    for l in range(j.width - i.width + 1):
                        if check_if_can_add(j, i, k, l):
                            for m in range(i.length):
                                for n in range(i.width):
                                    j.map[k + m][l + n] = i.id
                            j.items.insert_sorted(i)
                            j.used_area += i.area
                            item_added = True
                            break
                    if item_added:
                        break
                if item_added:
                    break

        if not item_added:
            containers.append(Container(dimension=2))
            containers[len(containers) - 1].items.insert_sorted(i)
            containers[len(containers) - 1].used_area += i.area
            for l in range(i.length):
                for m in range(i.width):
                    containers[len(containers) - 1].map[l][m] = i.id

    return containers


def d2_with_map_offline(items: [Item]):
    return d2_with_map_online(sorted(items, reverse=True, key=lambda x: x.area))


def d3_with_map_online(items: [Item]):
    containers = []
    for i in items:
        item_added = False
        for j in containers:
            if j.volume - j.used_volume >= i.volume:
                for k in range(j.length - i.length + 1):
                    for l in range(j.width - i.width + 1):
                        for m in range(j.height - i.height + 1):
                            if check_if_can_add(j, i, k, l, m):
                                for n in range(i.length):
                                    for o in range(i.width):
                                        for p in range(i.height):
                                            j.map[k + n][l + o][m + p] = i.id
                                j.items.insert_sorted(i)
                                j.used_volume += i.volume
                                item_added = True
                                break
                        if item_added:
                            break
                    if item_added:
                        break
                if item_added:
                    break

        if not item_added:
            containers.append(Container(dimension=3))
            containers[len(containers) - 1].items.insert_sorted(i)
            containers[len(containers) - 1].used_volume += i.volume
            for l in range(i.length):
                for m in range(i.width):
                    for n in range(i.height):
                        containers[len(containers) - 1].map[l][m][n] = i.id

    return containers


def d3_with_map_offline(items: [Item]):
    return d3_with_map_online(sorted(items, reverse=True, key=lambda x: x.volume))


def check_if_can_add(container: Container, item: Item, x=0, y=0, z=0):
    if container.dim == 1:
        if container.map[x] != 0:
            return False
        for i in range(x, x + item.length):
            if container.map[i] != 0:
                return False
    if container.dim == 2:
        if container.map[x][y] != 0:
            return False
        for i in range(x, x + item.length):
            for j in range(y, y + item.width):
                if container.map[i][j] != 0:
                    return False
    if container.dim == 3:
        if container.map[x][y][z] != 0:
            return False
        for i in range(x, x + item.length):
            for j in range(y, y + item.width):
                for k in range(z, z + item.height):
                    if container.map[i][j][k] != 0:
                        return False
    return True


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
            headers = ["Online", "Nombre wagons", "dimension non occupée", "Temps calcul"]
        else:
            headers = ["Offline", "Nombre wagons", "dimension non occupée", "Temps calcul"]
        table = [headers]

        for d in range(len(resultArray[i])):
            dim = f"d={d + 1}"
            nombre_wagons = len(resultArray[i][d][0])
            non_occupee = sum(get_non_used_volume(c) for c in resultArray[i][d][0])
            temps_calcul = resultArray[i][d][1]

            table.append([dim, nombre_wagons, non_occupee, temps_calcul])

        for row in table:
            print("{:<10} {:<15} {:<20} {:<15}".format(*row))

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


def d_k(items: [Item], dim: int = 3, offline: bool = False):
    if offline:
        if dim == 1:
            return d1_with_map_offline(items)
        if dim == 2:
            return d2_with_map_offline(items)
        if dim == 3:
            return d3_with_map_offline(items)
    else:
        if dim == 1:
            return d1_with_map_online(items)
        if dim == 2:
            return d2_with_map_online(items)
        if dim == 3:
            return d3_with_map_online(items)


if __name__ == '__main__':
    items = Item.list_from_csv('Données_marchandises_2324.csv')

    # result[0].print_map()

    # print_containers(result)

    start = time.time()
    result = d(items, dim=2, offline=True)
    #result = d2_with_map_offline(items)
    print(time.time() - start)
    print(len(result))
    c = 0
    for container in result:
        for item in container.items:
            c += 1
    print(c)

    resultArray = [[], []]

    for i in range(3):
        start_time = time.time()
        resultArray[0].append([d(items, dim=i + 1, offline=False)])
        resultArray[0][i].append(time.time() - start_time)

        start_time = time.time()
        resultArray[1].append([d(items, dim=i + 1, offline=True)])
        resultArray[1][i].append(time.time() - start_time)

    print_as_a_table(resultArray)

    resultArray.clear()

    resultArray = [[], []]

    for i in range(3):
        start_time = time.time()
        resultArray[0].append([d_k(items, dim=i + 1, offline=False)])
        resultArray[0][i].append(time.time() - start_time)

        start_time = time.time()
        resultArray[1].append([d_k(items, dim=i + 1, offline=True)])
        resultArray[1][i].append(time.time() - start_time)

    print_as_a_table(resultArray)

    resultArray = [[], []]

    start_time = time.time()
    resultArray[0].append([d(items, dim=1, offline=False)])
    resultArray[0][0].append(time.time() - start_time)

    start_time = time.time()
    resultArray[0].append([d(items, dim=2, offline=False)])
    resultArray[0][1].append(time.time() - start_time)

    start_time = time.time()
    resultArray[0].append([d(items, dim=3, offline=False)])
    resultArray[0][2].append(time.time() - start_time)

    start_time = time.time()
    resultArray[1].append([d(items, dim=1, offline=True)])
    resultArray[1][0].append(time.time() - start_time)

    start_time = time.time()
    resultArray[1].append([d(items, dim=2, offline=True)])
    resultArray[1][1].append(time.time() - start_time)

    start_time = time.time()
    resultArray[1].append([d(items, dim=3, offline=True)])
    resultArray[1][2].append(time.time() - start_time)

    print_as_a_table(resultArray)
