class Item:
    def __init__(self, name: str, mass: float, utility: float, next=None):
        self.name = name
        self.mass = int(mass * 100)
        self.utility = int(utility * 100)
        self.factor = round(utility / mass, 3)
        self.next = next

    def __str__(self):
        return f'{self.name} ({self.mass / 100} kg, {self.utility / 100} utils, factor of {self.factor})'

    def __lt__(self, other):
        return self.factor < other.factor

    def __le__(self, other):
        return self.factor <= other.factor

    def __gt__(self, other):
        return self.factor > other.factor

    def __ge__(self, other):
        return self.factor >= other.factor


class SortedLinkedList:
    def __init__(self):
        self.head = None

    def insert_sorted(self, data):
        """
        Insert an item in the list, keeping it sorted
        :param data: Item to insert
        :return: None
        """
        new_node = data
        if self.head is None or self.head.mass > data.mass:
            new_node.next = self.head
            self.head = new_node
            return
        current = self.head
        while current.next and current.next.mass <= data.mass:
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def remove(self, data):
        """
        Remove an item from the list
        :param data: Item to remove
        :return: None
        """
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
        """
        Return the iterator
        :return: Iterator
        """
        self._current = self.head
        return self

    def __next__(self):
        """
        Return the next item in the list
        :return: Item
        """
        if self._current is None:
            raise StopIteration
        else:
            data = self._current
            self._current = self._current.next
            return data

    def print_list(self):
        """
        Print the list
        """
        current = self.head
        while current:
            print(current)
            current = current.next

    def to_array(self):
        """
        Return a list of the items in the list
        :return: [Item]
        """
        array = []
        current = self.head
        while current:
            array.append(current.data)
            current = current.next
        return array

    def __str__(self):
        """
        Return a string representation of the list
        :return: str
        """
        return str(self.to_array())


def exact_recursion(items: [Item], C: float, k: int, best_mass: int, best_utility: int, best_items: [Item]) -> [int, int, [Item]]:
    """
    Recursive function for the exact algorithm
    :param items: List of items
    :param C: Capacity
    :param k: Index of the item to check
    :param best_mass: Best mass found
    :param best_utility: Best utility found
    :param best_items: Best items found
    :return: Best mass, best utility, best items
    """
    current_best_utility = best_utility
    current_best_mass = best_mass
    current_best_items = best_items[:]

    # Check if we can add an item that the program didn't check yet
    for i in range(k, len(items)):
        if items[i].mass <= C:
            new_mass = best_mass + items[i].mass
            new_utility = best_utility + items[i].utility
            if new_utility > current_best_utility:
                current_best_utility = new_utility
                current_best_mass = new_mass
                current_best_items = best_items[:] + [items[i]]

            recu_utility, recu_mass, recu_items = exact_recursion(items, C - items[i].mass, i + 1, new_mass,
                                                                  new_utility,
                                                                  best_items + [items[i]])
            if recu_utility > current_best_utility:
                current_best_utility = recu_utility
                current_best_mass = recu_mass
                current_best_items = recu_items

    return current_best_utility, current_best_mass, current_best_items


def exact(items: [Item], C: float) -> [int, int, [Item]]:
    """
    Exact algorithm, it will try all the possible combinations of items to find the best one
    :param items: List of items
    :param C: Capacity
    :return: Best mass, best utility, best items
    """
    C = int(C * 100)
    best_items = []
    best_utility, best_mass, best_items = exact_recursion(items, C, 0, 0, 0, best_items)
    return best_mass, best_utility, best_items


def heuristic_1(items: [Item], C: float) -> [int, int, SortedLinkedList]:
    """
    Heuristic algorithm, it will try to add the best item it can, if it can't, it will try to swap an item with a better one
    :param items: List of items
    :param C: Capacity
    :return: Best mass, best utility, best items
    """
    total_mass = 0
    total_utility = 0
    best_item = SortedLinkedList()
    items.sort(reverse=True, key=lambda x: x.factor)
    for i in items:
        if total_mass + i.mass <= C * 100:
            total_mass += i.mass
            total_utility += i.utility
            best_item.insert_sorted(i)
            if total_mass == C * 100:
                break
        else:
            for j in best_item:
                if total_mass - j.mass + i.mass <= C * 100 and j.utility < i.utility:
                    total_mass = total_mass - j.mass + i.mass
                    total_utility = total_utility - j.utility + i.utility
                    best_item.remove(j)
                    best_item.insert_sorted(i)
                    break

    return total_mass, total_utility, best_item


def heuristic_2(items: [Item], C: float) -> [int, int, SortedLinkedList]:
    """
    Heuristic algorthm, this one is a bit more efficient than the first one
    It doesn't check if it can swap an item with a better one, it just adds the item if it can
    :param items: List of items
    :param C: Capacity
    :return: Best mass, the best utility, best items
    """
    total_mass = 0
    total_utility = 0
    best_item = SortedLinkedList()
    items.sort(reverse=True, key=lambda x: x.factor)
    for i in items:
        if total_mass + i.mass <= C * 100:
            total_mass += i.mass
            total_utility += i.utility
            best_item.insert_sorted(i)
            if total_mass == C * 100:
                break

    return total_mass, total_utility, best_item


def read_csv(filename):
    """
    Read a csv file and return a list of items
    :param filename: Name of the file
    :return: List of items
    """
    item_list = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, mass, utility = line.strip().split(';')
                item = Item(name, float(mass), float(utility))
                item_list.append(item)
    except FileNotFoundError:
        print(f'File {filename} not found')

    return item_list
