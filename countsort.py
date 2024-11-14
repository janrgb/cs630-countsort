import multiprocessing
import random
import time


def CountThreadFunc(in_list, cnt_dict):
    # TODO: implement CountThreadFunc
    pass

def CountSortThreaded(in_list, cnt_dict, out_list, minimum, maximum):
    # TODO: implement CountSortThreaded
    pass

def CountSortRegular(in_list, cnt_dict, out_list, minimum, maximum):
    # Loop through array looking for each value and place how many times that value appears -> countArray's position for that element
    for elem in in_list:
        cnt_dict[elem] = cnt_dict[elem] + 1

    # Prefix sum.
    for j in range(minimum + 1, maximum + 1, 1):
        cnt_dict[j] = cnt_dict[j - 1] + cnt_dict[j]

    # Iterate backwards from in_list and capture each member to place in out_list
    for j in range(len(in_list) - 1, -1, -1):
        out_list[cnt_dict[in_list[j]] - 1] = in_list[j]
        cnt_dict[in_list[j]] = cnt_dict[in_list[j]] - 1

''' Print list.
    for elem in out_list:
        print(f"{elem} ")
'''
if __name__ == '__main__':
    # Set the seed.
    random.seed(42)
    print(random.randint(1, 100))

    # Init local vars.
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
        input_list.append((random.randrange(min, max + 1)))
        output_list.append(0)

    for i in range(min, max + 1, 1):
        count_dict[i] = 0
        count_dict_th[i] = 0

    start = time.time()
    CountSortRegular(input_list, count_dict, output_list, min, max)
    end = time.time()
    print(f"Time taken for regular countsort: {(end - start)}")

    # Build thread arguments and call threads.
    start = time.time()
    CountSortThreaded(input_list, count_dict_th, output_list_th, min, max)
    end = time.time()
    print(f"Time taken for threaded countsort: {(end - start)}")