#CHSH GAME SIMULATOR

#To play the 3 player variant, follow these steps: 
#Remove the "#" infront of line 17
#Remove the "#" infront of line 22
#Add "+c" to the sum on line 49
#Add "and zz" to the condition on line 54

import random

wins = 0
losses = 0

#Code inputs from the referee into Boolean values
xx = False
yy = False
zz = False

#Strategies
a = 1
b = 0
c = 0
output = False

for i in range(10000): 
    
    #Generate randomly the inputs of the referee and code the to Boolean values
    x = random.randint(0, 1)
    if x == 0: 
        xx = True
    else: 
        xx = False
        
    y = random.randint(0, 1)    
    if y == 0: 
        yy = True
    else: 
        yy = False
        
    z = random.randint(0, 1)
    if z == 0: 
        zz = True
    else: 
        zz = False
        
    
    #Code output to a Boolean value
    
    if (a+b+c)/2 == 0: 
        output = True
    else: 
        output = False
        
    if (xx and yy and zz) == output: 
        wins += 1
    else:
        losses += 1
    
print("wins", wins / 10000)
print("losses", losses / 10000)

