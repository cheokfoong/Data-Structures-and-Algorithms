
def optimise_single_pickup(corridor):
    """
    Maximizing the total value of items in a given list of integers. The input value corridor is
    a list of integers. The output value returns a tuple with two elements where the first element
    is the maximum total value it can obtain and the second element represents a list of binary numbers.
    Time complexity: O(N^2), where N is the length of corridor
    Space complexity: O(N^2), where N is the length of corridor
    """
    memo = [0] * len(corridor) #stores either 0 or 1 for picking item
    maxValue = 0
    energy = 1
    
    for i in range(1, (len(corridor))):
        if corridor[i] > 0:
            if energy >= 1:
                maxValue += corridor[i]
                energy -= 1
                memo[i] = 1

            # optimize the choices made again to get maximum value
            elif energy == 0: 
                minValue = corridor[i]
                
                # back track to get the min positive value 
                for j in range(i, 0, -1):                
                    if (corridor[j] > 0) and (corridor[j] < minValue):
                        minValue = corridor[j]
                        
                energy = 1 # reset energy

                # reselect the items into memo and this time skip the min positive value
                maxValue = 0
                for j in range (1, i+1):
                    if corridor[j] > 0 and corridor[j] != minValue:
                        maxValue += corridor[j]
                        energy -= 1
                        memo[j] = 1
                    else:
                        energy += 1
                        memo[j] = 0
                        
        else:
            energy += 1
            memo[i] = 0
            
    return (maxValue, memo)

x = ([4, 0, 4, 1, -3, 4, 3, 2])
y = [4,0,4,4,-3,1,3]
print(optimise_single_pickup(y))

def optimise_multiple_pickup(corridor):
    """
    Maximizing the total value of items while continuesly picking up items until energy reaches 0 when instructed to pick up items.
    The input value corridor is a list of integers. The output value returns a tuple with two elements where the first element
    is the maximum total value it can obtain and the second element represents a list of binary numbers.
    Time complexity: O(N^2), where N is the length of corridor
    Space complexity: O(N^2), where N is the length of corridor
    """
     
    memo = [0] * len(corridor) #stores either 0 or 1 for picking item
    maxValue = 0
    energy = 1
    length = 1 # current length we are at the corridor list
    
    for i in range(1, (len(corridor))):
        #stop loop if reaches end of corridor list
        if length >= len(corridor):
            break
        
        if corridor[length] > 0:
            if energy >= 1:
                for j in range(energy):
                    #stop loop if reaches end of corridor list
                    if length >= len(corridor):
                        break
                    
                    maxValue += corridor[length]
                    energy -= 1
                    memo[length] = 1
                    length += 1

            elif energy == 0:
                #creates temporary energy, maxValue and length variables
                temp_energy = 1
                temp_maxValue = 0
                temp_length = length

                #indicates skipping all value from corridor[1] to corridor[length] and thus keep adding energy
                for j in range(1, length):
                    temp_energy += 1

                #getting the maxValue starting from corridor[length] up to energy finishes    
                for j in range(temp_energy):
                    #stop loop if reaches end of corridor list
                    if temp_length >= len(corridor):
                        break
                    temp_maxValue += corridor[temp_length]
                    temp_length += 1

                # compare if no energy was used until current corridor[i] and only start picking up items continuosly from current[i],
                # is the temp_maxValue more than maxValue that we have gotten so far?
                if temp_maxValue >= maxValue and temp_energy > energy:                   
                    energy = 1
                    maxValue = 0
                    
                    for j in range(1, length):
                        memo[j] = 0
                        energy += 1
                    maxValue += corridor[length]
                    memo[length] = 1
                    length += 1
                    
                else:
                    energy += 1
                    memo[length] = 0
                    length += 1
                
        else:
            energy += 1
            memo[length] = 0
            length += 1

    return (maxValue, memo)

print(optimise_multiple_pickup([0,0,5,-4,1,1]))
    
def optimal_shade_selector(shades, probs):
    """
    Finding the minimum cost decision tree for some given set of shades along with a set of probability.
    The input values shades is a list of numbers between 0 to 1 inclsuive representing the brightness
    of each shade and probs is a list of numbers between 0 to 1 inclsuive representing the probabilities
    of each shade in shades. The output value is a single number which is the cost of the optimal decision tree.
    Time complexity: O(N^3) where N is the length of shades
    Space complexity: O(N^3) where N is the length of shades
    """
    #I don't know how to do :'(
    n = len(shades)
    memo = [None] * len(shades)
##    for i in range(len(memo)):
##        memo[i] = []

##    output = 0
##    j = min_output
##    i = j
        
    for i in range(n):      
        for j in range(i+1,n):
            for k in range(0,i-1):
                
         
##shades = [0.1, 0.2, 0.3]
##probs = [0.25, 0.2, 0.05]
##print(optimal_shade_selector(shades,probs))
