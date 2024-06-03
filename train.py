class Item:
    def __init__(self, id: int, name: str, length: int, width: int, height: int):
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.volume = length * width * height

    def __str__(self):
        return f'{self.name} ({self.length} x {self.width} x {self.height})'


def classItem(items: [Item], d):
    if d == 1:
        return one_dimension(items)
    elif d == 2:
        return two_dimension(items)


def one_dimension(items: [Item]):
    res = 0
    for i in items:
        res += i.length
    return res


def two_dimension(items: [Item]):
    res = 0
    for i in items:
        res += i.length * i.width
    return res
