# Task 4: Closure Practice


def make_hangman(secret_word):
    guesses = []
    
    def hangman_closure(letter):
        #Within the inner function, each time it is called, the letter should be appended to the guesses array. 
        guesses.append(letter.lower())

        # build the string
        display_word = ""
        all_guessed = True

        for char in secret_word:
            if char.lower() in guesses:
                display_word += char
            else:
                display_word += "_"
                all_guessed = False

        print(display_word)
        return all_guessed
    
    return hangman_closure


# mainline code to play the game
if __name__ == "__main__":
    word_to_guess = input("Enter the secret word: ").strip()

    # initialize the hangman closure with the secret word
    play_round = make_hangman(word_to_guess)

    # make sure it takes one character at a time and keeps asking for guesses until the word is fully guessed
    is_solved = False

    print(f"\nGame started! the word has {len(word_to_guess)} letters.")

    while not is_solved:
        guess = input("Enter a letter to guess: ").strip()

        if len(guess) != 1:
            print("Please enter only one letter.")
            continue

        is_solved = play_round(guess)

    print(f"Congratulations! You've guessed the word '{word_to_guess}'!")