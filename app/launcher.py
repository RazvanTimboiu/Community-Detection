from utilitary import *
from population import *
import keyboard
import pickle
import os

# 'idx': 'path_to_dataset'
datasets = {
    '0': "\\datasets\\demo.gml",
    '1': "\\datasets\\karate.gml",
    '2': "\\datasets\\dolphins.gml",
    '3': "\\datasets\\football.gml",
    '4': "\\datasets\\books.gml",
    '5': "\\datasets\\words.gml"
}

# 'idx': 'path_to_best_network_config_drawing'
drawings = {
    '0': "\\drawings\\demo.png",
    '1': "\\drawings\\karate.png",
    '2': "\\drawings\\dolphins.png",
    '3': "\\drawings\\football.png",
    '4': "\\drawings\\books.png",
    '5': "\\drawings\\words.png"
}

# 'idx': 'filepath', 'best_fitness', 'network_configuration'
results = {
    '0': ["\\results\\demo.pickle", 0.0, []],
    '1': ["\\results\\karate.pickle", 0.0, []],
    '2': ["\\results\\dolphins.pickle", 0.0, []],
    '3': ["\\results\\football.pickle", 0.0, []],
    '4': ["\\results\\books.pickle", 0.0, []],
    '5': ["\\results\\words.pickle", 0.0, []]
}


def get_baseline():
    for key in results:
        with open(os.getcwd() + results[key][0], 'rb') as handle:
            results[key] = pickle.load(handle)


def update_baseline():
    for key in results:
        with open(os.getcwd() + results[key][0], 'wb') as handle:
            pickle.dump(results[key], handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_options():
    options = {'population_size': int(input("\n Population size : ")),
               'number_of_generations': int(input("\n Number of generations : ")),
               'mutation_rate': int(input("\n Mutation rate (in %) : ")),
               'number_of_biased_nodes': int(input("\n Number of biased nodes : "))}
    return options


def search(filename):
    """
    Function to search for the optimal community configuration in a given network.
    :param filename ~ Name of the file which contains the network (GML format).
    :return best configuration found and network details.
    """

    network = read_network_from_gml(os.path.join(os.getcwd(), filename))
    options = get_options()

    population = Population()
    population.initialize(options, network)
    population.evaluate(modularity, network)

    global_best = population.get_fittest_chromosome()

    best_fits = []
    avg_fits = []

    print("\n Starting search, feel free to press 'c' to stop early if results do not improve for a long time! \n")

    for current_generation in range(options['number_of_generations']):

        # population.iterate_one_generation_standard(modularity, network, options)
        # population.iterate_one_generation_elitism(modularity, network, options)
        population.iterate_one_generation_steady_state(modularity, network, options)

        if keyboard.is_pressed("c"):
            break

        avg_fitness = sum([c.fitness for c in population.population]) / len(population.population)
        avg_fits.append(avg_fitness)

        local_best = population.get_fittest_chromosome()
        best_fits.append(local_best.fitness)

        print("############## Gen: " + str(current_generation + 1) + " #################")
        print('    Average fit = ' + str(avg_fitness))
        print('Local  Best fit = ' + str(local_best.fitness))
        print('Global Best fit = ' + str(global_best.fitness))
        print(' Number of communities (G) = ' + str(global_best.get_community_count()) + '\n')

        if local_best > global_best:
            global_best = local_best
            draw_configuration_layout(global_best.genes, network, 2, False)

    # Evolution of best fitness.
    plot_evolution_over_time(best_fits, 'Best Fitness')

    # Evolution of average fitness.
    plot_evolution_over_time(avg_fits, 'Average Fitness')

    print("Drawing best configuration found...")
    draw_configuration_layout(global_best.genes, network, 1, True)

    return global_best, network


def run():
    get_baseline()

    while True:

        print(""" \n\n Choose the dataset you want to work on or press 'q' to save results and quit :
                  \t 0. Demo 
                  \t 1. Karate
                  \t 2. Dolphins
                  \t 3. Football
                  \t 4. Books
                  \t 5. Words """)

        choice = input()
        if choice == 'q':
            print('Closing App !')
            break
        else:
            try:
                int(choice)
            except ValueError:
                print("Please enter an integer !")

        best, network = search(os.getcwd() + datasets[choice])

        if results[choice][1] < best.fitness:
            print('\n You found a better configuration ! \n')
            results[choice][1], results[choice][2] = best.fitness, best.genes

            print("Saving graphic representation ...")
            save_network_configuration(os.getcwd() + drawings[choice], best.genes, network)

    update_baseline()


run()
