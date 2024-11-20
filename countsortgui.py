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
        root.resizable(False, False)

        # Initializing styles.
        self.error_style = ttk.Style()
        self.normal_style = ttk.Style()
        self.error_style.configure("Error.TLabel", foreground="red")
        self.normal_style.configure("Normal.TLabel", foreground="black")

        # Create the entry widgets.
        self.number_of_threads = StringVar()
        thread_entry = ttk.Entry(mainframe, width=10, textvariable=self.number_of_threads)
        thread_entry.grid(column=0, row=0, sticky=(N,W))

        self.number_of_elements = StringVar()
        element_entry = ttk.Entry(mainframe, width=10, textvariable=self.number_of_elements)
        element_entry.grid(column=1, row=0, sticky=(N,W))

        self.minimum_bound = StringVar()
        minimum_entry = ttk.Entry(mainframe, width=10, textvariable=self.minimum_bound)
        minimum_entry.grid(column=0, row=2, sticky=(N,W))

        self.maximum_bound = StringVar()
        maximum_entry = ttk.Entry(mainframe, width=10, textvariable=self.maximum_bound)
        maximum_entry.grid(column=1, row=2, sticky=(N,W))

        # Calculate max_cores.
        self.max_cores = multiprocessing.cpu_count() - 1

        # Initial text.
        self.thread_label_init_text = f"# of threads (minimum 1, maximum {self.max_cores}) "
        self.element_label_init_text = f"# of elements (minimum 20)"
        self.minimum_label_init_text = f"minimum bound on elements (minimum 0)"
        self.maximum_label_init_text = f"maximum bound on elements (must be greater than min)"

        # Create the labels. We make them available in the class for error updating.
        self.thread_label = ttk.Label(mainframe, text=self.thread_label_init_text, wraplength=100)
        self.thread_label.grid(column=0, row=1, sticky=(N))

        self.element_label = ttk.Label(mainframe, text=self.element_label_init_text, wraplength=100)
        self.element_label.grid(column=1, row=1, sticky=(N))

        self.minimum_label = ttk.Label(mainframe, text=self.minimum_label_init_text, wraplength=100)
        self.minimum_label.grid(column=0, row=3, sticky=(N))

        self.maximum_label = ttk.Label(mainframe, text=self.maximum_label_init_text, wraplength=100)
        self.maximum_label.grid(column=1, row=3, sticky=(N))

        # Create a button for generating arrays.
        style = ttk.Style()
        style.configure("Custom.TButton",
                        font=("Helvetica", 16),
                        padding=(20,20))
        button = ttk.Button(mainframe, text="GENERATE", command=self.generate, style="Custom.TButton")
        button.grid(column=0, row=4, columnspan=2, sticky=(W, E))

        # Create a separate frame to house the scrollbar and text area.
        subframe = ttk.Frame(root, padding=10)
        subframe.grid(row=0, column=2, rowspan=4, sticky=(N,W,E,S))
        subframe.rowconfigure(0, weight=1)
        subframe.columnconfigure(0, weight=1)

        # Create a text area for storing output.
        text_area = Text(subframe, width=100, height=10, wrap=WORD)
        text_area.grid(row=0, column=0, sticky="nsew")
        text_area.insert('1.0', 'This is where you will see the generated and sorted array.')
        text_area.config(font=('Consolas', 10))

        # Create a Scrollbar widget
        scrollbar = Scrollbar(subframe, orient=VERTICAL, command=text_area.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_area.config(yscrollcommand=scrollbar.set)
        text_area['state'] = 'disabled'

        # Create a separate frame for storing table/treeview content.
        subframe_two = ttk.Frame(root, padding=10)
        subframe_two.grid(row=5, column=0, columnspan=3, sticky=(N,W,E,S))
        subframe_two.rowconfigure(0, weight=1)
        subframe_two.columnconfigure(0, weight=1)

        # Define columns for the table.
        columns = ("Threads", "Elements", "Time (Regular)", "Time (Threaded)")

        # Create Treeview.
        tree = ttk.Treeview(subframe_two, columns=columns, show="headings")

        # Define headings in column config.
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=CENTER, width=100)
        
        # Add sample data to the table.
        '''data = [
            (1, "Alice", 30, "HR")
        ] * 10

        for _ in range(10):
            data.append((2, "Bran", 40, "Corp"))
        
        for row in data:
            tree.insert("", END, values=row)'''

        # Add TreeView widgets to frame
        tree.grid(row=0, column=0, sticky="nsew")

        # Add a vertical scrollbar.
        v_scroll = ttk.Scrollbar(subframe_two, orient=VERTICAL, command=tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=v_scroll.set)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        for child in subframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        thread_entry.focus()
        # root.bind("<Return>", self.calculate)

    def update_label_empty(self, label):
        # Apply the error style.
        label.config(style="Error.TLabel")
        label['text'] = label['text'] + ' [cannot be blank!]'
    
    # ERROR CHECKING FUNCTIONS
    def thread_label_update(self):
        self.thread_label.config(style="Normal.TLabel")
        self.thread_label['text'] = self.thread_label_init_text
        
        # Check empty?
        if not self.number_of_threads.get():
            self.update_label_empty(self.thread_label)
            return 1

        # Check ValueError?
        self.n_cores = 0
        try:
            self.n_cores = int(self.number_of_threads.get())
        except ValueError:
            self.thread_label.config(style="Error.TLabel")
            self.thread_label['text'] = self.thread_label['text'] + ' [please enter a number!]'
            return 1
        
        # Check Range?
        if (self.n_cores < 1 or self.n_cores > self.max_cores):
            self.thread_label.config(style="Error.TLabel")
            self.thread_label['text'] = self.thread_label['text'] + ' [please enter a valid range!]'
            return 1
        
        return 0

    def elem_label_update(self):
        self.element_label.config(style="Normal.TLabel")
        self.element_label['text'] = self.element_label_init_text

        # Check empty?
        if not self.number_of_elements.get():
            self.update_label_empty(self.element_label)
            return 1
        
        # Check ValueError?
        self.n_elements = 0
        try:
            self.n_elements = int(self.number_of_elements.get())
        except ValueError:
            self.element_label.config(style="Error.TLabel")
            self.element_label['text'] = self.element_label['text'] + ' [please enter a number!]'
            return 1
        
        # Check Range?
        if (self.n_elements < 20 or self.n_elements > 10000000):
            self.element_label.config(style="Error.TLabel")
            self.element_label['text'] = self.element_label['text'] + ' [please enter a valid range!]'
            return 1
        
        return 0

    def min_label_update(self):
        self.minimum_label.config(style="Normal.TLabel")
        self.minimum_label['text'] = self.minimum_label_init_text

        # Check empty?
        if not self.minimum_bound.get():
            self.update_label_empty(self.minimum_label)
            return 1
        
        # Check ValueError?
        self.min = 0
        try:
            self.min = int(self.minimum_bound.get())
        except ValueError:
            self.minimum_label.config(style="Error.TLabel")
            self.minimum_label['text'] = self.minimum_label['text'] + ' [please enter a number!]'
            return 1
        
        # Check Range?
        if (self.min < 0):
            self.minimum_label.config(style="Error.TLabel")
            self.minimum_label['text'] = self.minimum_label['text'] + ' [please enter a valid range!]'
            return 1
        
        return 0

    def max_label_update(self):
        self.maximum_label.config(style="Normal.TLabel")
        self.maximum_label['text'] = self.maximum_label_init_text

        # Check empty?
        if not self.maximum_bound.get():
            self.update_label_empty(self.maximum_label)
            return 1
        
        # Check ValueError?
        self.max = 0
        try:
            self.max = int(self.maximum_bound.get())
        except ValueError:
            self.maximum_label.config(style="Error.TLabel")
            self.maximum_label['text'] = self.maximum_label['text'] + ' [please enter a number!]'
            return 1
        
        # Check Range?
        if (self.max > 10000000):
            self.maximum_label.config(style="Error.TLabel")
            self.maximum_label['text'] = self.maximum_label['text'] + ' [it can\'t be that big!]'
            return 1
        
        if (self.max <= self.min):
            self.maximum_label.config(style="Error.TLabel")
            self.maximum_label['text'] = self.maximum_label['text'] + ' [must be bigger than min!]'
            return 1

        return 0

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

    def testUserInput(self):
        # We will defer the actual testing to functions we have cooked up.
        
        # Ask the user for the number of threads/cores.
        '''
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
        '''

        # Ask the user how many elements they would like to generate.
        '''
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
        '''

        # Ask the user to put a bounds on the elements.
        '''
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
        '''
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
        # The first thing we have to do is TEST OUR INPUTS. If our inputs are bad, we SHOULD NOT CONTINUE.
        bad_run = 0
        if self.thread_label_update():
            bad_run = 1
        
        if self.elem_label_update():
            bad_run = 1
        
        if self.min_label_update():
            bad_run = 1
        
        if self.max_label_update():
            bad_run = 1
        
        if bad_run: return bad_run
        

        
        # Testing what vars we have access to...
        print(f"# of cores chosen: {self.n_cores}")
        print(f"# of elements needing to be gen'd: {self.n_elements}")
        print(f"minimum bound: {self.min}")
        print(f"maximum bound: {self.max}")

        # Set the seed.
        random.seed(42)
        # print(random.randint(1, 100))

        # Introduction.
        '''
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
        '''

        '''
        start_time = time.time()
        output1 = self.CountSortRegular(returned_list)
        end_time = time.time()

        print("\n==========REGULAR COUNTSORT==========\n")

        # print("ORIGINAL ARRAY: ", returned_list)
        # print("SORTED ARRAY: ", output)
        print(f"Time taken for regular countsort: {(end_time - start_time)}")

        print("\n==========THREADED COUNTSORT==========\n")
        '''

        # Build thread arguments and call threads.
        '''
        start_time = time.time()
        output2 = self.CountSortThreaded(returned_list, num_threads)
        end_time = time.time()
        print("ORIGINAL ARRAY: ", returned_list)
        print("SORTED ARRAY: ", output)
        print(f"Time taken for threaded countsort: {(end_time - start_time)}")

        if (self.identityCheck(output1, output2) == 0):
            print("The arrays are identical!")
        else:
            print("ERROR! The arrays are not identical! Something's wrong!")

        print("\nRUNNING AGAIN...\n")
        '''

# Set up the window.
root = Tk()
CountSort(root)
root.mainloop()
