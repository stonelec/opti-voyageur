import item
import time


def main():
    item_list = item.read_csv('velo.csv')

    C = [0.6, 0.8, 1, 1.5, 2, 3, 4, 5, 6]

    print("Running exact algorithm")

    for i in C:
        print("Running algo for C = ", i)

        total_mass, total_utility, best_item = item.exact(item_list, i)

        print("     ", "total mass : ", total_mass / 100, "total utility : ", total_utility / 100, "\n")
        for i in best_item:
            print("     ", i)

        time_moy = 0
        n = 4
        for i in range(n):
            start = time.time()
            item.exact(item_list, i)
            time_moy += time.time() - start

        print("     ", time_moy / n, "\n")

    print("Heuristic 2 algorithm")

    for i in C:
        print("Running algo for C = ", i)

        total_mass, total_utility, best_item = item.heuristic_1(item_list, i)

        print("     ", "total mass : ", total_mass / 100, "total utility : ", total_utility / 100, "\n")
        for i in best_item:
            print("     ", i)

        time_moy = 0
        n = 1000
        for i in range(n):
            start = time.time()
            item.heuristic_1(item_list, i)
            time_moy += time.time() - start

        print("     ", time_moy / n, "\n")

    print("Heuristic 2 algorithm")

    for i in C:
        print("Running algo for C = ", i)

        total_mass, total_utility, best_item = item.heuristic_2(item_list, i)

        print("     ", "total mass : ", total_mass / 100, "total utility : ", total_utility / 100, "\n")
        for i in best_item:
            print("     ", i)

        time_moy = 0
        n = 1000
        for i in range(n):
            start = time.time()
            item.heuristic_2(item_list, i)
            time_moy += time.time() - start

        print("     ", time_moy / n, "\n")


if __name__ == '__main__':
    main()
