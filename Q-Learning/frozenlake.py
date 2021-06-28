import numpy as np

import random

import gym

import matplotlib.pyplot as plt

from new_reward_fun import create_reward_function


def find_max(array_s):
    max_s = np.max(array_s)
    array_s_max = []
    for i in range(len(array_s)):
        if array_s[i] == max_s:
            array_s_max.append(i)
    return random.choice(array_s_max)


def get_moves(q_array):
    move_array = []

    for i in range(64):
        next_move = find_max(q_array[i])
        move_array.append(next_move)
    return move_array


def make_moves(env, q_array):
    env.reset()

    state = env.reset()
    print("New episode")

    for i in range(50):
        env.render()
        action = q_array[state]

        new_state, reward, terminal_state, info = env.step(action)

        if terminal_state:
            break
        state = new_state
    env.render()
    env.close()


def create_frozen_lake(a_choice, slippery):
    if slippery:
        env = gym.make('FrozenLake8x8-v0')
    else:
        env = gym.make('FrozenLake8x8-v0', is_slippery=False)

    action_size = env.action_space.n
    state_size = env.observation_space.n

    if a_choice == 2:
        if slippery:
            create_reward_function(action_size, state_size, env.env)
        else:
            create_reward_function(action_size, state_size, env.env, False)
    q_state_action = [[0 for i in range(action_size)] for j in range(state_size)]

    exploration = 1

    rewards = []
    for episode in range(10000):
        state = env.reset()
        sum_rewards = 0

        for i in range(120):

            exploitation = random.uniform(0, 1)
            if exploitation > exploration:
                actual_state_action = q_state_action[state]
                action = np.argmax(actual_state_action)
            else:
                action = env.action_space.sample()

            new_state, reward, terminal_state, info = env.step(action)

            next_state_action = q_state_action[new_state]
            q_state_action[state][action] = q_state_action[state][action] + 0.7 * (reward + 0.95 * np.max(next_state_action) - q_state_action[state][action])

            state = new_state
            sum_rewards += reward

            if terminal_state is True:
                break

        exploration -= 0.00005
        rewards.append(sum_rewards)

    return q_state_action, env, rewards


def choose_algorithm():
    while True:
        a_choice = input("Choose the reward algorithm:\n1-default\n2-proposed algorithm")
        a_choice = int(a_choice)
        if a_choice == 1 or a_choice == 2:
            break
        print("Invalid data")

    while True:
        s_choice = input("Is the lake slippery?:\ny-yes\nn-no")
        if s_choice == 'y' or s_choice == 'n':
            if s_choice == 'y':
                slippery = True
            else:
                slippery = False
            break
        print("Invalid data")
    return a_choice, slippery


def run_frozen_lake():
    a_choice, slippery = choose_algorithm()
    q_state_action, env, rewards = create_frozen_lake(a_choice, slippery)
    q_moves = get_moves(q_state_action)
    make_moves(env, q_moves)
    return rewards


if __name__ == "__main__":
    rewards = run_frozen_lake()
    plt.plot(rewards, 'm')
    plt.show()
