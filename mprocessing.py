from multiprocessing import Process

def print_func (continent='Asia'):
    print("The name of the continent is: ", continent)

if __name__ == '__main__':
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func)   # instantiate w/ no args
    procs.append(proc)
    proc.start()

    # instantiating process w/ args
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()

    # complete the process
    for proc in procs:
        proc.join()