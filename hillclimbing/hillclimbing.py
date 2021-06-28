import random
from math import exp, sqrt
import matplotlib.pyplot as plt


def standard_deviation(results, arithmetic_mean):
    sum_squares = 0
    for i in results:
        sum_squares += i**2
    a_squares = sum_squares/len(results)
    s_deviation = sqrt(a_squares-(arithmetic_mean**2))
    return s_deviation


def sel_random(x, sigma):
    a = x - sigma
    b = x + sigma
    if a < -2 or b > 12:
        if b > 12:
            y = random.uniform(a, 12)
        if a < -2:
            y = random.uniform(-2, b)
        if a < -2 and b > 12:
            y = random.uniform(-2, 12)
    else:
        y = random.uniform(a, b)
    return y


def galar_function(x):
    q = -5*exp(-(x**2) / 2) - 4*exp(-((x-9)**2) / 8)
    return q


def hillclimbing(number, sigma):
    x = number
    stop = 100
    while stop != 0:
        chosen_point = sel_random(x, sigma)
        if galar_function(chosen_point) < galar_function(x):
            x = chosen_point
            y = galar_function(x)
            plt.scatter(x, y, c='blue', s=0.5)

        stop -= 1
    return x


def n_hillclimbing():
    x_values = []
    number = random.uniform(-2, 12)
    amount = 0
    results = []
    data = []
    for i in range(25):
        x_values.append(hillclimbing(number, 0.8))
    best_result = galar_function(x_values[0])
    worst_result = galar_function(x_values[0])
    for i in x_values:
        outcome = galar_function(i)
        results.append(outcome)
        amount += outcome
        if outcome < best_result:
            best_result = outcome
        if outcome > worst_result:
            worst_result = outcome
    average_score = amount / len(x_values)
    std_deviation = standard_deviation(results, average_score)
    data = [number, average_score, x_values, results, std_deviation, best_result, worst_result]
    return data


def main_function():
    random_num_results = []
    for i in range(10):
        random_num_results.append(n_hillclimbing())

    for r in range(len(random_num_results)):
        x = random_num_results[r][2]
        y = random_num_results[r][3]

        rgb = (random.random(), random.random(), random.random())
        plt.scatter(x, y, c=[rgb], s=75)

        write_informations(random_num_results, r)

    plt.title('Stochastyczny algorytm wspinaczkowy')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def write_informations(random_num_results, i):
    print(f'For number: {round(random_num_results[i][0], 7)} arithmetic mean of results is: {round(random_num_results[i][1], 7)}, standard deviation is: {round(random_num_results[i][4], 7)}, best value: {round(random_num_results[i][5], 7)} and worst value: {round(random_num_results[i][6], 7)}.')


main_function()
