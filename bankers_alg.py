
# Implement the Banker's algorithm for deadlock avoidance, that works on
# a given set of N processes and M resource types (N<10,M<10).
#
# The input files are set up as follows:
#
# resources m, processes n
# total number of resource units
# next n lines, resource needs for each process
# next n lines, resources allocated to each process
#
# Example:
# 5,7
# 8,6,9,5,7
# 1,2,1,2,1
# 2,0,1,0,2
# 0,0,1,0,1
# 1,2,1,2,0
# 2,0,1,0,1
# 1,1,0,1,2
# 2,3,2,2,1
# 2,1,0,1,0
# 0,2,3,1,1
# 1,0,2,0,1
# 1,0,1,0,1
# 0,0,1,0,2
# 1,0,0,1,1
# 2,3,1,2,0

needs = []
allocated = []
max_claim = []
total_resource_units = []
available = []
solutions = []


def get_input():
    file_name = input('Enter name of file\n')
    try:
        with open(file_name) as file:
            line_number = 1
            global resources, processes, total_resource_units, available
            for line in file:
                split_numbers = line.split(',')
                if line_number == 1:
                    resources = int(split_numbers[0])
                    processes = int(split_numbers[1])
                    line_number += 1
                elif line_number == 2:
                    total_resource_units = [int(num) for num in split_numbers]
                    available = [int(num) for num in split_numbers]
                    line_number += 1
                elif 3 <= line_number <= processes + 2:
                    needs.append([int(num) for num in split_numbers])
                    line_number += 1
                elif processes + 2 <= line_number <= (processes * 2) + 2:
                    r = 0
                    to_allocate = [int(num) for num in split_numbers]
                    allocated.append(to_allocate)
                    for t in to_allocate:
                        allocate(available, t, r)
                        r += 1
                    line_number += 1
        set_max()

    except FileNotFoundError:
        print('File Not Found')
        get_input()

    print_data()


def set_max():
    for i in range(processes):
        mc = [needs[i][j] + allocated[i][j] for j in range(resources)]
        max_claim.append(mc)


def allocate(array, resource, r):
    array[r] = array[r] - resource


def print_data():
    print(f'Resources: {resources} Processes: {processes}')
    print(f'Total Resource Units: {total_resource_units}')
    for i in range(processes):
        j = i + 1
        print(f'Process: {j} Max Claim: {max_claim[i]} Allocated: {allocated[i]} Needs: {needs[i]}')
    print(f'Available: {available}')


def print_sequence():
    if len(solutions) > 1:
        print(f'There are a total of {len(solutions)} safe solutions')
    for i in solutions:
        print(f'Safe sequence: {i}')


def all_done(f):
    if False in f:
        return False
    else:
        return True


def return_resource(array, resource, r):
    array[r] = array[r] + resource


class Sequence:

    def __init__(self):
        self.sequence = [None for i in range(processes)]
        self.finished = [False for b in range(processes)]
        self.needs = list.copy(needs)
        self.available = list.copy(available)
        self.allocated = list.copy(allocated)
        self.position = 0

    def check_safe(self):
        is_safe = True
        while not all_done(self.finished):
            possibles = []
            is_safe = False
            for b in range(processes):
                if not self.finished[b]:
                    for r in range(resources):
                        if self.needs[b][r] > self.available[r]:
                            break
                    if r == resources - 1:
                        possibles.append(b)
                        is_safe = True
            if is_safe:
                if len(possibles) > 1:
                    sequence_copy = list.copy(self.sequence)
                    finished_copy = list.copy(self.finished)
                    needs_copy = list.copy(self.needs)
                    available_copy = list.copy(self.available)
                    position_copy = self.position
                    for j in range(len(possibles)):
                        if j == 0:
                            current = possibles[j]
                            self.sequence[self.position] = current + 1
                            self.position += 1
                            self.finished[current] = True
                            for r in range(resources):
                                return_resource(self.available, self.allocated[current][r], r)
                        else:
                            branch = Sequence()
                            branch.available = list.copy(available_copy)
                            branch.finished = list.copy(finished_copy)
                            branch.sequence = list.copy(sequence_copy)
                            branch.position = position_copy
                            branch.needs = list.copy(needs_copy)
                            current = possibles[j]
                            branch.sequence[branch.position] = current + 1
                            branch.position += 1
                            branch.finished[current] = True
                            for r in range(resources):
                                return_resource(branch.available, branch.allocated[current][r], r)
                            branch.check_safe()
                else:
                    current = possibles[0]
                    self.sequence[self.position] = current + 1
                    self.position += 1
                    self.finished[current] = True
                    for r in range(resources):
                        return_resource(self.available, self.allocated[current][r], r)
            else:
                print('There are no safe sequences')
                break
        if is_safe:
            solutions.append(self.sequence)


get_input()
first = Sequence()
first.check_safe()
print_sequence()

