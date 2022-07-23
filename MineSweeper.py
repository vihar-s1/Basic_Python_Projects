#!/usr/bin/env python

from os import system
import random, sys, time
from typing import final

#! MACROS
DIMENSION = 10
NUMBER_OF_BOMBS = 10


class ClosedGameError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return super().__str__()
    
def clrscr():
    if sys.platform.startswith('win32'):
        system("cls")
    else: # sys.platform.startswith('linux') or sys.platform.startswith('darwin'): # darwin represents macOS
        system("clear")
        
def pause():
    if sys.platform.startswith('win32'):
        system('pause')
    else: # sys.platform.startswith('linux') or sys.platform.startswith('darwin'): # darwin represents macOS
        system('read -s -n 1 -p "Press any key to continue..."')
    
class Board:
    def __init__(self, dimension, no_of_bombs) -> None:
        self.__dimension = dimension
        self.__no_of_bombs = no_of_bombs
        self.__flagged = set()
        self.__safe_dig_sites = self.__dimension**2 - self.__no_of_bombs
        self.__board = None
        self.__bomb_list = list()
        # Sites already dug --> contains tuples of row and col number of sites
        self.__dug = set()
        self.make_new_board()
        
    def get_dimension(self):
        return self.__dimension
    
    def dug_sites_count(self):
        return len(self.__dug)
    
    def safe_dig_sites_count(self):
        return self.__safe_dig_sites
    
    def remaining_flags(self):
        return self.__no_of_bombs - len(self.__flagged)

    def make_new_board(self):
        self.__game_closed = False
        self.__board = [[None for i in range(self.__dimension)]for j in range(self.__dimension)]

        # Assigning bombs on the board randomly
        remaining_bombs = self.__no_of_bombs
        while remaining_bombs > 0:
            row = random.randint(0, self.__dimension - 1)
            col = random.randint(0, self.__dimension - 1)

            if self.__board[row][col] != '*':
                self.__board[row][col] = '*'
                self.__bomb_list.append((row, col))
                remaining_bombs -= 1

        # Assigning values to the remaining locations based on the neighouring bombs
        for row in range(self.__dimension):
            for col in range(self.__dimension):
                if self.__board[row][col] == '*':
                    continue
                else:
                    self.__board[row][col] = 0

                # iterating through neighbouring cells ranging from (row-1,col-1) to (row+1, col+1) excluding (row,col)
                for i in range(max(0, row-1), min(self.__dimension, (row+1) + 1)):
                    for j in range(max(0, col-1), min(self.__dimension, (col+1) + 1)):
                        if i != row or j != col:  # i = row and j = col represents to current box
                            if self.__board[i][j] == '*':
                                self.__board[row][col] += 1


    def dig(self, row: int, col: int) -> bool:
        if self.__game_closed:
            return False

        self.__dug.add((row, col))  # Site has been dug
        if (row, col) in self.__flagged:
            self.__flagged.remove((row, col))

        if self.__board[row][col] == '*':  # ! DIG SITE HAD A BOMB
            return False
        elif self.__board[row][col] > 0:  # . Has neighbouring bombs
            return True

        # dig site value self.board[row][col] == 0

        # (row, col) has value 0 so no neighbouring bombs are there.
        # hence all neighbouring sites must either have a zero value or non-zero value.
        # non-zero value will terminate digging and zero value will again iterate through this loop.
        # Thus, no bomb is actually being dug inside this recursive loop call

        for r in range(max(0, row-1), min(self.__dimension, row+1 + 1)):
            for c in range(max(0, col-1), min(self.__dimension, col+1 + 1)):
                if (r, c) not in self.__dug:
                    self.dig(r, c)  # dig neighbouring sites where not dug

        return True

    def print_board(self):
        # All sites not dug should be hidden so visible_board != game_board
        visible_board = [[' ' for i in range(self.__dimension)] for j in range(self.__dimension)]
        for row in range(self.__dimension):
            for col in range(self.__dimension):
                if (row, col) in self.__dug:
                    visible_board[row][col] = str(self.__board[row][col])
                elif (row, col) in self.__flagged:
                    visible_board[row][col] = '?'
        
        print(end='   |')
        for i in range(self.__dimension):
            print('%3d|' % i, end='')
            
        print(('\n'+ "   " + '----'*self.__dimension) + '-')
        for index in range(self.__dimension):
            print('%-3d' % index, end='')
            print('|' ,' | '.join(visible_board[index]), '|')
            #print(('---' + '----'*self.dimension) + '-')
    
    def flag_unflag(self, row, col):
        if len(self.__flagged) < self.__no_of_bombs and (row, col) not in self.__dug:
                if (row, col) in self.__flagged:
                    self.__flagged.remove((row, col))
                else:
                    self.__flagged.add((row, col))
    
    def close_game(self):
        for bomb in self.__bomb_list:
            self.__dug.add(bomb)
            

def play(game_board: Board):
    # Step 1: Display Board and ask user for dig site
    # Step 2: if dug a bomb:
    #             Game Over
    #         else:
    #             recursive dig until next to a bomb
    # Step 3: Rpeate 2 and 3 until either all safe sites are dug or game over
    safe = True
    while safe and game_board.dug_sites_count() < game_board.safe_dig_sites_count():
        clrscr()
        game_board.print_board()
        print(f"\nFlags Left: {game_board.remaining_flags()}")
        try:
            create_flag = input("\nEnter Y/y to flag a site else press Enter: ")
            
            row = int(input("\nEnter Row: "))
            if 0 > row or row >= game_board.get_dimension():
                raise ValueError
            col = int(input("Enter Column: "))
            if 0 > col or col >= game_board.get_dimension():
                raise ValueError
        except ValueError:
            print("Invalid Value Try Again!!")
            pause()
        
        # safe is false if a bomb is dug
        if create_flag == 'Y' or create_flag == 'y':
            game_board.flag_unflag(row, col)
        else:
            safe = game_board.dig(row, col)
    
    # safe is true if all squares without bomb are dug
    # safe is false when a bomb exploded
    return safe


if __name__ == "__main__":
    game = Board(DIMENSION, NUMBER_OF_BOMBS)
    won_game = play(game)
    game.close_game()
    clrscr()
    game.print_board()
    if won_game:
        print("YOU WON!!")
    else:
        print("YOU LOST!!")
