import os
name = "Bob"
score = 97000
def highScores(name,score):
    data = []
    temp = [[],[]]
    f = open('scores.txt','r+') # Open the file
    for line in f: # For every line in the file
        data.append(line[:-1]) # Append it to the list 'data'
    for i in range(10):
        if 97000 > int(data[i]): # If the score > a current score...
            cur = i # Keep track of the score
            break
        else:
            cur = '' # If there are no scores higher, ignore it
    if cur != '':
        # ADDS THE FIRST VALUES UP TO THE CURRENT SCORE
        for i in range(cur):
            temp[0].append(data[i]) # Up to the new score, add values to list...
            temp[1].append(data[20-(10-i)]) # Add names corresponding to value...
        print(temp[0])
        print(temp[1])
        # ADD THE CURRENT SCORE
        temp[0].append(str(score)) # Add the new score
        temp[1].append(name) # Add the new score name
        print("")
        print(temp[0])
        print(temp[1])
        ## APPENDS REMAINING VALUES
        for i in range(cur,10):
            temp[0].append(data[i]) # Append remaining scores to list
            temp[1].append(data[i+10]) # Append remaining names to list
        print("")
        print(temp[0])
        print(temp[1])
        temp[0].remove(temp[0][-1]) # Remove lowest score
        temp[1].remove(temp[1][-1]) # Remove lowest player
        myFile = open("scores.txt","w") # Create a new scores file
        for f in range(2): # Write to the new file...
            for i in range(10):
                if i == 0 and f == 0:
                    myFile.write(temp[f][i]) # For the first score without a new line
                else:
                    myFile.write('\n%s'%temp[f][i]) # For the rest of the scores
highScores(name,97000)
