from tkinter import *
from tkinter import ttk
import multiprocessing
import random
import time
import numpy
import math

class CountSort:
    
    def __init__(self, root):
        root.title("Counting Sort Program: Threaded vs. Unthreaded")

        # Create a "content frame" or "frame widget".
        mainframe = ttk.Frame(root, padding="10 10 10 10")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create the entry widgets.

        self.number_of_threads = StringVar()
        thread_entry = ttk.Entry(mainframe, width=10, textvariable=self.number_of_threads)
        thread_entry.grid(column=0, row=0, sticky=(N,W))

        def update_label(event=None):
            element_label['text'] = f"# of elements (minimum 20): {self.number_of_elements.get()}"

        self.number_of_elements = StringVar()
        element_entry = ttk.Entry(mainframe, width=10, textvariable=self.number_of_elements)
        element_entry.grid(column=1, row=0, sticky=(N,W))
        element_entry.bind("<Return>", update_label)

        self.max_cores = multiprocessing.cpu_count() - 1

        # Variable label.
        self.thread_label_var = f"# of threads (minimum 1, maximum {self.max_cores}) "

        # Create the labels.
        thread_label = ttk.Label(mainframe, text=self.thread_label_var, wraplength=100)
        thread_label.grid(column=0, row=1, padx=5, pady=5, sticky=(N))

        element_label = ttk.Label(mainframe, text=f"# of elements (minimum 20)", wraplength=100)
        element_label.grid(column=1, row=1, padx=5, pady=5, sticky=(N,W))

        # Create a button for generating arrays.
        style = ttk.Style()
        style.configure("Custom.TButton",
                        font=("Helvetica", 16),
                        padding=(20,20))
        button = ttk.Button(mainframe, text="GENERATE", command=self.generate, style="Custom.TButton")
        button.grid(column=0, row=2, columnspan=2, sticky=(W, E))

        # Create a text area for storing output.
        text_area = Text(mainframe, height=10, width=100, wrap="word")
        text_area.grid(row=0, column=2, rowspan=3, sticky="n")
        text_area.insert('1.0', 'This is where you will see the generated and sorted array.')
        text_area.configure(font=('Consolas', 10))

        # Create a Scrollbar widget
        scrollbar = ttk.Scrollbar(mainframe, orient="vertical", command=text_area.yview)
        scrollbar.grid(row=0, column=3, rowspan=3, sticky="ns")
        text_area['state'] = 'disabled'

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        thread_entry.focus()
        # root.bind("<Return>", self.calculate)

    def CountThreadFunc(self, chunk, max_value):
        local_count = numpy.zeros(max_value + 1, dtype=int)
        for num in chunk:
            local_count[num] += 1
        return local_count

    # This code was made possible by Harshita Gupta!
    def CountSortThreaded(self, in_list, procs):
        # Step 1: find the maximum value in the array.
        max_value = max(in_list)

        # Step 2: Split the array into chunks for each process.
        chunk_size = math.ceil(len(in_list) // procs)            # Round up to let the last process consume any leftovers
        chunks = []
        for i in range(procs):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            chunk = in_list[start:end]
            chunks.append(chunk)
        
        # Step 3: Create a multiprocessing pool and pass arguments.
        with multiprocessing.Pool(processes=procs) as pool:
            #parallel counting
            partial_counts = pool.starmap(self.CountThreadFunc, [(chunk, max_value) for chunk in chunks])

        # Step 4: Aggregate the counts from every process.
        total_count = numpy.zeros(max_value + 1, dtype=int)
        for count in partial_counts:
            total_count += count

        # Step 5: Construct a sorted array from the total counts.
        sorted_array = []
        for num, count in enumerate(total_count):
            sorted_array.extend([num] * count)

        return sorted_array

    # This code was made possible by Janhavi Tatkare!
    def CountSortRegular(self, in_list):
        # Step 1: find the maximum value in the array.
        max_val = max(in_list)

        # Step 2: initialize the count array.
        count_list = [0] * (max_val + 1)

        # Step 3: Count occurrences of each element.
        for num in in_list:
            count_list[num] += 1

        # Step 4: Accumulate the counts.
        for i in range(1, len(count_list)):
            count_list[i] += count_list[i - 1]

        # Step 5: Place elements into the sorted array.
        output_list = [0] * len(in_list)
        for num in reversed(in_list):           # To make it a stable sort, iterate in reverse.
            output_list[count_list[num] - 1] = num
            count_list[num] -= 1

        return output_list

    def identityCheck(self, arr1, arr2):
        if (arr1 == arr2):
            return 0
        return 1

    def getUserInput(self):
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

        # Make an input array based on min and max.
        input_list = []

        for _ in range(0, no_elements, 1):
            input_list.append((random.randrange(min, max + 1)))

        return input_list, no_threads

    def generate(self):
        while True:
            # Set the seed.
            random.seed(42)
            # print(random.randint(1, 100))

            # Introduction.
            print("Welcome to the Regular VS. Parallel Counting Sort Program!")
            print("Enter exit to quit the program or press enter")
            exit_input=input("Do you want to quit or continue?").strip()
            if exit_input.lower()=="exit":
                print("Thanks for coming!\n")
                break

            # Get user input.
            list_and_threads = self.getUserInput()
            returned_list = list_and_threads[0]
            num_threads = list_and_threads[1]

            if len (returned_list) == 0:
                print("Empty array, nothing to sort.")
                print("\nRUNNING AGAIN...\n")
                continue

            start_time = time.time()
            output1 = self.CountSortRegular(returned_list)
            end_time = time.time()

            print("\n==========REGULAR COUNTSORT==========\n")

            # print("ORIGINAL ARRAY: ", returned_list)
            # print("SORTED ARRAY: ", output)
            print(f"Time taken for regular countsort: {(end_time - start_time)}")

            print("\n==========THREADED COUNTSORT==========\n")

            # Build thread arguments and call threads.
            start_time = time.time()
            output2 = self.CountSortThreaded(returned_list, num_threads)
            end_time = time.time()
            # print("ORIGINAL ARRAY: ", returned_list)
            # print("SORTED ARRAY: ", output)
            print(f"Time taken for threaded countsort: {(end_time - start_time)}")

            if (self.identityCheck(output1, output2) == 0):
                print("The arrays are identical!")
            else:
                print("ERROR! The arrays are not identical! Something's wrong!")

            print("\nRUNNING AGAIN...\n")

# Set up the window.
root = Tk()
CountSort(root)
root.mainloop()
