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
    def __init__(self, length: int = LENGTH, width: int = WIDTH, height: int = HEIGHT, dimension=3, next=None):
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height

        self.items = SortedLinkedList(DIM[dimension])
        self.used_length = 0
        self.used_width = 0
        self.used_height = 0

    def __str__(self):
        return f'({self.length} m * {self.width} m * {self.height} m)'


class Item:
    def __init__(self, name: str, length: int, width: int, height: int):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.area = length * width
        self.volume = length * width * height


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
                containers[j].items.insert_sorted(item)
                containers[j].used_length += item.length
                del items[0]
                keep = False

            elif (containers[j].length - containers[j].used_length) >= item.length:
                containers[j].items.insert_sorted(item)
                containers[j].used_length += item.length
                del items[0]
                keep = False
            else:
                for item_to_replace in containers[j].items:
                    if containers[j].used_length - item_to_replace.length + item.length <= containers[
                        j].length and item_to_replace.length < item.length:
                        containers[j].used_length = containers[j].used_length - item_to_replace.length + item.length
                        containers[j].items.remove(item_to_replace)
                        containers[j].items.insert_sorted(item)
                        del items[0]
                        items.insert(0, item_to_replace)
                        keep = False
                        break
            j += 1
        if containers[i].used_length == containers[i].length:
            i += 1

    return containers


def read_csv(filename):
    item_list = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                number, name, length, width, height = line.strip().split(';')
                item = Item(name, int(float(length) * 1000), int(float(width) * 1000), int(float(height) * 1000))
                item_list.append(item)
    except FileNotFoundError:
        print(f'File {filename} not found')

    return item_list


if __name__ == '__main__':

    items = read_csv('Données_marchandises_2324.csv')
    result = d1(items)
    print(len(result))
    c = 0
    for container in result:
        for item in container.items:
            c += 1
    print(c)
