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

    # Calcule des performance de l'algorithme
    resultArrays = [[], []]
    for w in range(3):
        start_time = time.time()
        resultArrays[0].append([d(items, dim=w + 1, offline=False)])
        resultArrays[0][w].append(time.time() - start_time)

        start_time = time.time()
        resultArrays[1].append([d(items, dim=w + 1, offline=True)])
        resultArrays[1][w].append(time.time() - start_time)
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
