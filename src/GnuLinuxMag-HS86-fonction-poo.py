#### CRÉER UNE FONCTION ayant un nombre de paramètres non fixé

sq_sum(*args):
	result = 0
	for elt in args:
	result += elt ** 2
	return result

print(sq_sum(1, 4, 5, 6, 2, 8))

##### Creer une fonction en inline

f = lambda x : x ** 2
f(2)

##### CRÉER UNE FONCTION qui renvoie une fonction

def genere_fonction(exposant):
	return lambda *e : [x ** exposant for x in e]

carre_liste = genere_fonction(2)
print(carre_liste(1, 2, 3, 4, 5))
cube_liste = genere_fonction(3)
print(cube_liste(1, 2, 3, 4, 5))

##### CRÉER UNE fonction ayant un comportement différent suivant le type de ses paramètres

from functools import singledispatch

@singledispatch
def add(a, b):
	raise NotImplementedError('Les types fournis ne sont pas supportés!')

@add.register(int)
def _(a, b):
	return a + b

@add.register(str)
def _(a, b):
	return sum(list(map(ord, a)) + list(map(ord, b)))

print(add(2, 3))
print(add('GLMF', 'LP'))

##### Ternaire 

ma_variable = True if valeur == 10 else False

##### Creer un decorateur de log

def logger(function):
	def intern(*args, **kwargs):
		print('Arguments transmis :')
		print(' args : {}'.format(args))
		print(' kwargs : {}'.format(kwargs))
		return function(*args, **kwargs)
	return intern

@logger
def test_fct(val1, val2, val3):
	print('Juste un test')

test_fct(1, 'GLMF', val3=12)

#### creer un iterateur

import random

class Dice:
	def __iter__(self):
		return self

	def __next__(self):
		n = random.randint(1, 6)
		if n >= 6:
			raise StopIteration
		return n

if __name__ == '__main__':
	dice = Dice()
	for number in dice:
		print(number)

##### CRÉER UN PAQUETAGE de modules

paquet
├── __init__.py
├── module_X.py
├── sous_paquet_1
│ ├── __init__.py
│ ├── module_a.py
│ └── module_b.py
└── sous_paquet_2
├── __init__.py
├── module_1.py
└── module_2.py

◦ paquet/__init__.py :
from . import sous_paquet_1
from . import sous_paquet_2
◦ paquet/sous_paquet_1/__init__.py :
from . import module_a
from . import module_b
◦ paquet/sous_paquet_2/__init__.py :
from . import module_1
from . import module_2

import paquet
paquet.sous_paquet_1.module_a.display()

##### CRÉER un attribut de classe

class Serie:
	nb = 0 # en dehors d'une methode = partagé

	def __init__(self, name):
		self.name = name
		Serie.nb += 1

	def stock(self):
		print('Nombre total de séries définies :', Serie.nb)


if __name__ == '__main__':
	lost = Serie('Lost')
	got = Serie('Game of Throne')
	lost.stock()
	got.stock()

##### CRÉER UNE MÉTHODE de classe

class Serie:
	nb = 0

	def __init__(self, name):
		self.name = name
		Serie.nb += 1

	@staticmethod
	def stock():
		print('Nombre total de séries définies :', Serie.nb)


if __name__ == '__main__':
	lost = Serie('Lost')
	got = Serie('Game of Throne')
	Serie.stock()