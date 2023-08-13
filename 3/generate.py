import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
     
        set1 = set()
        for var in self.domains:
            for word in self.domains[var]:
                if var.length== len(word):
                    set1.add(word)
            self.domains[var] = set1
            set1 = set()

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        second_bool = False
        bool = True
        if self.crossword.overlaps[x,y] != None:
            celli, cellj = self.crossword.overlaps[x,y] 
            for word in self.domains[x].copy():
                bool = True
                
                char = word[celli]              #BURALARI TEKRAR GÖZDEN GEÇİR 
                    
                for word2 in self.domains[y].copy():
                    if word2[cellj] == char:
                        bool = False
                        break
                if bool:
                    self.domains[x].remove(word) #BURALARI TEKRAR GÖZDEN GEÇİR
                    second_bool = True
                
             
            return second_bool
        else:                  
            return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
      
        queue = []
        if arcs == None:
            for x in self.domains:
                for y in self.domains:
                    if x!=y:
                        queue.append((x,y))
        else:
            queue = arcs
        while queue :
            x,y = queue.pop(0) 
            if self.revise(x,y) == True:
                if self.domains[x] == {}: #ya da {} duruma göre bak
                    return False
                for z in self.crossword.neighbors(x): 
                    queue.append((x,z))
        return True  
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        if assignment == {}:
            return False
        
        if len(assignment) != len(self.domains) :
            return False
        else:
               return True
            
  

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        bool = True
        word_list = []
        for var in assignment:
            
            for neighbor in self.crossword.neighbors(var):
                if self.revise(var,neighbor) == False: #BURADAN EMİN DEĞİLİM TEKRAR BAK
                    continue
                else:
                    
                    return False
        
           
            
            if len(assignment[var]) != var.length:
                    
                return False
            if assignment[var] in word_list:
                
                return False
            else:
                    
                word_list.append(assignment[var])
        return True    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        list_of_words = list(self.domains[var])
        dico = {}
        for k in range (len(self.domains[var])):
            
            for v in self.crossword.neighbors(var):
                for value in self.domains[v]:
                
                    celli, cellj = self.crossword.overlaps[var,v]
                    if var.direction == "down":
                        
                        char1 = list_of_words[k][celli - var.i]
                        char2 = value[cellj-v.j]
                    else:
                        char1 = list_of_words[k][cellj - var.j]
                        char2 = value[celli-v.i]
                    
                    if value == list_of_words[k]:
                        if dico[list_of_words[k]] == None:
                            dico[list_of_words[k]] = 1
                        else:
                            dico[list_of_words[k]] += 1
                    if char1 !=char2:
                        if dico[list_of_words[k]] == None:
                            dico[list_of_words[k]] = 1
                        else:
                            dico[list_of_words[k]] += 1
        temp_list = []
        for round in range (len(dico)):
            min_value = min(dico.values())
            for elem in dico:
                if dico[elem] == min_value:
                    temp_list.append(elem)
                    dico.pop(elem)
        return temp_list
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        temp_list = []
        min = 1000
        current_elem = None
    
        for var in self.domains:
            
            # BURAYA DİKKAT
            
            if var not in assignment:
                
                
                if len(self.domains[var])<min:
                    
                    min = len(self.domains[var])
                    current_elem = var
                    
                if len(self.domains[var]) == min:
                    
                    
                   
                    
                    if len(self.crossword.neighbors(current_elem)) < len(self.crossword.neighbors(var)):
                        current_elem = var 
                        
                
        return current_elem           
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.domains[var]:
            assignment[var] = value
            
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                
                if result != None:
                    
                    return assignment
            else:
                
                assignment.pop(var)
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
