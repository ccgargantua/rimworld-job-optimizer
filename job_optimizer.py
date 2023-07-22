import json
import pygad as pg
import numpy as np

# TODO milestones
#     TODO Finish fitness function
#     TODO Read colonist data from .rws save files
#     TODO Retrieve .rws save files from game directory
#     TODO Account for traits in calculations
#     TODO Update .rws save file with optimized jobs **BE CAUTIOUS WITH THIS**


# TODO Move configuration to config file
##########
# CONFIG #
##########

# TODO delete or at least change
COLONY_DATA_FILENAME = 'test_colony.json'

##############
# END CONFIG #
##############

# TODO clean this up. It is really bad right now
#############
# CONSTANTS #
#############

# TODO Put in a json later
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
    {'name': 'mine',      'skills': ['mining'],                                    'category': ['skilled_labor']},
    {'name': 'plant_cut', 'skills': ['plants'],                                    'category': ['dumb_labor']},
    {'name': 'smith',     'skills': ['crafting'],                                  'category': ['skilled_labor']},
    {'name': 'tailor',    'skills': ['crafting'],                                  'category': ['skilled_labor']},
    {'name': 'art',       'skills': ['artistic'],                                  'category': 'artistic'},
    {'name': 'craft',     'skills': ['crafting', 'cooking', 'intellectual', None], 'category': ['skilled_labor', 'intellectual']},
    {'name': 'haul',      'skills': None,                                          'category': 'dumb_labor'},
    {'name': 'clean',     'skills': None,                                          'category': 'dumb_labor'},
    {'name': 'research',  'skills': ['intellectual'],                              'category': ['intellectual']}
]

# Gather colonist data from json file
# TODO remove from constants
def get_colony_data():
    with open(COLONY_DATA_FILENAME, 'r') as file:
        data = json.load(file)
    return data
colonists = get_colony_data()['colonists']

NUM_COLONISTS = len(colonists)
NUM_JOBS = len(jobs)

gene_space = list(range(5)) * NUM_JOBS * NUM_COLONISTS

#################
# END CONSTANTS #
#################

# Reshape the solution into a 2D numpy array
#   The number of rows is equal to the number of colonists,
#   and the number of columns is equal to the number of jobs.
#   Each element is the priority level:
#     1 - Highest priority
#     4 - Lowest priority
#     0 - Will not do
def reshape_solution(solution):
    return solution.reshape((NUM_COLONISTS,20))

# This will calculate how proficient a colonist is at a job,
# if they are even able to do said job.
# RETURNS
#   * Higher return value indicates a higher proficiency.
#   * -1 indicates that the colonist is unable or unwilling to
#     do the job
def calculate_proficiency(colonist, job):

    # Check if two lists contain any of the same elements
    def contain_same(list_1, list_2):
        return len(set(list_1) & set(list_2)) > 0
    
    # Check if colonist is incapable of doing the job
    if contain_same(colonist['incapable_of'], job['category']):
        return -1
    
    proficiency = 0
    for skill in job['skills']:
        # Another check if colonist is incapable of doing the job.
        # Kind of have to do it this way because of how rimworld
        # marks colonists as incapable
        if colonist[skill] == None:
            return -1
        proficiency += colonist[skill]
    return proficiency

# Calculate the fitness of a solution
# TODO finish
def fitness_function(ga_instance, solution, solution_idx):

    solution_array = reshape_solution(solution)
    penalty = 0
    reward = 0

    for colonist_idx, colonist_assignments in np.enumerate(solution_array):
        colonist = colonists[colonist_idx]
        for job_idx, job_priority in np.enumerate(colonist):
            job = jobs[job_idx]
            proficiency = calculate_proficiency(colonist, job)
            # TODO continue from here
    try:
        return reward / penalty
    except ZeroDivisionError:
        return np.inf # **Probably** will never get here

def print_results(ga_instance):
    solution, fitness, idx = ga_instance.best_solution()
    for colonist_idx, colonist in solution:
        pass # TODO fill

if __name__ == '__main__':
    
    # TODO remove hard-coded values
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