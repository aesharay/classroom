# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:17:28 2020

@author: aesha
"""

###########################################################
    #Computer Project #11
    # Student Class
        # Places student in classroom
        # Adds and removes items from student backpack
    # Classroom Class
        # Represents a single classroom at a time
        # Directions to other rooms
        # Interact with objects in room
    # Rush Class
        # User interaction with student and rooms
        # Interacts with items in student's backpack
        # Moves student
    # main function
###########################################################

#DO NOT DELETE THis LINES
MAP = {"U":"Up","D":"Down","L":"Left","R":"Right"}

class Student(object):
    '''A student knows the id of the room they are currently in, and has a list of its inventory'''
    
    def __init__(self, item_list=None, classroom_id=-1):
        '''Initializes yourself, with an empty backpack by default. The default position of the student is room -1.'''

        if item_list == None:
            self.backpack = []
        else:
            self.backpack = item_list
        self.classroom_id = classroom_id

    def __repr__(self):
        '''Returns a string representation of the student.'''
        return self.__str__()

    def __str__(self):
        '''Returns a string representing the student's inventory.'''
        s = "Backpack: "
        if len(self.backpack) == 0:
            s += "Empty"
        else:
            for item in self.backpack:
                s += item + ", "
            else:
                s = s[:-2] # remove trailing comma and space
        return s

    def __eq__( self, S ):
        '''Return True if self and S objects are equal, else return False'''
        if self.classroom_id == S.classroom_id and self.backpack == S.backpack:
            return True
        else: 
            return False

    def place(self, classroom_id):
        '''Place student in classroon'''
        self.classroom_id = classroom_id #identify classroom
    
    def add_item(self, item):
        '''Add items into student's backpack, unless it is full'''
        if len(self.backpack) < 6: #check for number of items in backpack
            self.backpack.append(item)
        else:
            print("Backpack is full.") #already items in backpack

    def remove_item(self, item):
        '''Removes duplicate items from the backpack'''
        if item in self.backpack: #checks if item is in backpack
            self.backpack.remove(item)
        else:
            print("Failed to remove item from backpack.") #item was not in backpack


class Classroom(object):
    '''Represents a single classroom at a time, and gives directions to other rooms'''
    
    def __init__(self, text_desc="0 empty"):
        '''Initialzes a classroom. By default it has id 0 and is a "empty" room with no inventory or exits.'''
        description = text_desc.split()

        self.id = int(description[0])
        self.course = description[1]

        # Initialize a dictionary of potential exits as empty
        self.exits = {}

        # Initialize a "backpack" of items as empty list
        self.backpack = []
        
        #ADD YOUR CODE HERE
        for i in range(2, len(description)):
            if description[i][0] in MAP: #check if direction exists in MAP
                self.exits[description[i][0]] = int(description[i][1:])
            else:
                self.backpack.append(description[i]) #add descripton to backpack
            
    def __repr__(self):
        '''Returns a string representation of the classroom.'''
        classroom_repr = '''Classroom("''' + repr(self.id) + " " + self.course

        for direction in self.exits:
            classroom_repr += " {}".format(direction) + repr(self.exits[direction])

        for item in self.backpack:
            classroom_repr += " " + item

        classroom_repr += '''")'''

        return classroom_repr

    def __str__(self):
        '''Returns a string representing the room in a nice conversational style.'''

        # Basic classroom description
        classroom_str = "You see a " + self.course + " classroom."

        # List the things in the classroom
        if len(self.backpack) == 1:
            classroom_str += " On the desk you see a " + \
                             self.backpack[0] + "."
        if len(self.backpack) == 2:
            classroom_str += " On the desk you see a " + \
                             self.backpack[0] + \
                             " and a " + self.backpack[1] + "."
        elif len(self.backpack) > 2:
            classroom_str += " On the desk you see "
            for item in self.backpack[:-1]:
                classroom_str += "a " + item + ", "
            classroom_str += "and a " + self.backpack[-1] + "."

        # List the exits
        if len(self.exits) == 0:
            classroom_str += " Run through the classroom grab what you need (if possible). Exit and run to the exam!"
        elif len(self.exits) == 1:
            classroom_str += " Run through the classroom grab what you need (if possible). Now, run into the hallway and go " + \
                             MAP[list(self.exits.keys())[0]] + "."
        elif len(self.exits) == 2:
            classroom_str += " Run through the classroom grab what you need (if possible). Now, run into the hallway and go " + \
                             MAP[list(self.exits.keys())[0]] + " or " + MAP[list(self.exits.keys())[1]] + "."
        elif len(self.exits) > 2:
            classroom_str += " Run through the classroom grab what you need (if possible). Now, run into the hallway and go "
            for direction in list(self.exits.keys())[:-1]:
                classroom_str += MAP[direction] + ", "
            classroom_str += "or " + MAP[list(self.exits.keys())[-1]] + "."

        return classroom_str
    
    def __eq__( self, C ):
        '''Return True if self and C objects are equal, else return False'''
        if self.id == C.id and self.course == C.course and self.backpack == C.backpack and self.exits == C.exits:
            return True
        else: 
            return False
    
    def add_item(self, item):
        '''Add item to classroom's back.'''
        self.backpack.append(item)

    def remove_item(self, item):
        '''Removes duplicate items from the backpack'''
        if item in self.backpack:
            self.backpack.remove(item) #add item if not in backpack
        else:
            print("Failure to find the item in the classroom.") #error if item not in class, or already in backpack
        
    def get_room(self, direction):
        '''Returns the room id in the given direction, or return false'''
        if direction in self.exits:
            return self.exits[direction]
        else:
            return False
    
    
class Rush(object):
    ''' responsible for interactions between the user, the character, and the rooms'''

    def __init__(self, filename="rushing.txt"):
        '''Initializes the student rushing to class.  The student starts in the classroom with the lowest id.'''

        # First make a student start with an empty inventory
        self.student = Student()

        # Create classrooms are an empty dictionary
        self.classrooms = {}
        

        file = open(filename, 'r') #opens file
        for line in file:
            lines = line.split()
            self.classrooms[int(lines[0])] = Classroom(line)
        
        # Place the student in the room with lowest id
        self.student.place(min(self.classrooms.keys()))

    def __repr__(self):
        '''Returns a string representation.'''

        return self.__str__()

    def __str__(self):
        '''Returns a string representing the journey to the class, simply giving the number of rooms.'''
        search_str = "You are searched in "
        if len(self.classrooms) == 0:
            search_str += "no classrooms at all, you are in the hallway. You are late run in a random class and get items from the desks."
        elif len(self.classrooms) == 1:
            search_str += "a classroom."
        else:
            search_str += "a set of " + str(len(self.classrooms)) + \
                          " classrooms."

        return search_str

    def intro(self):
        '''Prints an introduction to the search for items because you are late
        This prompt includes the commands.'''
        print("\nAHHHH! I'm late for class\n")
        print("*runs out the house to catch the bus with an empty backpack*")

        print("\nYou're popular and have friends in many classes. Find and collect any items you find useful for your exam.")
        print("You are already late, and have a CSE231 Final Exam in 10 mins.\n")
        self.print_help()


    def print_help(self):
        '''Prints the valid commands.'''
        print("Use your instincts: ")
        print("*thinks*.. *thinks*.. what to do?!?!?!?!")
        print("*running*")
        print("S or search -- prints a description of the classroom you ran into")
        print("B or backpack - prints a list of items in your backpack")
        print("P pencil or pickup pencil - *mental* instruction to pick up an item called pencil")
        print("DR pencil or drop pencil - *mental* instruction to drop off an item called pencil")
        print("U or up - *mental* instruction to up the hallway to find another classroom")
        print("D or down - *mental* instruction to down the hallway to find another classroom")
        print("R or right - *mental* instruction to right in the hallway to find another classroom")
        print("L or left - *mental* instruction to left in the hallway to find another classroom")
        print("G or giveup - I have no more time, I need to get to class!!!")
        print("H or help - prints this list of options again")
        print()
        print("Remember that uppercase and lowercase SHOULD NOT matter. ")
        print("JUST GRAB WHAT YOU NEED AND GET TO CLASS TO START YOUR FINAL EXAM!!! HURRYYYY!!!")
        print()

    def prompt(self):
        '''Prompts for input and handles it, whether by error message or handling a valid command.
        Returns True as long as the user has not chosen to quit, False if they have.'''

        print("In room {} with course {}".format(self.student.classroom_id,self.classrooms[self.student.classroom_id].course))
        print(self.student)
        user_input = input("Enter a command (H for help): ")
        print()

        # Handle input: split for pickup/drop, capitalization unimportant for commands
        input_list = user_input.split()

        if len(input_list) == 0:
            user_input = "?"  # No command is not a valid command
            return False
        else:
            try:
                command = input_list[0].upper()  # The command
                if len(input_list) > 1:
                    item = input_list[1]
                if command == 'S':
                    self.search()
                elif command == 'B':
                    self.backpack()
                elif command == 'P':
                    self.pickup(item)
                elif command == 'DR':
                    self.drop(item)
                elif command in "UDLR":
                    self.move(command)
                elif command == 'G':
                    print("I have no more time, I need to get to class!!!")
                    return False
                elif command == 'H':
                     self.print_help() 
                else:
                    print("Unfortunately, that's not a valid option.")
                    return False
            except:
                print("Problem with the option or the item.")
                return False
        if self.win():
            return "win"
        return True

    def search(self):
        '''Prints the description of the current room.'''
        
        current_classroom = self.classrooms[self.student.classroom_id]
        print(current_classroom)

    def backpack(self):
        '''Prints items in student's backpack'''

        print(self.student)
        
    def pickup(self, item):
        '''Add classroom item to student's backpack, else return error'''
        c_back = self.classrooms[self.student.classroom_id] #defines class
        s_back = c_back.backpack[:] #shallow copy
        c_back.remove_item(item)
        
        if s_back != c_back.backpack: #if student backpack does not have class item
            self.student.add_item(item) #add item
    
    def drop(self, item):
        '''Remove item from student's backpack, and place it in classroom.'''

        backpack_item = self.classrooms[self.student.classroom_id] #defines class
        shallow = self.student.backpack[:] #shallow copy
        self.student.remove_item(item)

        if shallow != self.student.backpack: #if shallow doesnt match student backpack
            backpack_item.add_item(item) #add item
            
    def move(self, direction):
        '''Moves the student in the specified direction, else prints error'''
    
        class_direction = self.classrooms[self.student.classroom_id] #define class
        
        if class_direction.get_room(direction): #if direction is true
            self.student.place(class_direction.get_room(direction))
            print("You went " + MAP[direction] + " and found a new classroom.") #move student to class
        else: 
            errMsg = "Unfortunately, you went " + MAP[direction] + " and there was no classroom." #error for wrong direction
            print(errMsg)

    def win(self):
        '''Checked if student enters classroom and has the right materials, otherwise return False'''
        winning_backpack = ['cheatsheet', 'eraser', 'paper', 'pencil']
    
        classroom = self.classrooms[self.student.classroom_id] #define class
        
        backpack = self.student.backpack #define backpack
        backpack_shallow = backpack[:] #shallow copy
        backpack_shallow.sort() #sort backpack
        
        if 'CSE231' in str(classroom) and backpack_shallow == winning_backpack: #if class is CSE and backpack is same as winning backpack
            return True #return true
        return False
               
def main():
    '''
    Prompts the user for a file, then plays that file until the user chooses to give up.
    Does not check formatting of input file.
    '''

    while True:
        try:
            filename = input("Enter a text filename: ")
            escapade = Rush(filename)
            break
        except IOError:
            print("Cannot open file:{}. Please try again.".format(filename))
            continue
    
    escapade.intro()
    escapade.__str__()
    escapade.search()
    
    keep_going = True
    while keep_going:
        keep_going = escapade.prompt()
        if keep_going == 'win':
            break
    if keep_going == 'win':
        print("You succeeded!")
    else:
        print("Thank you for playing")

if __name__ == "__main__":    
    main()