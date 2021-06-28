from optproblems.cec2005 import F6
import random
import math
import numpy


def init_population(size_of_population, dim):
    population = []
    sigma = 5
    sigma_array = []
    for s in range(dim):
        sigma_array.append(sigma)
    for i in range(size_of_population):
        subject = []
        subject_with_sigma = []
        for j in range(dim):
            r = random.randint(-100, 100)
            subject.append(r)
        subject_with_sigma.append(subject)
        subject_with_sigma.append(sigma_array)
        population.append(subject_with_sigma)
    return population


def rate(list_of_population):
    results = []
    dim = len(list_of_population[0][0])
    fun = F6(dim)
    for i in list_of_population:
        arg = i[0]
        j = fun.objective_function(arg)
        results.append([j, i])
    results.sort(key=lambda x: x[0])
    return results


def mutation(subject):
    l = len(subject[0])
    a = numpy.random.normal(0, 1)
    r0 = 1/math.sqrt(2*l)
    sn = 2 * math.sqrt(l)
    r1 = 1/math.sqrt(sn)
    mutant = []
    mutant_sigma = []
    mutant_subject = []
    for i in range(len(subject[0])):
        sigma = subject[1][i]
        bi = numpy.random.normal(0, 1)
        an = a * r1 + bi * r0
        sigma = round(sigma * math.exp(an), 5)
        mutant_sigma.append(sigma)
        xi = round(subject[0][i] + sigma * numpy.random.normal(0, 1), 5)
        if xi > 100:
            xi = 100
        if xi < -100:
            xi = -100
        mutant_subject.append(round(subject[0][i] + sigma * numpy.random.normal(0, 1), 5))

    mutant.append(mutant_subject)
    mutant.append(mutant_sigma)
    return mutant


def crossover(a, b):
    offspring = []
    offspring_subject = []
    offspring_sigma = []
    w = numpy.random.uniform(0, 1)
    for i in range(len(a[0])):
        offspring_subject.append(round(a[0][i]*w + (1-w)*b[0][i], 5))
        offspring_sigma.append(round(a[1][i]*w + (1-w)*b[1][i], 5))
    offspring.append(offspring_subject)
    offspring.append(offspring_sigma)
    return offspring


def cross_and_mut(lambda_population):
    temp_population = []
    population = []
    lam_pop = lambda_population
    num = len(lam_pop)*0.25
    while num > 0:
        a = random.choice(lam_pop)
        lam_pop.remove(a)
        b = random.choice(lam_pop)
        lam_pop.remove(b)
        temp_population.append(crossover(a, b))
        num -= 2
    for i in range(len(lam_pop)):
        temp_population.append(lam_pop[i])

    for i in temp_population:
        population.append(mutation(i))
    return population


def init_lambda_population(lam, u_population):
    lambda_population = []
    s = len(u_population)
    for i in range(lam):
        index = random.randint(0, s-1)
        x = u_population[index]
        lambda_population.append(x)
    return lambda_population


def rate_lambda_population(u_population, lambda_population):
    population = []
    for i in range(len(u_population)):
        population.append(u_population[i])
    for i in range(len(lambda_population)):
        population.append(lambda_population[i])
    sort_population = rate(population)
    return sort_population


def selection(sorted_population, u):
    u_population = []
    for i in range(u):
        u_population.append(sorted_population[i][1])
    return u_population[:u]


def check_influence_of_lambda():
    set_of_lambda = []
    values = []
    results = []

    dim = 10
    mu = 20

    initial_u_population = init_population(mu, dim)
    rate_u_population = rate(initial_u_population)
    result = rate_u_population[0][0]

    for i in range(3, 21, 2):
        u_population = initial_u_population
        lam = mu*i
        num_of_iterations = round(100000/lam)
        while num_of_iterations >= 0:
            lambda_population = init_lambda_population(lam, u_population)
            offspring = cross_and_mut(lambda_population)
            rate_lam_population = rate_lambda_population(u_population, offspring)
            u_population = selection(rate_lam_population, mu)
            result = round(rate_lam_population[0][0])
            num_of_iterations -= 1

        set_of_lambda.append(i)
        values.append(result)

    results.append(set_of_lambda)
    results.append(values)
    return results

def outcome(results, lambda_iter):
    sum = 0
    arr_results = []
    for i in range(len(results)):
        sum += results[i][1][lambda_iter]
        arr_results.append(results[i][1][lambda_iter])
    outcome = []
    outcome.append(sum / len(results))
    outcome.append(min(arr_results))
    outcome.append(max(arr_results))
    return outcome

def draw_table(results):
    szer = 42
    print("-" * szer)
    print("| Lambda value |           Result        |")
    print("|              | Avarage |  MIN  |  MAX  |")
    print("*" * szer)
    for i in range(len(results[0][0])):
        calculation = outcome(results, i)
        print("| %7i * mu | %7i | %5i | %5i |" % (results[0][0][i], calculation[0], calculation[1], calculation[2]))
    print("-" * szer)



def main():
    results = []
    for i in range(8):
        results.append(check_influence_of_lambda())
    draw_table(results)


main()
