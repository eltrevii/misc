import os
from math import ceil

def clear(): os.system("cls" if os.name == "nt" else "clear")

def bookshelf():
	print('this utility calculates the materials required to craft a specific amount of bookshelves')

	shelves = int(input('how many bookshelves to you want? '))

	wood	= 6 * shelves
	books 	= 3 * shelves

	print(f'''
	for one bookshelf, you need:
	- 6 wood planks
	- 3 books

	for every book, you need:
	- 3 sugar cane
	- 1 leather

	in total, to craft {shelves} bookshelves, you need:
	- {wood} wood planks (can be crafted from {(wood)/4} logs) (round: {ceil((wood)/4)} logs)
	- {books*3} sugar cane and {books} leather = {books} books
	''')

funcs = {
	"bookshelf": bookshelf,
	"test": "test"
}

clear()
print('this script is wip, meaning it has a very reduced amount of utilities')
print(f'what do you want? options are: {", ".join(list(funcs.keys()))}')

sel = input('> ')
clear()
funcs[sel]()