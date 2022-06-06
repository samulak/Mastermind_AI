import random
from scsa import *
from player import *
from copy import deepcopy
import sys
class dinosaur(Player):
    def __init__(self):
        sys.setrecursionlimit(5000)
        self.player_name = "dinosaur"                
        # self.All_colors stores all the colors that the agent found in
        # the first stage.
        # Ex: {'J': 0, 'I': 0, 'D': 3, 'F': 0, 'A': 0, 'B': 1}
        self.All_colors = {}
        
        # self.All_codes_attempted and self.All_codes_attempted_backup 
        # stores all codes that that agent attemptet.
        # First # bulls, second # cows
        # Ex:['ADCD': (2, 2),
        #     'AACD': (2, 1),
        #     'AAAD': (1, 1),
        #     'AAAA': (0, 0)]
        self.All_codes_attempted = []
        self.All_codes_attempted_backup = []
        
        # self.All_codes_attempted_two_color 
        # stores all codes that that agent attemptet.
        # First # bulls, second # cows
        # Ex:{'ADCD': (2, 2),
        #     'AACD': (2, 1),
        #     'AAAD': (1, 1),
        #     'AAAA': (0, 0)}
        self.All_codes_attempted_two_color = {}
        
        # self.Deciphered_code will initialize to:
        # Ex: ['0', '0', '0', '0'], 0 is digit zero
        # Once the agent checks individual pegs
        # the variable will be stored it in this form:
        # ['0', 'C', '0', 'B']
        self.Deciphered_code = []
        
        # self.Current_code is a code that is used to send a 
        # string to the game environment
        self.Current_code = ''
        
        # self.Saved_responses contains all the codes that the
        # agent attempted when checking individual pegs.
        # First # bulls, second # cows, third 3 peg position
        #Ex: [['CDDCG', 3, 2, 0],
        #     ['FDDCG', 2, 2, 1],
        #     ['FFDCG', 1, 2, 2],
        #     ['FFFCG', 0, 1, 3]]
        self.Saved_responses = []
        
        # self.Counter is used to keep track of individual pegs
        # that are checked.
        self.Counter = 0
        
        # self.Constraints contains constraints that are allowable for 
        # individual pegs. 
        # Ex: {0: ['A','B'], <- means that peg 0 can be 'A' or 'B'
        #      1: ['C'],
        #      2: [],
        #      3: ['A', 'C']}
        self.Constraints = {}
        
        # All bool variables are used to make sure that
        # the agent never revisits a stage that it completes
        self.Found_all_colors = False
        self.Found_more_than_one = False
        
        # Dictionary used for easier translation between
        # ints and strings
        self.Color_Dictionary = {0: 'A',
         1: 'B',
         2: 'C',
         3: 'D',
         4: 'E',
         5: 'F',
         6: 'G',
         7: 'H',
         8: 'I',
         9: 'J',
         10: 'K',
         11: 'L',
         12: 'M',
         13: 'N',
         14: 'O',
         15: 'P',
         16: 'Q',
         17: 'R',
         18: 'S',
         19: 'T',
         20: 'U',
         21: 'V',
         22: 'W',
         23: 'X',
         24: 'Y',
         25: 'Z'}



    # Generates a random state by using self.All_colors,
    # self.Deciphered_code and self.Constraints
    def generate_random_code(self, colors):
        self.constraint_elimination()
        Temp_colors = deepcopy(self.All_colors)
        Temp_constrains = deepcopy(self.Constraints)

        # Use self.Deciphered_code to remove already found colors form Temp_colors
        for code_pos in self.Deciphered_code:
            if code_pos != '0':
                Temp_colors[code_pos] -=  1

        # Use information from self.Deciphered_code & 
        # reduced Temp_colors & self.Constraints
        # to produce a new random state.
        New_random_guess = ''
        for code_pos in range(len(self.Deciphered_code)):
            if self.Deciphered_code[code_pos] == '0':
                if Temp_constrains[code_pos] == []:
                    random_code = []
                    for c in Temp_colors:
                        for i in range(Temp_colors[c]):
                            random_code.append(c)
                        random_char = random.choice(random_code)
                random_char = random.choice(Temp_constrains[code_pos])
                New_random_guess += random_char
                Temp_colors[random_char] -= 1
            elif self.Deciphered_code[code_pos] != '0':
                New_random_guess += self.Deciphered_code[code_pos]
        
        # Check if the current guess was already attempted
        # if it was run the generator again until new random code is found
        if all(attempt!=New_random_guess for attempt in self.All_codes_attempted):
            return  New_random_guess
        else:
            z = self.generate_random_code(colors)
            return z
    
    # Initialize all posible colors for individual pegs
    def constraint_initalization(self, board_length):
        for i in range(board_length):
            tmp = []
            for color in self.All_colors:
                if self.All_colors[color] != 0:
                    tmp.append(color)
            self.Constraints[i] = tmp
            
    # Eliminates constraints by using self.Deciphered_code & self.All_codes_attempted.
    # self.Deciphered_code allows for reduction of a peg to a single constraint
    # if a code in self.All_codes_attempted has zero bulls that means that
    # all of the colors are in a wrong positions and can be pruned from the self.Constraints
    def constraint_elimination(self):
        Temp_colors = deepcopy(self.All_colors)

        # Use self.Deciphered_code to remove already found colors form Temp_colors
        for code_pos in self.Deciphered_code:
            if code_pos != '0':
                Temp_colors[code_pos] -= 1
        
        # Remove colors that were already found from self.Constraints
        for i in Temp_colors:
            if Temp_colors[i] == 0:
                for j in range(len(self.Constraints)):
                    if i in self.Constraints[j]:
                        self.Constraints[j].remove(i)

        # Use all of the guesses that had 0 bulls to remove constraints 
        New_elimination_list = []
        for attempt in self.All_codes_attempted:
            if attempt[1] == 0:
                for i in range(len(attempt[0])):
                    if attempt[0][i] in self.Constraints[i]:
                        self.Constraints[i].remove(attempt[0][i])
        
        # Place found pegs into constraints
        for i in range(len(self.Deciphered_code)):
            if self.Deciphered_code[i] != '0':
                self.Constraints[i] = [self.Deciphered_code[i]]
    
    # update_All_codes_attempted uses found pegs to remove bulls
    # from the All_codes_attempted.
    # Ex: If the attempt in All_codes_attempted ['AGFAS', 1, 4]
    # and self.Deciphered_code = ['0', '0', 'F', '0', '0']
    # then we can remove 'F' from the bulls. ['AGFAS', 0, 4]
    # and the rest of the data can be used to reduce constraints.
    def update_All_codes_attempted(self):
        self.All_codes_attempted = deepcopy(self.All_codes_attempted_backup)
        for attempt in self.All_codes_attempted:
            for peg in range(len(attempt[0])):
                if attempt[0][peg] == self.Deciphered_code[peg]:
                    attempt[1] -= 1
    
    # If there is only one constraint self.Deciphered_code can be updated
    def update_deciphered_from_constraints(self):
        for i in range(len(self.Constraints)):
            if len(self.Constraints[i]) == 1 and self.Deciphered_code[i] == '0':
                self.Deciphered_code[i] = self.Constraints[i][0]
    
    # Summing up values in Dictinary All_colors
    def sum_up(self):
        sum = 0
        for clr in self.All_colors:
            sum += self.All_colors[clr]
        return sum

    # Count found pegs
    def colors_found(self):
        colors_found = 0
        for peg in self.Deciphered_code:
            if peg != '0':
                colors_found += 1
        return colors_found
        
    # Count number of colors found
    def count_number_of_colors(self):
        number = 0
        for col in self.All_colors:
            if self.All_colors[col] != 0:
                number += 1
        return number

    # Guessing colors randomly at the begining of the round unless ABColor
    def guess_colors(self,colors, scsa, board_length):
        
        my_random_color = random.choice(colors)
        guess = my_random_color * board_length
        if self.All_colors != {}:
            if all(attempt!=my_random_color for attempt in self.All_colors):
                return guess
            else:
                return self.guess_colors(colors, scsa, board_length)
        else:
            return guess

    # Procedure for solving problem with two colors after making first guess
    # 1. Start with a monochromatic guess of the color with the highest occurrence. 
    # 2. Change each peg at a time.
    # 3. If the response of the change results in a higher bull count, store the change.
    #    Else, change back 
    # 4. Then change the next peg.
    def twocolor_problem(self, board_length, last_response, max_col, other):
        if self.Saved_responses == []:
            self.Current_code = max_col * board_length
            bulls, cows = self.All_codes_attempted_two_color[self.Current_code]
            self.Saved_responses.append([self.Current_code,bulls,cows])
            guess = list(self.Current_code)
        else:
            guess = list(self.Current_code)
            if last_response[0] < self.Saved_responses[-1][1]:
                guess[self.Counter] = max_col
                self.Counter += 1
            else:
                self.Saved_responses.append([self.Current_code,last_response[0],last_response[1]])
                self.Counter += 1         
        if self.Counter < board_length:
            guess[self.Counter] = other
        return ''.join(guess)
    
    def make_guess(self, board_length, colors, scsa, last_response):
        # Reinitialize Player variables at the beginning of a new round
        if last_response[-1] == 0:
            self.Counter = 0            
            self.Current_code = ''            
            self.All_colors = {}
            self.Constraints = {}           
            self.Deciphered_code = []
            self.Saved_responses = []
            self.All_codes_attempted = []
            self.All_codes_attempted_backup = []
            self.All_codes_attempted_two_color = {}
            self.Found_all_colors = False
            self.Found_more_than_one = False
            self.Deciphered_code = [str(0)] * board_length
            
            #SCSA specific color initialization
            if scsa == "OnlyOnce" and board_length == len(colors):
                for i in range(board_length):
                    self.All_colors[self.Color_Dictionary[i]] = 1                
                    self.constraint_initalization(board_length)
                self.Current_code = self.generate_random_code(colors)
                self.Found_all_colors = True
            elif scsa == "ABColor":
                self.Found_all_colors = True
                self.All_colors['A'] = 1
                self.All_colors['B'] = 0
                self.Current_code = 'A'*board_length
            else:
                self.Current_code = self.guess_colors(colors,scsa,board_length)
            return self.Current_code

        # Begin adding found colors until all colors are found
        if last_response[-1] != 0 and self.Found_all_colors == False:
            self.All_codes_attempted_two_color[self.Current_code] = [last_response[0], last_response[1]]
            self.All_codes_attempted.append([self.Current_code, last_response[0], last_response[1]])
            last_color = self.Current_code[0]
            self.All_colors[last_color] = last_response[0] + last_response[1]

            # Generate a random code if all colors are found
            # and initiate SCSA specific strategies
            if board_length == self.sum_up():
                self.Found_all_colors = True
                self.constraint_initalization(board_length)
                if scsa == "TwoColorAlternating" or scsa == "mystery5":
                    sort = sorted(self.All_colors.items(),key=lambda x:x[1])
                    first_col = sort[-1][0]
                    second_col = sort[-2][0]
                    first_code = ''
                    second_code = ''
                    rem = 0
                    rem = board_length % 2
                    first_code = (first_col + second_col) * int(board_length/2)
                    second_code = (second_col + first_col) * int(board_length/2)
                    if rem != 0:
                        first_code += first_col
                        second_code += second_col
                    self.Saved_responses.append(first_code)
                    return second_code
                elif scsa == "TwoColor" or self.count_number_of_colors() == 2:
                    sort = sorted(self.All_colors.items(),key=lambda x:x[1])
                    max_col = sort[-1][0]
                    other_col = sort[-2][0]
                    self.Current_code = self.twocolor_problem(board_length, last_response, max_col, other_col)
                    return self.Current_code
                elif scsa == "mystery2":
                    sort = sorted(self.All_colors.items(),key=lambda x:x[1])
                    first_col = sort[-1][0]
                    second_col = sort[-2][0]
                    third_col = sort[-3][0]
                    first_code = ''
                    second_code = ''
                    third_code = ''
                    fourth_code = ''
                    fifth_code = ''
                    sixth_code = ''
                    rem = 0
                    rem = board_length % 3
                    first_code = (first_col + second_col + third_col) * int(board_length/3)
                    second_code = (first_col + third_col + second_col) * int(board_length/3)
                    third_code = (second_col + first_col + third_col) * int(board_length/3)
                    fourth_code = (second_col + third_col + first_col) * int(board_length/3)
                    fifth_code = (third_col + first_col + second_col) * int(board_length/3)
                    sixth_code = (third_col + second_col + first_col) * int(board_length/3)
                    if rem == 1:
                        first_code += first_col
                        second_code += first_col
                        third_code += second_col
                        fourth_code += second_col
                        fifth_code += third_col
                        sixth_code += third_col
                    elif rem == 2:
                        first_code += (first_col + second_col)
                        second_code += (first_col + third_col)
                        third_code += (second_col + first_col)
                        fourth_code += (second_col + third_col)
                        fifth_code += (third_col + first_col)
                        sixth_code += (third_col + second_col)   
                    self.Saved_responses.append(second_code)
                    self.Saved_responses.append(third_code)
                    self.Saved_responses.append(fourth_code)
                    self.Saved_responses.append(fifth_code)
                    self.Saved_responses.append(sixth_code)
                    return first_code
                else:
                    self.Current_code = self.generate_random_code(colors)
                return self.Current_code
            # Otherwise, keep guessing colors
            else:
                guess = self.guess_colors(colors,scsa,board_length)
                self.Current_code = guess
                return self.Current_code
        
        # Begin checking individual pegs nce all colors are found
        if self.Found_all_colors == True:
            self.All_codes_attempted_two_color[self.Current_code] = [last_response[0], last_response[1]]
            self.All_codes_attempted.append([self.Current_code, last_response[0], last_response[1]])
            self.All_codes_attempted_backup.append([self.Current_code, last_response[0], last_response[1]])
            
            # Complete SCSA specific strategies or go into peg checking cycle
            if scsa == "TwoColorAlternating" or scsa == "mystery5":
                return self.Saved_responses[0]
            elif scsa == "mystery2":
                self.Current_code = self.Saved_responses[0]
                self.Saved_responses.remove(self.Current_code)
                return self.Current_code
            elif scsa == "ABColor" or scsa == "TwoColor" or self.count_number_of_colors() == 2:
                sort = sorted(self.All_colors.items(),key=lambda x:x[1])
                max_col = sort[-1][0]
                other_col = sort[-2][0]
                self.Current_code = self.twocolor_problem(board_length, last_response, max_col, other_col)
                return self.Current_code
            else:
                self.constraint_elimination()
                colors_found = self.colors_found()
                Max_peg = max(self.All_colors, key=self.All_colors.get)

                # Making random guesses until a optimal amount of bulls
                # is found. based on the heuristic function ((board_length - colors_found)/5)-1).
                if last_response[0] > int(((board_length - colors_found)/5)-1) and self.Found_more_than_one == False:
                    self.Found_more_than_one = True # Initiate peg checking
                    self.All_codes_attempted.append([self.Current_code, last_response[0], last_response[1]])
                    self.All_codes_attempted_backup.append([self.Current_code, last_response[0], last_response[1]])
                elif last_response[0] >= 0 and self.Found_more_than_one == False:
                    self.Current_code = self.generate_random_code(colors)
                    return self.Current_code


                # Once we find the desired # of bulls we will delete one peg at a time
                # In the process we will save each response and # of bulls in order to 
                # retrieve the information about correct pegs.
                # Ex: [['CDDCG', 3, 2, 0],
                #      ['FDDCG', 2, 2, 1],
                #      ['FFDCG', 1, 2, 2],
                #      ['FFFCG', 0, 2, 3]]
                if self.Counter != board_length and self.Found_more_than_one == True:
                    self.All_codes_attempted.remove([self.Current_code, last_response[0], last_response[1]])
                    self.All_codes_attempted_backup.remove([self.Current_code, last_response[0], last_response[1]])
                    self.Saved_responses.append([self.Current_code, last_response[0], last_response[1], self.Counter])

                    # If all bulls are found stop the peg checking cycle
                    if last_response[0] - colors_found == 0:
                        self.Counter = board_length
                    Current_code_list = list(self.Current_code)

                    # Before changing the state check if Deciphered_code has any found pegs.
                    # If there are any change it to Max_peg to avoid checking the same peg 
                    # multiple times.
                    for i in range(len(self.Deciphered_code)):
                        if self.Deciphered_code[i] != '0':
                            Current_code_list[i] = Max_peg
                            
                    # Check the next peg based on self.Counter
                    for i in range(self.Counter, len(Current_code_list)):
                        if Current_code_list[i] != Max_peg:
                            Current_code_list[i] = Max_peg
                            self.Counter = i
                            break
                        elif i == board_length - 1:
                            self.Counter = board_length
                    
                    # Place found pegs back into the code
                    for i in range(len(self.Deciphered_code)):
                        if self.Deciphered_code[i] != '0':
                            Current_code_list[i] = self.Deciphered_code[i]
                    self.Current_code = ''.join(Current_code_list)
                    return self.Current_code
                
                # Once all pegs have been checked, review saved responses to identify correct pegs
                else:
                    self.All_codes_attempted.remove([self.Current_code, last_response[0], last_response[1]])
                    self.All_codes_attempted_backup.remove([self.Current_code, last_response[0], last_response[1]])   
                    
                    # There are five possible cases:
                    # Case 1: If bulls(next response)>bulls(prev response) and we have the same # of cows, we found a new bull in the next response
                    # Case 2: If bulls(next response)<bulls(prev response), the peg that was changed in the previous guess
                    # Case 3: If bulls(next response)>bulls(prev response) and we have 2 less cows in the next repsonse 
                    # (you moved a color to the right peg and you lost a color by replacing it), then we found a new bull in the position changed
                    # Case 4: If bulls(next response)>bulls(prev response), and we have cows -1, we found a new bull
                    # Case 5: If cows(next response) == cows(prev response) -1, we know the color in the position changed belongs elsewhere
                    for save in range(1, len(self.Saved_responses)):
                        if self.Saved_responses[save][1] > self.Saved_responses[save-1][1] and self.Saved_responses[save][2] == self.Saved_responses[save-1][2]:
                            self.Deciphered_code[self.Saved_responses[save][3]] = Max_peg
                        elif self.Saved_responses[save][1] < self.Saved_responses[save-1][1]:
                            self.Deciphered_code[self.Saved_responses[save][3]] = self.Saved_responses[0][0][self.Saved_responses[save][3]]
                        elif self.Saved_responses[save][1] > self.Saved_responses[save-1][1] and self.Saved_responses[save][2] == self.Saved_responses[save-1][2] - 2:
                            self.Deciphered_code[self.Saved_responses[save][3]] = Max_peg
                        elif self.Saved_responses[save][1] > self.Saved_responses[save-1][1] and self.Saved_responses[save][2] == self.Saved_responses[save-1][2] - 1:
                            self.Deciphered_code[self.Saved_responses[save][3]] = Max_peg
                        elif self.Saved_responses[save][2] == self.Saved_responses[save-1][2] - 1:
                            if self.Saved_responses[0][0][self.Saved_responses[save][3]] in self.Constraints[self.Saved_responses[save][3]]:
                                self.Constraints[self.Saved_responses[save][3]].remove(self.Saved_responses[0][0][self.Saved_responses[save][3]])

                    # If self.Deciphered_code contains first or last peg
                    # replace the other one
                    if scsa == 'FirstLast':
                        if self.Deciphered_code[0] != '0':
                            self.Deciphered_code[-1] = self.Deciphered_code[0]
                        elif self.Deciphered_code[-1] != '0':
                            self.Deciphered_code[0] = self.Deciphered_code[-1]
                    
                    # Reinitialize variables for the next cycle
                    self.Counter = 0
                    self.Saved_responses = []
                    self.constraint_elimination()
                    self.Found_more_than_one = False
                    self.update_All_codes_attempted()          
                    self.update_deciphered_from_constraints()
                    
                    self.Current_code = self.generate_random_code(colors)
                    return self.Current_code