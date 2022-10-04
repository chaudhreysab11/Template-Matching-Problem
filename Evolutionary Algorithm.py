import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import matplotlib.patches as patches
from numpy.core.numeric import binary_repr
import random

def flip(prob):
    check_flip = np.random.binomial(n=1, p= prob)
    if check_flip==1:
        return True
    else: 
        return False

def show_output(image1,population):
    fig, ax = plt.subplots()
    plt.gray()
    ax.imshow(image1)
    for i in population:
        print(i)
        rect = patches.Rectangle(i, 29, 35, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.show()
    

def initialize_pop(row,column,sizeofPop):
    population = [(np.random.randint(0,row), np.random.randint(0,column)) for _ in range(sizeofPop)]
    return population

def correlation_coefficient(img1, img2):
    numerator = np.mean((img1 - img1.mean()) * (img2 - img2.mean()))
    denominator = img1.std() * img2.std()
    if denominator == 0:
        return 0
    else:
        result = numerator / denominator
        return result

def fittness_check(image1,image2,population):
    fitness_values = []
    for i in population:
        x = i[0]
        y= i[1]
        image3 = image1[y:y+35,x:x+29]
        corVal = correlation_coefficient(image3,image2)
        fitness_values.append(corVal)
    return fitness_values

def selection(fitness_values,population):
    combine = zip(fitness_values,population)
    combine = sorted(combine,reverse=True)
    ranked_pop = [x for y,x in combine]
    avg_max_fitness = [np.average(fitness_values),combine[0][0]] 
    ranked_pop[-1] = ranked_pop[0] 
    return ranked_pop,avg_max_fitness

# def cross_over(ranked_pop):
#     for i in range(1,len(ranked_pop)-1,2):
#         first_x = binary_repr(ranked_pop[i][0],10)
#         first_y = binary_repr(ranked_pop[i][1],9)
#         first = str(first_x)+str(first_y)
#         second_x = binary_repr(ranked_pop[i+1][0],10)
#         second_y = binary_repr(ranked_pop[i+1][1],9)
#         second = str(second_x)+str(second_y)
#         point = random.randint(0,19)
#         first = list(first)
#         second = list(second)
#         for index in range(point,len(first)-1):
#             first[index],second[index] = second[index],first[index]
#         first = "".join(first)
#         second = "".join(second)
#         first_x = int(first[0:10],2)
#         first_y = int(first[10:],2)
#         second_x = int(second[0:10],2)
#         second_y = int(second[10:],2)
#         ranked_pop[i] = (first_x,first_y) 
#         ranked_pop[i+1] = (second_x,second_y)

#     cross_pop = ranked_pop
#     return cross_pop
def cross_over(ranked_pop):
    for i in range(1,len(ranked_pop)-1,2):
        while True:
            if flip(0.8):
                first_x = binary_repr(ranked_pop[i][0],10)
                first_y = binary_repr(ranked_pop[i][1],10)
                first = str(first_x)+str(first_y)
                second_x = binary_repr(ranked_pop[i+1][0],10)
                second_y = binary_repr(ranked_pop[i+1][1],10)
                second = str(second_x)+str(second_y)
                point = random.randint(0,9)
                first = list(first)
                second = list(second)
                for index in range(point,len(first)-1):
                    first[index],second[index] = second[index],first[index]
                first = "".join(first)
                second = "".join(second)
                first_x = int(first[0:10],2)
                first_y = int(first[10:],2)
                second_x = int(second[0:10],2)
                second_y = int(second[10:],2)
                ranked_pop[i] = (first_x,first_y) 
                ranked_pop[i+1] = (second_x,second_y)
                if ranked_pop[i][0] < 996 and ranked_pop[i][1] < 478 and ranked_pop[i+1][0] < 996 and ranked_pop[i+1][1] < 478:
                    break


    cross_pop = ranked_pop
    return cross_pop
def mutation(cross_pop):
    for i in range(len(cross_pop)):
        is_run = flip(0.02)
        if is_run or cross_pop[i][0]>995:
            while True:
                pop_x = str(binary_repr(cross_pop[i][0]))
                pop_x = list(pop_x)
                point = random.randint(0,len(pop_x)-1)
                if pop_x[point] =='0':
                    pop_x[point] = '1'
                else:
                    pop_x[point] = '0'
                pop_x = ''.join(pop_x)
                pop_x = int(pop_x,2)
                cross_pop[i] = (pop_x,cross_pop[i][1])
                if pop_x < 996:
                    break
        if is_run or cross_pop[i][1]>477:
            while True:
                pop_y = str(binary_repr(cross_pop[i][1]))
                pop_y = list(pop_y)
                point = random.randint(0,len(pop_y)-1)
                if pop_y[point] =='0':
                    pop_y[point] = '1'
                else:
                    pop_y[point] = '0'
                pop_y = ''.join(pop_y)
                pop_y = int(pop_y,2)
                cross_pop[i] = (cross_pop[i][0],pop_y)
                if pop_y < 478:
                    break
    population = cross_pop
    return population

def check_termination(fitness_values,population):
    fitness_results = sorted(zip(fitness_values,population),reverse=True)
    match = []
    for val in fitness_results:
        if val[0] >= 0.83:
            match.append(val[1])
    if len(match)>0:
        return match
    else:
        return match



run_count = 0
best_fitness = 0
max_fitness = []
avg_fitness = []
fitness_match = []
im1 = np.array(img.imread("D:\Semester 5\AI\Course\groupgray.jpg"))
im2 = np.array(img.imread("D:\Semester 5\AI\Course\\boothigray.jpg"))
pop = initialize_pop(995,477,100)
while(True):
    fitness_values = fittness_check(im1,im2,pop)
    if run_count<=10000 and len(fitness_match) ==0:
        result = check_termination(fitness_values,pop)
        fitness_match.extend(result)
    else:
        show_output(im1,fitness_match)
        break
    ranked_pop,min_max = selection(fitness_values,pop)
    avg_fitness.append(min_max[0])
    max_fitness.append(min_max[1])
    pop = cross_over(ranked_pop)
    # pop = mutation(evolved_pop)
    run_count += 1

plt.figure(2)
plt.plot(max_fitness,'r')
plt.plot(avg_fitness,'g')
plt.show()

