from random import uniform
from math import exp

import operator

mapper = ["rock", "scissor", "paper"]


def generate_opponent_policy(difficulty='easy'):
    ret = {}
    var = 0.5
    if difficulty == 'easy':
        logit = [uniform(-var, var), uniform(-var, var), uniform(-var, var)]
        logit_exp = [exp(x) for x in logit]
        for x, y in ((x, y) for x in mapper for y in mapper):
            ret[x, y] = {
                "rock": logit_exp[0] / sum(logit_exp),
                "scissor": logit_exp[1] / sum(logit_exp),
                "paper": logit_exp[2] / sum(logit_exp)}
    else:
        for x, y in ((x, y) for x in mapper for y in mapper):
            logit = [uniform(-var, var), uniform(-var, var),
                     uniform(-var, var)]
            logit_exp = [exp(x) for x in logit]
            ret[x, y] = {
                "rock": logit_exp[0] / sum(logit_exp),
                "scissor": logit_exp[1] / sum(logit_exp),
                "paper": logit_exp[2] / sum(logit_exp)}

    return ret


def sample(p):
    """sample one element from the probability distribution.

    Parameters
    ----------
    p : list of floats.
        probability of drawing rock, proability of drawing scissor, probability of drawing paper
    Return
    ----------
    string
        chosen form(rock, scissor, paper)
    """
    r = 0
    q = []
    for x in p:
        r += p[x]
        q.append(r)  

    v = uniform(0, 1)
    for i in range(3):
        if v <= q[i]:
            return mapper[i]
    return mapper[2]


def evalute_rsp(form_of_a, form_of_b):
    """
        given two forms, return result of the game.

    Parameters
    ----------
    form_of_a : string
        one of "rock", "scissor", "paper", which the player a drawed
    form_of_b : string
        one of "rock", "scissor", "paper", which the player b drawed
    Returns
    -------
    int
        1 if player a wins,
        0 if draws,
        and -1 if player b wins
    """
    if (form_of_a == "rock" and form_of_b == "scissor") or (form_of_a == "paper" and form_of_b == "rock") or (form_of_a == "scissor" and form_of_b == "paper"):
        return 1
    elif form_of_a == form_of_b:
        return 0
    elif (form_of_a == "rock" and form_of_b == "paper") or (form_of_a == "paper" and form_of_b == "scissor") or (form_of_a == "scissor" and form_of_b == "rock"):
        return -1


def generate_policy_exploration(my_history, opponent_history,
                                my_form_last_time, opponent_form_last_time):
    return {"rock": 0.333,
            "scissor": 0.333,
            "paper": 0.334}


def generate_policy_exploitation(my_history, opponent_history,
                                 my_form_last_time, opponent_form_last_time):
    """
        You must fill here
        Find the value for rock, scissor and paper
    """
    rock = paper = scissor = 0

    for i in opponent_history:
        if i == "rock":
            rock += 1
        if i == "paper":
            paper += 1
        if i == "scissor":
            scissor += 1

    rock /= 1000
    scissor /= 1000
    paper /= 1000

    stats = {"rock": rock,
             "scissor": scissor,
             "paper": paper}

    choice = max(stats.items(), key=operator.itemgetter(1))[0]

    if (choice == "rock"):
        return {"rock": 0.1,
                "scissor": 0.1,
                "paper": 0.8}
    elif (choice == "scissor"):
        return {"rock": 0.8,
                "scissor": 0.1,
                "paper": 0.1}
    elif (choice == "paper"):
        return {"rock": 0.1,
                "scissor": 0.8,
                "paper": 0.1}


def run(difficulty='easy'):
    """

    Parameters
    ----------
    Return
    ----------
    reward

    """
    opponent_policy = generate_opponent_policy(difficulty=difficulty)
    result_sum = 0
    statistics = {
        "opponent_history": [],
        "my_history": [],
        "my_form_last_time": "rock",
        "opponent_form_last_time": "rock"}

    # Exploration Phase
    for i in range(1000):
        my_policy = generate_policy_exploration(**statistics)
        
        my_action = sample(my_policy)  

        opponent_action = sample(opponent_policy[(
            statistics['my_form_last_time'], statistics['opponent_form_last_time'])])
        result = evalute_rsp(my_action, opponent_action)

        statistics['my_history'].append(my_action)
        statistics['opponent_history'].append(opponent_action)
        statistics['my_form_last_time'] = my_action
        statistics['opponent_form_last_time'] = opponent_action

    # Exploitation Phase
    statistics['my_form_last_time'] = 'rock'
    statistics['opponent_form_last_time'] = 'rock'

    for i in range(1000):
        my_policy = generate_policy_exploitation(**statistics)
        my_action = sample(my_policy)

        opponent_action = sample(opponent_policy[(
            statistics['my_form_last_time'], statistics['opponent_form_last_time'])])
        result = evalute_rsp(my_action, opponent_action)
        result_sum += result

        statistics['my_form_last_time'] = my_action
        statistics['opponent_form_last_time'] = opponent_action
    return result_sum


if __name__ == "__main__":
    cnt = 10
    for difficulty in ("easy", "hard"):
        ret = []
        for i in range(cnt):
            ret.append(run(difficulty=difficulty))
        print("[%s]\taverage game results: %0.2f" %
              (difficulty, sum(ret) / cnt))
        print("result:", ret, '\n')
