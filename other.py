# print(f"My History: {my_history}   He History: {opponent_history}")
    
    ret = {}
    
    for i in range(len(my_history)):
        if (my_history[i] == "rock" and opponent_history[i] == "scissor") or (my_history[i] == "scissor" and opponent_history[i] == "rock"):
            # change to scissor
            ret = {
                "scissor": 0.8,
                "rock": 0.1,
                "paper": 0.1
            }
        elif (my_history[i] == "scissor" and opponent_history[i] == "paper") or (my_history[i] == "paper" and opponent_history[i] == "rock"):
            # change to paper
            ret = {
                "scissor": 0.1,
                "rock": 0.1,
                "paper": 0.8
            }
        elif (my_history[i] == "paper" and opponent_history[i] == "rock") or (my_history[i] == "rock" and opponent_history[i] == "paper"):
            # change to rock
            ret = {
                "scissor": 0.1,
                "rock": 0.8,
                "paper": 0.1
            }
        elif (my_history[i] == opponent_history[i]):
            ret = {"scissor": uniform(0,1),
                "rock": uniform(0,1),
                "paper": uniform(0,1)}


    # return ret

    # return {"rock": 0.333,
    #         "scissor": 0.333,
    #         "paper": 0.334}