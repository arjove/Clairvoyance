from collections import Counter
from itertools import permutations
from geometry import inside_polygon
from copy import deepcopy
import math
import datetime
import sys

AREAS = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot']
RESULT_FILE = "result.txt"

def save_solution(solution):
	print("[*] Writing solution to " + RESULT_FILE)
	with open(RESULT_FILE, 'w') as f:
		f.write(datetime.datetime.now().time().isoformat() + "\n")
		f.write('\n'.join(solution))

def read_solution():
	print("[*] Reading previous solution from " + RESULT_FILE)
	try:
		with open(RESULT_FILE, 'r') as f:
			data = f.read()
		time = data.split('\n')[0]
		solution = data.split('\n')[1:]
	except:
		return 0, []
	return time, solution

def input_sequence():
	solution = []
	for area in AREAS:
		solution.append(raw_input(area + ": "))
	return solution

def find_best(solutions):
	time, solution = read_solution()
	#check if we succesfully read the previous solution
	if time == 0 or solution == []:
		print("[-] Failed to read a past solution.")
		sys.stdout.flush()
	else:
		print("[*] Read solution has timestamp " + str(time))
		sys.stdout.flush()

	choice = raw_input("[?] Manually enter (more) recent solution? [Y/N]\n>")
	sys.stdout.flush()
	if choice in ['y', 'yes', 'Y', 'Yes']:
		solution = input_sequence()
		choice = raw_input("[?] Store entered solution? [Y/N]\n>")
		sys.stdout.flush()
		if choice in ['y', 'yes', 'Y', 'Yes']:
			save_solution(solution)

	print("[*] Searching for the solution that is closest to recent solution.")
	sys.stdout.flush()

	#compute sum of squared error for each possible solution
	distances = []
	for i in range(len(solutions)):
		distance = 0
		for j in range(len(AREAS)):
			a = map(int, solution[j].split(' '))
			b = map(int, solutions[i][0][j].split(' '))
			distance += math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
		distances.append(distance)
		print("[*] Score of solution #" + str(i) + ": " + str(distance))

	#select the solution closest to the previous solution
	best = distances.index(min(distances))
	print("[+] Solution with lowest distance is #" + str(best))
	print_solution(solutions[best][0])
	save_solution(solutions[best][0])

def print_solution(solution):
	for i in range(len(AREAS)):
		print(AREAS[i] + ':' + ((10-len(AREAS[i]))*' ') + solution[i])

def check_areas(solution, polygons):
	for i in range(len(AREAS)):
		#append 0 because the hint only gives the first 5 digits
		x = int(solution[i].split(' ')[0] + '0')
		y = int(solution[i].split(' ')[1] + '0')
		if not inside_polygon(x, y, polygons[AREAS[i]]):
			return False
	return True

def build_mapping(mapping, solution):
	#Copy because lists and dicts are by reference (and not by value)
	mapping = deepcopy(mapping)
	j = 0
	for i in range(ord('A'), ord('J')+1):
		if mapping[chr(i)] == '?':
			mapping[chr(i)] = solution[j]
			j += 1
	return mapping

def apply_mapping(puzzle, mapping):
	solution = []

	for line in puzzle:
		s = ""
		for char in line:
			if char == ' ':
				s += char
			else:
				s += mapping[char]
		solution.append(s)

	return solution


def solve(puzzle, polygons):
	mapping = {}
	for i in range(ord('A'), ord('J')+1):
		mapping[chr(i)] = '?'

	#first letter is either 1 or 2 and that 2 appears less often than 1
	first_letters = [row[0] for row in puzzle]

	c = Counter(first_letters)

	if len(c.items()) == 1:
		mapping[c.items()[0][0]] = '1'

	if len(c.items()) == 2:
		if c.items()[0][1] > c.items()[1][1]:
			mapping[c.items()[0][0]] = '1'
			mapping[c.items()[1][0]] = '2'
		else:
			mapping[c.items()[0][0]] = '2'
			mapping[c.items()[1][0]] = '1'
	

	#the first letter of the second part is always 4.
	mapping[puzzle[0][6]] = '4'

	#count how many mappings are still unknown
	remaining = 10 - len([mapping[key] for key in mapping if mapping[key] != '?'])
	print("[*] Checking " + str(math.factorial(remaining)) + " possibile solutions...")
	sys.stdout.flush()

	#generate list of all possible solutions
	unknown = [str(i) for i in range(10) if str(i) not in mapping.values()]
	possibilities = list(permutations(unknown))

	#for each possibility, check if the position it gives for each area actually is in the right area
	solutions = []
	for pos in possibilities:
		m = build_mapping(mapping, pos)
		res = apply_mapping(puzzle, m)
		if check_areas(res, polygons):
			solutions.append((res, m))

	print("[+] Finished checking all possible solutions.")
	sys.stdout.flush()

	#report on found solutions
	if len(solutions) == 0:
		print("[-] Failed to find a solution.")
		sys.stdout.flush()
	elif len(solutions) == 1:
		print("[+] Found one solution!")
		print_solution(solutions[0][0])
		save_solution(solutions[0][0])
		sys.stdout.flush()
	else:
		print("[+] Found " + str(len(solutions)) + " solutions.")
		for i in range(len(solutions)):
			print("Solution #" + str(i))
			print_solution(solutions[i][0])
		choice = raw_input("\n[?] Use past results to determine correct solution? [Y/N]\n>")
		sys.stdout.flush()
		if choice in ['y', 'yes', 'Y', 'Yes']:
			solution = find_best(solutions)

	print("[*] Goodbye!")
	sys.stdout.flush()