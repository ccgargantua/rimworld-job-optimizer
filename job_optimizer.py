import json
import pygad as pg
import numpy as np

# TODO milestones
#     TODO Finish fitness function
#         [x] Account for skills in calculations
#         [ ] Account for traits in calculations
#         [ ] Account for colonist value
#     TODO Read colonist data from .rws save files
#     TODO Retrieve .rws save files from game directory
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

MAX_SKILL_LEVEL = 20

gene_space = [list(range(5))] * NUM_JOBS * NUM_COLONISTS

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
def reshape_solution(solution : np.array) -> np.array:
    return solution.reshape((NUM_COLONISTS, NUM_JOBS))

# This will calculate how proficient a colonist is at a job,
# if they are even able to do said job.
# RETURNS
#   * Higher return value indicates a higher proficiency.
#   * -1 indicates that the colonist is unable or unwilling to
#     do the job
def calculate_proficiency(colonist : dict, job : dict) -> np.int32:

    # Check if two lists contain any of the same elements
    # Unnecessary now but might be used in the future when other
    # factors are considered TODO <-
    def contain_same(list_1, list_2):
        if list_1 == None or list_2 == None:
            return False
        return len(set(list_1) & set(list_2)) > 0
    
    # Check if colonist is incapable of doing the job
    if contain_same(colonist['incapable_of'], job['category']):
        return -1
    
    proficiency = 0
    can_do = False # TODO ugly. find a better way to do this later
    if job['skills'] == None:
        return MAX_SKILL_LEVEL
    for skill in job['skills']:
        
        if skill == None:
            proficiency += MAX_SKILL_LEVEL // 2
            can_do = True
            continue
        # Another check if colonist is incapable of doing the job.
        # Kind of have to do it this way because of how rimworld
        # marks colonists as incapable in two different ways...
        if colonist[skill] == None:
            continue
        can_do = True
        proficiency += colonist[skill]
    return proficiency if can_do else -1

# Calculate the fitness of a solution
# TODO finish
def fitness_function(ga_instance : pg.GA, solution : np.array, solution_idx : np.int64) -> float:

    solution_array = reshape_solution(solution)
    penalty = 0
    reward = 0
    job_bias = [0] * NUM_JOBS

    for colonist_idx, colonist_assignments in enumerate(solution_array):
        colonist = colonists[colonist_idx]
        for job_idx, job_priority in enumerate(colonist_assignments):
            job = jobs[job_idx]
            proficiency = calculate_proficiency(colonist, job)
            if job_priority == 0:
                # Penalize for not prioritizing jobs that a colonist has the skills for
                if proficiency > -1:
                    penalty += proficiency
                # Reward for not assigning colonists to jobs they can't do
                else:
                    reward += 10
            else:
                # Penalize assigning colonists to jobs that they can't or just barely can do
                if proficiency <= 3:
                    penalty += 10
                # Reward for assigning colonists to jobs they are capable of doing
                else:
                    reward += proficiency

    try:
        return reward / penalty
    except ZeroDivisionError:
        return 10000 # **Probably** will never get here

def on_generation(ga_instance : pg.GA):
    print(f'Generation {ga_instance.generations_completed} completed. Best fitness: {ga_instance.best_solution()[1]}')

def print_results(ga_instance : pg.GA):
    solution, fitness, idx = ga_instance.best_solution()

    for colonist_idx, colonist_priorities in enumerate(reshape_solution(solution)):
        print(f"Name:\n  {colonists[colonist_idx]['name']}")

        # print stats
        print("Stats:")
        for k in colonists[colonist_idx].keys():
            if k == 'name':
                continue
            print(f'  {k}: {colonists[colonist_idx][k]}')

        # print job priorities
        print("Job Priority:")
        for job_idx, job in enumerate(jobs):
            print(f"  {job['name']}: {colonist_priorities[job_idx]}")

    print(f'Best Fitness: {fitness}')
    ga_instance.plot_fitness()


if __name__ == '__main__':

    # TODO remove hard-coded values
    ga_instance = pg.GA(num_generations=1000,
                       num_parents_mating=20,
                       fitness_func=fitness_function,
                       sol_per_pop=300,
                       num_genes=len(gene_space),
                       gene_type=int,
                       gene_space=gene_space,
                       parent_selection_type='sss',
                       keep_parents=4,
                       crossover_type='scattered',
                       mutation_type='swap',
                       mutation_percent_genes=10,
                       on_generation=on_generation,
                       stop_criteria='saturate_20')
    ga_instance.run()
    print_results(ga_instance)