# Dimensions des containers en millimètres
LENGTH = 11583
WIDTH = 2294
HEIGHT = 2569

DIM = {
    1: 'length',
    2: 'area',
    3: 'volume',
}


class Container:
    def __init__(self, length: int=LENGTH, width: int=WIDTH, height: int=HEIGHT, dimension=3, next=None):
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height

        self.items = SortedLinkedList(DIM[dimension])
        self.used_length = 0
        self.used_area = 0

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
        self.map = [[0 for j in range(int(WIDTH//100))] for i in range(int(LENGTH//100))]
        self.items = []

    def add_item(self, item):
        id = len(self.items)+1
        stop = False
        for j in range(int(LENGTH//100) - int(item.length//100) + 1):
            for i in range(int(WIDTH//100) - int(item.width//100) + 1):
                if self.map[j][i] == 0:
                    is_ok = True
                    for y in range(item.length//100):
                        for x in range(item.width//100):
                            if self.map[y+j][x+i] != 0:
                                is_ok = False
                                break
                    if is_ok:
                        for y in range(item.length // 100):
                            for x in range(item.width // 100):
                                self.map[y+j][x+i] = id
                        stop = True
                if stop:
                    break
            if stop:
                break
        if stop:
            item.id = id
            self.items.append(item)
            self.used_area += item.area
            return True
        return False

    def print_map(self):
        for row in self.map:
            print('| ', end='')
            for col in row:
                if col != 0:
                    print(col, end='')
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
                    item = Item(int(number), name, int(float(length)*1000), int(float(width)*1000), int(float(height)*1000))
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
                    if containers[j].used_length - item_to_replace.length + item.length <= containers[j].length and item_to_replace.length < item.length:
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


def d2_2(items: [Item]) -> [Item]:
    containers = []
    #items = sorted(items, reverse=True, key=lambda x: x.area)
    for item in items:
        j = 0
        keep = True
        while keep:
            if len(containers) == j:
                containers.append(Container2(dimension=2))
                inserted = containers[j].add_item(item)
                if inserted:
                    keep = False

            elif (containers[j].area - containers[j].used_area) >= item.area:
                inserted = containers[j].add_item(item)
                if inserted:
                    keep = False
            j += 1
    return containers


if __name__ == '__main__':
    def read_csv(filename):
        item_list = []
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    number, name, length, width, height = line.strip().split(';')
                    item = Item(int(number), name, int(float(length)*1000), int(float(width)*1000), int(float(height)*1000))
                    item_list.append(item)
        except FileNotFoundError:
            print(f'File {filename} not found')

        return item_list

    items = read_csv('Données_marchandises_2324.csv')
    result = d2_2(items)
    print(len(result))
    c = 0
    for container in result:
        for item in container.items:
            c += 1
    print(c)

    #result[0].print_map()

    def print_containers(containers):
        nb_rows = LENGTH // 100
        for i in range(nb_rows):
            for container in containers:
                row = container.map[i]
                print('| ', end='')
                for col in row:
                    if col != 0:
                        print(col, end='')
                    else:
                        print('_', end='')
                print(' |   ', end='')
            print()
    print_containers(result)
