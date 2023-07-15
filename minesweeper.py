import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i,j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mine_set = set()
        for cell in self.cells:
            if self.count == len(self.cells):
                mine_set.add(cell)
        return mine_set
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe_set = set()
        for cell in self.cells:
            if self.count == 0 :
                safe_set.add(cell)
        
        return safe_set
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            print("removed cell: "+  str(cell)+ " from sentence before : " +str(self.cells)  + "=" + str(self.count))
            self.cells.remove(cell)
            self.count -=1
            print("sentence after : " +str(self.cells)  + "=" + str(self.count))

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
 


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        print("cell added as mine: " + str(cell))
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
       
        i,j = cell 
        sentence_set = set()
        for h in range (0,3):
            for k in range (0,3):
                new_cell = i-1+h,j-1+k
                if not (h == 1 and k == 1) and new_cell not in self.moves_made  and i-1+h>=0 and i-1+h<=7 and j-1+k>=0 and j-1+k<=7 :
                    if new_cell in self.mines:
                        count = count -1
                        continue
                    sentence_set.add(new_cell)
        sentence = Sentence(sentence_set,count)
        
        if sentence in self.knowledge:
                self.knowledge.remove(sentence)
        self.knowledge.append(sentence)
        extra_knowledge_list = []
        for know in self.knowledge: 
            
            if know.cells.issubset(sentence.cells) and know.cells != sentence.cells:
                extra_cells = sentence.cells - know.cells 
                extra_count = sentence.count-know.count
                extra_knowledge = Sentence(extra_cells,extra_count)
                if extra_knowledge not in extra_knowledge_list:
                    extra_knowledge_list.append(extra_knowledge)
                    print("this is extra knowledge" + str(extra_knowledge))
            if sentence.cells.issubset(know.cells) and know.cells != sentence.cells:    
                extra_cells2 = know.cells-sentence.cells
                extra_count2 = know.count-sentence.count
                extra_knowledge2 = Sentence(extra_cells2,extra_count2)
                if extra_knowledge2 not in extra_knowledge_list:
                    extra_knowledge_list.append(extra_knowledge2)
                    print("this is extra knowledge2" + str(extra_knowledge2))
            
        self.knowledge = self.knowledge + extra_knowledge_list        
               
                
        
        for know2 in self.knowledge:                 #BURA TEHLIKELİ BURAYA BAK TEKRAR
            safe_set = know2.known_safes()
            mine_set = know2.known_mines()
            for cell2 in safe_set:
                print("adding this new safe cell: " + str(cell2))
                self.mark_safe(cell2)
                
            for cell3 in mine_set:
                self.mark_mine(cell3)
               
        print("These are known mines:" + str(self.mines))
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("these are unplayed safe moves:"  + str(self.safes - self.moves_made))
        if len(self.safes) == 0:
            return None
        
        for safe_move in self.safes:
            
            if safe_move not in self.moves_made:
                return safe_move 
        return None
    

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.moves_made) == 81:
            return None
        total_moves = set()
        for i in range (8):
            for j in range(8):
                total_moves.add((i,j))
                
        total_moves = total_moves - self.moves_made   
        total_moves = total_moves - self.mines 
        if len(total_moves) == 0:
            return None  
        return total_moves.pop()
