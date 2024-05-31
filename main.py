from item import Item, exact
import time


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

    C = [0.6, 2, 3, 4, 5]

    for i in C:
        print("Running algo for C = ", i)

        total_mass, total_utility, best_item = exact(item_list, i)

        print("     ", "total mass : ", total_mass / 100, "total utility : ", total_utility / 100, "\n")
        for i in best_item:
            print("     ", i)

        time_moy = 0
        n = 1000
        for i in range(n):
            start = time.time()
            exact(item_list, i)
            time_moy += time.time() - start

        print("     ", time_moy / n, "\n")


if __name__ == '__main__':
    main()
