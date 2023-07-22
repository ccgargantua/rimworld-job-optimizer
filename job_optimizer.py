import json
import pygad as pg
import numpy as np

##########
# CONFIG #
##########

COLONY_DATA_FILENAME = 'test_colony.json'

##############
# END CONFIG #
##############

#############
# CONSTANTS #
#############

# TODO maybe put in a json or something later
jobs = [
    {'name': 'firefight', 'skills': None,                                          'category': None},
    {'name': 'patient',   'skills': None,                                          'category': None},
    {'name': 'doctor',    'skills': ['medical'],                                   'category': ['caring', 'social']},
    {'name': 'bed_rest',  'skills': None,                                          'category': None},
    {'name': 'basic',     'skills': None,                                          'category': None},
    {'name': 'warden',    'skills': ['social'],                                    'category': None},
    {'name': 'handle',    'skills': ['animals'],                                   'category': ['animals']},
    {'name': 'cook',      'skills': ['cooking'],                                   'category': ['skilled_labor']},
    {'name': 'hunt',      'skills': ['shooting', 'animals'],                       'category': ['violent']},
    {'name': 'construct', 'skills': ['construction'],                              'category': ['skilled_labor']},
    {'name': 'grow',      'skills': ['plants'],                                    'category': ['skilled_labor']},
    {'name': 'plant_cut', 'skills': ['plants'],                                    'category': ['dumb_labor']},
    {'name': 'mine',      'skills': ['mining'],                                    'category': ['skilled_labor']},
    {'name': 'smith',     'skills': ['crafting'],                                  'category': ['skilled_labor']},
    {'name': 'tailor',    'skills': ['crafting'],                                  'category': ['skilled_labor']},
    {'name': 'art',       'skills': ['artistic'],                                  'category': 'artistic'},
    {'name': 'craft',     'skills': ['crafting', 'cooking', 'intellectual', None], 'category': ['skilled_labor', 'intellectual']},
    {'name': 'haul',      'skills': None,                                          'category': 'dumb_labor'},
    {'name': 'clean',     'skills': None,                                          'category': 'dumb_labor'},
    {'name': 'research',  'skills': ['intellectual'],                              'category': ['intellectual']}
]

#################
# END CONSTANTS #
#################


def get_colony_data():
    with open(COLONY_DATA_FILENAME, 'r') as file:
        data = json.load(file)
    return data

def fitness_function(ga_instance, solution, solution_idx):
    penalty = 0



    try:
        return 1 / penalty
    except ZeroDivisionError:
        return np.inf

def print_results(ga_instance):
    pass

if __name__ == '__main__':
    colonists = get_colony_data()['colonists']
    gene_space = [list(range(5)) * 20] * len(colonists)
    ga_instance = pg.GA(num_generations=1000,
                       num_parents_mating=20,
                       fitness_func=fitness_function,
                       sol_per_pop=300,
                       num_genes=len(gene_space),
                       gene_type=int,
                       parent_selection_type='sss',
                       keep_parents=4,
                       crossover_type='scattered',
                       mutation_type='swap',
                       mutation_percent_genes=10)
    ga_instance.run()
    print_results(ga_instance)