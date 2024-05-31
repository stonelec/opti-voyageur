from item import Item


def read_csv(filename):
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


def main():
    item_list = read_csv('velo.csv')

    for item in item_list:
        print(item)


if __name__ == '__main__':
    main()
