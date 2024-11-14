import multiprocessing
import random

if __name__ == '__main__':
    # Set the seed.
    random.seed(42)
    print(random.randint(1, 100))

    # Init local vars.
    maximum = 0
    max_cores = multiprocessing.cpu_count() - 1

    # Ask the user for the number of threads/cores.
    no_threads = 0
    while True:
        try:
            no_threads = int(
                input(f"Hey user! Enter the number of threads you would like to use between 1 and {max_cores}: "))
            if 1 <= no_threads <= max_cores:
                break
            else:
                print(f"Invalid range. Please enter a number between 1 and {max_cores}.")
        except ValueError:
            print("Error! That wasn't a number. Please enter a valid number.")
    print(f"You have chosen {no_threads} threads.")

    # Ask the user how many elements they would like to generate.
    elements = 0
    while True:
        try:
            elements = int(
                input("How many elements would you like to generate? Minimum 20: "))
            if elements >= 20:
                break
            else:
                print("Invalid range. Please enter a number higher than or equal to 20.")
        except ValueError:
            print("Error! That wasn't a number. Please enter a valid number.")
    print(f"The program will generate {elements} elements.")

    # Ask the user to put a bounds on the elements.
    while True:
        try:
            min = int(
                input(f"What should be the minimum value in this array? It must be at LEAST 0: "))
            if min >= 0:
                break
            else:
                print("Invalid range. Please enter a number higher than or equal to 0.")
        except ValueError:
            print("Error! That wasn't a number. Please enter a valid number.")