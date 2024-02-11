import os, sys
from math import ceil, floor

def clear(): os.system("cls" if os.name == "nt" else "clear")

class cc:
	def doc(arg=None):
		'''displays help'''
		if arg == None:
			print("help: displays help for a specific command, e.g. help bookshelf")
		else:
			if arg in funcs:
				print(f"help for {arg}:\n  {funcs[arg].__doc__}")
			else:
				print(f"help: command '{arg}' not found")			

	def bookshelf(shelves):
		'''calculates the materials required to craft a specific amount of bookshelves
  e.g. 1 bookshelf = 6 planks and 3 books (3 paper and 1 leather)'''

		#shelves = int(input('how many bookshelves to you want? '))

		wood	= 6 * shelves
		books 	= 3 * shelves

		print(f"{wood} wood planks (from {(wood)/4} logs) (round: {ceil((wood)/4)} logs), {books*3} sugar cane, {books} books from {books} leather")

	def stacks(items):
		'''calculates how many stacks (and extra items) a specific amount of items has
  e.g. 132 blocks = 2 stacks and 4 blocks'''
		items = int(items)
		print(f"stacks: {int(items/64 - (items/64 - floor(items/64)))} stacks + {int((items/64 - floor(items/64))*64)} blocks")

# ------------------------------------------------------------------------------------------------------

funcs = {
	"help": cc.doc,
	"bookshelf": cc.bookshelf,
	"stacks": cc.stacks
}

clear()
print('this script is wip, meaning it has a very reduced amount of utilities')
print(f'what do you want? options are: {", ".join(list(funcs.keys()))}')

while True:
	command = input("> ")
	#commands = ' '.join(sys.argv[1:])
	command_name, *args = command.split()
	if command_name in funcs:
		function = funcs[command_name]
		function(*args)
		print("")