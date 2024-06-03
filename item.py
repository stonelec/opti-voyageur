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


def exact_recu(items, C, k, best_mass, best_utility, best_items):
    current_best_utility = best_utility
    current_best_mass = best_mass
    current_best_items = best_items[:]

    for i in range(k, len(items)):
        if items[i].mass <= C:
            new_mass = best_mass + items[i].mass
            new_utility = best_utility + items[i].utility
            if new_utility > current_best_utility:
                current_best_utility = new_utility
                current_best_mass = new_mass
                current_best_items = best_items[:] + [items[i]]
            recu_utility, recu_mass, recu_items = exact_recu(items, C - items[i].mass, i + 1, new_mass, new_utility,
                                                             best_items + [items[i]])
            if recu_utility > current_best_utility:
                current_best_utility = recu_utility
                current_best_mass = recu_mass
                current_best_items = recu_items

    return current_best_utility, current_best_mass, current_best_items


def exact(items, C):
    C = int(C * 100)
    best_items = []
    best_utility, best_mass, best_items = exact_recu(items, C, 0, 0, 0, best_items)
    return best_mass, best_utility, best_items


def heuristic_1(items: [Item], C: float) -> [int, int, SortedLinkedList]:
    total_mass = 0
    total_utility = 0
    best_item = SortedLinkedList()
    items.sort(reverse=True, key=lambda x: x.factor)
    for i in items:
        if total_mass + i.mass <= C * 100:
            total_mass += i.mass
            total_utility += i.utility
            best_item.insert_sorted(i)
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
    total_mass = 0
    total_utility = 0
    best_item = SortedLinkedList()
    items.sort(reverse=True, key=lambda x: x.factor)
    for i in items:
        if total_mass + i.mass <= C * 100:
            total_mass += i.mass
            total_utility += i.utility
            best_item.insert_sorted(i)

    return total_mass, total_utility, best_item
