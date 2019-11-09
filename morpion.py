import numpy as np


#______interactions_players________

def set_case(grid,p,j): 
	grid[p] = j
	return grid

def possib(grid): #return all alignements
	L1 = grid[0,:]
	L2 = grid[1,:]
	L3 = grid[2,:]
	C1 = grid[:,0]
	C2 = grid[:,1]
	C3 = grid[:,2]
	D1 = grid.diagonal()
	D2 = np.array([grid[0,2],grid[1,1],grid[2,0]])
	return [L1,L2,L3,C1,C2,C3,D1,D2]

def win(grid,who): 
	combis = possib(grid)
	for x in combis:
		if (x == who).sum() == 3:
			return True
	return False

def f(grid,p,j): #eval function
	grid_with_p = grid.copy()
	grid_with_p[p] = j
	combis = possib(grid)
	nbalign2H = 0
	nbalign1H = 0
	nbalign2C = 0
	nbalign1C = 0
	for x in combis:
		C_H = (x == 'H').sum()
		C_empty = (x == '').sum()
		C_C = 3-C_H-C_empty
		if C_empty + C_H == 3:
			if C_H >= 2:
				nbalign2H += 1
			else :
				nbalign1H += 1
		if C_empty + C_C == 3:
			if C_C >= 2 : 
				nbalign2C +=1
			else :
				nbalign1C +=1
	if j == 'C':
		return 	(3*nbalign2C+nbalign1C)-(3*nbalign2H+nbalign1H)
	return (3*nbalign2H+nbalign1H) - (3*nbalign2C+nbalign1C)

def cases(grid,who): #renvoie une liste des coordonnées des cases de who
    cases=[]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j]==who:
                cases.append((i,j))
    return cases

def inverse(j):
	if j == 'H':
		return 'C'
	return 'H'
#_________min_max__________
def minimax(grid,n,p,j,next_states,eval):
	if n == 0:
		return eval(grid,p,j)
	new_grid = grid.copy()
	new_grid[p] = j
	empty = next_states(grid,'')
	score_min = +999 #+ infinity
	score_max = -999 #- infinity
	for x in empty:
		score_x = minimax(new_grid,n-1,x,inverse(j),cases,f)
		if (inverse(j) == 'H') and (score_min > score_x):
			score_min = score_x
			best_x = x
		if (inverse(j) == 'C') and (score_max < score_x):
			score_max = score_x
			best_x = x
	if j == 'C':
		return score_min
	return score_max

def find_best_place(grid,depth): #find best place using minmax 
	empty = cases(grid,'')
	scores = []
	for x in empty:
		scores.append(minimax(grid,depth,x,'C',cases,f))
	if depth%2:
		ind = scores.index(min(scores))
	else:
		ind = scores.index(max(scores))
	return empty[ind]

def new_game(): #generate new grid
	return np.zeros((3,3),dtype = str)

def render(grid): #display frid on console
	for i in range(3):
		ligne = ''
		for j in range(3):
			if grid[i][j] != '':
				ligne+='-'+str(grid[i][j])
			else:
				ligne+='-0'
		print(ligne)
	return None		
def input_to_tuple(input):
	return (int(input[1]),int(input[-2]))

def main():
	G = new_game()
	render(G)
	joueur = 'H'
	while not win(G,inverse(joueur)) and len(cases(G,'')) > 0:
		if joueur == 'H':
			next_pos = input("Entrez la position de la nouvelle case (i,j)") 
			next_pos = input_to_tuple(next_pos)
		else:
			next_pos = find_best_place(G,3)
			print("L'ordinateur joue :")
		G = set_case(G,next_pos,joueur)
		render(G)
		joueur = inverse(joueur)
	if win(G,'H'):
		print("Félicitation vous avez battu l'IA")
	elif win(G,'C'):
		print("Dommage, vous avez perdu, essayez encore !")
	else :
		print("La grille du morpion est pleine, c'est une égalité entre vous, retentez votre chance !")
	return None



if __name__ == '__main__':
	main()


