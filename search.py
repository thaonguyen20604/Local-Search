import random
import numpy as np
import math

class LocalSearchStrategy:
    #cau2
    def random_restart_hill_climbing(problem, num_trial):
        best_path = []

        for _ in range(num_trial):
            current = problem.generate_initial_state()
            best_path.append((current[0], current[1], problem.get_evaluation(current)))
           
            while True:
                neighbours = problem.get_successor(current)
                if not neighbours:
                    break

                neighbour = max(neighbours, key=lambda state: problem.get_evaluation(state))
                
                if problem.get_evaluation(neighbour) <= problem.get_evaluation(current):
                    break
                
                current = neighbour
                x, y = current
                best_path.append((x, y, problem.get_evaluation(neighbour)))
                
        return best_path
    
    
    #cau3
    def simulated_annealing_search(problem, schedule):
        path = []
        t = 0
        current_state = problem.generate_initial_state()
        current_energy = problem.get_evaluation(current_state)
        path.append((current_state[0], current_state[1], current_energy))

        while True:
            T = schedule(t)
            if T==0:
                break

            neighbor = problem.get_successor(current_state)

            if neighbor is None:
                break
            
            next_state = random.choice(neighbor)
            next_energy = problem.get_evaluation(next_state)
            delta_e = np.subtract(next_energy, current_energy)

            if delta_e > 0:
                path.append((next_state[0], next_state[1], next_energy))
                current_state = next_state
                current_energy = next_energy
            else:
                if random.random() < math.exp(delta_e/T):
                    path.append((next_state[0], next_state[1], next_energy))
                    current_state = next_state
                    current_energy = next_energy

            t += 1
            
        return path
    

    def get_index_lbs(arr): #get index of z from tuple (z_x_index, z_y_index, z_value)
        tmp = []
        for a in arr:
            x, y, _ = a
            tmp.append((x,y))
        return tmp
    
    def find_src(A,destination): #find parent nodes of input, return an array contains all parents node
        find = []
        while True:
            for a in A:
                if destination in a[1]:
                    find.append(a[0])
                    destination = a[0]
                    break
            else:
                break
        return find
    
    def local_beam_search(problem, k) -> list: 
        path = list()
        find_path = [] #array contains tuples, in tuple contains 2 element: source and an array contains destinations
        count = 0 #count variable use to get element form array find_path
        current_state = []
        current_state.append(problem.generate_initial_state())
        tmp = [] #an empty temporary array use to contain k most optimal elements
        
        while current_state:
            satisfied_successors = [] #an array contains successors that more optimal than current state
            
            for curr_state in current_state: 
                z_curr = problem.get_evaluation(curr_state) #get value of z 
                all_successor = problem.get_successor(curr_state) #get all succesors of z by using z_index
                x_curr, y_curr = curr_state #get value of x and value of y of current node
                find_path.append(((x_curr,y_curr,z_curr),[])) #append source and its successors
                if all_successor:
                    for succ in all_successor: #get optimal successors
                        z_succ = problem.get_evaluation(succ)
                        if z_succ > z_curr:
                            x_succ, y_succ = succ
                            satisfied_successors.append((x_succ, y_succ, z_succ))
            
            if not satisfied_successors: #If not find optimal successor, then this is k optimal elements
                tmp += current_state
                tmp_x, tmp_y = tmp[0]
                tmp_z = problem.get_evaluation(tmp[0])
                path = [(tmp_x,tmp_y,tmp_z)] + LocalSearchStrategy.find_src(find_path,(tmp_x,tmp_y,tmp_z))
                break

            satisfied_successors.sort(key=lambda x: x[2], reverse=True) #sort theo z value

            current_state = LocalSearchStrategy.get_index_lbs(satisfied_successors)
            if k <= len(current_state):
                current_state = current_state[:k]

            _, des = find_path[count]
            for c in current_state:
                x, y = c
                z = problem.get_evaluation(c)            
                des.append((x,y,z))
            count += 1   
        
        return path[::-1]
