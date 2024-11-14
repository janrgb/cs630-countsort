import multiprocessing
import random
import time

def CountSortRegular():
    # TODO: implement CountSortRegular

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
    no_elements = 0
    while True:
        try:
            no_elements = int(
                input("How many elements would you like to generate? Minimum 20: "))
            if no_elements >= 20:
                break
            else:
                print("Invalid range. Please enter a number higher than or equal to 20.")
        except ValueError:
            print("Error! That wasn't a number. Please enter a valid number.")
    print(f"The program will generate {no_elements} elements.")

    # Ask the user to put a bounds on the elements.
    min = -1
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

    max = -1
    while True:
        try:
            max = int(
                input(f"What should be the maximum value in this array? It must be at LEAST {min + 1}: "))
            if max >= min + 1:
                break
            else:
                print(f"Invalid range. Please enter a number higher than or equal to {min + 1}.")
        except ValueError:
            print("Error! That wasn't a number. Please enter a valid number.")
    print(f"The program will generate {no_elements} elements between {min} and {max}, inclusive.")

    # Make an input/output array and count dictionary based on min + max.
    input_list = []
    output_list = []
    output_list_th = []

    count_dict = {}
    count_dict_th = {}
    for i in range(0, no_elements, 1):
        input_list[i] = (random.randrange(min, max + 1))
        el = input_list[i]
        if (el > maximum):
            count_dict[maximum] = 0
            count_dict_th[maximum] = 0

    start = time.time()
    CountSortRegular(input_list, count_dict, output_list)
    end = time.time()
    print("Time taken for regular countsort: %f\n", (end - start))