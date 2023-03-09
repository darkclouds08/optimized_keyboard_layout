from random import shuffle
import random as rand
import numpy as np 
import time

ALPHABET = list('qwertyuiopasdfghjkl;zxcvbnm,./')
COST = np.array([
    [1.6, 1.3, 1.3, 1.4, 1.3, 1.7, 1.3, 1.3, 1.3, 1.3],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [1.6, 1.5, 1.5, 1.3, 1.9, 1.3, 1.3, 1.4, 1.5,1.5],
])

def construct_lookup_table(layout):
    '''
    returns a dict with key as letter, value as cost of that letter
    '''
    table = dict()
    for i in range(3):
        for j in range(10):
            table[layout[i][j]] = COST[i][j]
    return table

def mutate(layout):
    '''
    randomly chooses 2 keys to be swapped in a same row
    '''
    row_val = rand.randint(0,2)
    col_val1 = rand.randint(0,9)
    col_val2 = rand.randint(0,9)
    layout[row_val][col_val1], layout[row_val][col_val2] = layout[row_val][col_val2], layout[row_val][col_val1]

    return layout

def get_cost(word, table):
    '''
    word => 'word'
    construct_lookup_table()
    for letter in word:
        row, col = find_row_col(letter)
        compute_cost(row, col)
    '''
    cost = 0
    for i in range(len(word)):
        if i > 0 and word[i-1] == word[i]:
            continue
        cost += table[word[i]]
    return cost
        
def merge(mom, dad, mom_threshold=0.5, mutation_rate=0.05):
    '''

    qwertyuiop
    asdfghjkl;
    zxcvbnm,./

        +

    /,.pyfgcrl
    aoeuidhtsn
    ;qjkxbmwvz

        =
        
    intermediate:

    qwert___l
    asdfg_h__n
    zxcvb_m___

        =

    qwert/,.pl
    asdfgyhoun
    zxcvbim;jk

    top -> bottom  -> middle
    bottom -> top -> middle
    middle -> top -> bottom
    
    '''

    used = set()

    child = [list('_' * 10) for _ in range(3)]

    if rand.randint(0, 1) == 0:
        mom, dad = dad, mom
    # fill with left
    for i in range(3):
        for j in range(5):
            child[i][j] = mom[i][j]
            used.add(mom[i][j])

    # fill right
    for i in range(3):
        for j in range(5, 10):
            char = dad[i][j]
            if char not in used:
                used.add(char)
                child[i][j] = char

    def find_unused_char(layout):
        for row in layout:
            for letter in row:
                if letter not in used:
                    return letter
        # unreachable code
        assert False

    
    # fill missing
    for i in range(3):
        for j in range(5, 10):
            # gene missing
            if child[i][j] == '_':
                char = find_unused_char(dad)
                child[i][j] = char
                used.add(char)

    if rand.random() < mutation_rate:
        child = mutate(child)
    return child

def load():
    words, cleaned_words = [], []
    with open('./worddata copy.txt','r') as f:
        words = f.readlines()
        for i in words:
            # [\n\t\r ]
            cleaned_words.append(i.strip())
    return cleaned_words

def keyboard_layout(): 
    keys = ALPHABET
    shuffle(keys)
    return [keys[:10], keys[10:20], keys[20:]]

def get_total_cost(layout, data):
    table = construct_lookup_table(layout)
    cost = 0
    for word in data:
        cost += get_cost(word, table)
    return cost

def main():
    data = load()
    POPULATION_SIZE = 100
    GENERATIONS = 1

    population = [keyboard_layout() for _ in range(POPULATION_SIZE)]
    POPULATION_HISTORY = []

    TOP_N = 10 
    
    for gen in range(GENERATIONS):
        POPULATION_HISTORY.append(population)
        score_and_layout = [(get_total_cost(layout, data), layout) for layout in population]
        score_and_layout.sort(key=lambda x: x[0])

        new_generation = list(map(lambda x: x[1], score_and_layout))[:TOP_N]

        for count in range(POPULATION_SIZE - TOP_N):
            mom = population[rand.randrange(0, len(population))]
            dad = population[rand.randrange(0, len(population))]
            new_generation.append(merge(mom, dad))

        # for i in range(TOP_N):
        #     for j in range(TOP_N):
        #         if i == j:
        #             continue
        #         mom = population[i]
        #         dad = population[j]
        #         child = merge(mom, dad)
        #         if rand.random() < MUTATION_RATE:
        #             child = mutation(child)
        #         new_generation.append(child)

        # shuffle(new_generation)
        

        population = new_generation

        gen_avg_cost = sum(map(lambda x: x[0], score_and_layout)) / len(score_and_layout)
        print(f'Avg score in generation {gen + 1}: {gen_avg_cost}')
        print(f'Best score in generation {gen + 1}: {score_and_layout[0][0]}')
        if gen == 999:
            print(f'Best keyboard layout {score_and_layout[0][1]}')








    qwerty = [list('qwertyuiop'), list('asdfghjkl;'), list('zxcvbnm,./')]
    # dvorak = [list('/,.pyfgcrl'), list('aoeuidhtns'),  list(';qjkxbmwvz')]
    # colemak = [list('qwfpgjluy;'),list('arstdhneio'),list('zxcvbkm,./')]
    qwerty_score = get_total_cost(qwerty,data)
    # dvorak_score = get_total_cost(dvorak,data)
    # colemak_score = get_total_cost(colemak,data)
    print(qwerty_score)
    # print(dvorak_score)
    # print(colemak_score)
    '''
        for i in range(10):
            POPULATION = [keyboard_layout() for _ in range(POPULATION_SIZE)]
            print(f'Simulation {i}')
            print('MOM')
            mom = POPULATION[0]
            mom_score = get_total_cost(mom, data)
            print(mom)
            print(f'Cost: {mom_score}')
            print('DAD')
            dad = POPULATION[1]
            dad_score = get_total_cost(dad, data)
            print(dad)
            print(f'Cost: {dad_score}')

            print('\nCHILD\n')
            child = merge(POPULATION[0], POPULATION[1])
            child_score = get_total_cost(child, data)
            print(child)
            print(f'Cost: {child_score}')

            if abs(child_score - mom_score) < abs(child_score - dad_score):
                print("Mom's child")
            else:
                print("Dad's child")
            print()
            print()
            print()
            print()
            print()
            '''


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f'Runtime: {end_time - start_time} seconds')


# asdfghjkl;
# 0000110000

# redirection
# ./application > file.txt
# python -u "c:\mahadasdf\Genetic "