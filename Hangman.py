#!/usr/bin/env python

import string
import words
import os

# . word --> word to be guessed by user
# . used_letters --> letters already guessed by user correctly


def display_word(word: str, used_letters: set):
    for character in list(word):
        if character in used_letters:
            print(character, end="")
        else:
            print(end="-")
    print(f"\tWord Length: {len(list(word))}")


def hangman():
    word = words.get_valid_word(words.words)

    word_letters = set(word)  # . Unguessed Wordletters
    used_letters = set()  # . Letters that user has already entered
    alphabets = set(string.ascii_uppercase)  # . all the alphabets

    lives = 10
    
    while len(word_letters) > 0 and lives > 0:
        os.system("clear")
        display_word(word, used_letters)

        print("\n\nCharacters Used:", ' '.join(used_letters))
        print(f"Remaining Lives: {lives}")
        character = input("Guess a Character: ").upper()

        if character not in alphabets:
            print(f"\n{character} is not an ALPHABET!!\n")
        if character in word_letters - used_letters:
            print("\nLetter Correctly Guessed!!\n")
            used_letters.add(character)
            word_letters.remove(character)
        elif character in used_letters:
            print(f"\nYou already guessed {character}\n")
        else:
            print("\nIncorrect Guess!! Try Again.\n")
            lives -= 1
            used_letters.add(character)

        os.system("pause")

    if lives == 0:
        print(f"You Died!! The correct Word was {word}!!")
    else:
        print(f"\nYou Successfully Guessed {word}!!")


hangman()
