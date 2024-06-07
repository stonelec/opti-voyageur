import time
from  container import print_containers, Item, print_as_a_table, d, init_interactive
import tkinter


# Programme de test
if __name__ == '__main__':
    # CSV des items
    items = Item.list_from_csv('Données_marchandises_2324.csv')
    # Activation de la fenêtre tkinter (graphique)
    INTERACTIVE_MODE = False
    # Affiche dans la console la map des containers
    CONSOLE_MODE = False
    # Test mode
    TEST_MODE = True

    if TEST_MODE:
        # Calcule des performance de l'algorithme
        resultArrays = [[], []]
        nb_test = 5
        for w in range(1, 4):
            t_moy = 0
            for p in range(nb_test):
                start_time = time.time_ns()
                d(items, dim=w, offline=False)
                end_time = time.time_ns()
                t_moy += end_time-start_time
            t_moy /= nb_test
            resultArrays[0].append([d(items, dim=w, offline=False)])
            resultArrays[0][w-1].append(t_moy/1000000000)

            t_moy = 0
            for p in range(nb_test):
                start_time = time.time_ns()
                d(items, dim=w, offline=True)
                end_time = time.time_ns()
                t_moy += end_time-start_time
            t_moy /= nb_test
            resultArrays[1].append([d(items, dim=w, offline=True)])
            resultArrays[1][w-1].append(t_moy/1000000000)
        # Affichage des performance de l'algorithme
        print_as_a_table(resultArrays)

    # Containers à afficher selon les modes sélectionnés précédement
    result = d(items, dim=3, offline=False)
    if CONSOLE_MODE:
        print_containers(result)
    if INTERACTIVE_MODE:
        init_interactive()
        result[0].render(result)
        tkinter.mainloop()
