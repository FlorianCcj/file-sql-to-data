##### regex

import re
series = 'Miss Fisher:Phrany Fisher;GOT:Daenerys Targaryen;XFiles:Dana Scully;Miss Fisher:Jack Robinson; Miss Fisher:Dorothy Williams;GOT:Jon Snow;GOT:Tyrion Lannister;X-Files:Fox Mulder'

pattern = r':([A-Za-z ]+)[;|$]'
match = re.findall(r'GOT' + pattern, series)
print(match)

##### entree utilisateur au clavier

error = True
while error:
try:
entier = int(input('Donnez un entier : '))
error = False
except:
print('Une valeur entière est attendue!')
print('Entier : {}'.format(entier))
chaine = input('Donnez une phrase : ')
print('Chaîne : {}'.format(chaine))
error = True
while error:
try:
reels = list(map(float, input('Donnez des réels séparés par une virgule : ').split(',')))
error = False
except:
print('Erreur dans la saisie!')
print('Liste de réels : {}'.format(reels))

##### nombre aleatoire

import random
DEBUG = True
if DEBUG:
	random.seed(1)
	for i in range(5):
		print(random.randint(0, 10))
	for i in range(5):
		print(random.uniform(5, 25)

##### PARCOURIR une liste

ma_liste = ['Jarod', 'Miss Parker', 'Sydney', 'Broots', 'Raines']

for num, name in enumerate(ma_liste):
	print(num, name)