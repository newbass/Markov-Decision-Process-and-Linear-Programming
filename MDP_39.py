import sys
from copy import deepcopy

n,m = input().split(' ')
n = int(n)
m = int(m)

grid = [[0 for i in range(m)] for j in range(n)]
policy = [['O' for i in range(m)] for j in range(n)]

# print(grid)
for i in range(n):
	x = input().split(' ')
	for j in range(len(x)):
		x[j] = float(x[j])
	grid[i] = x

e,w = input().split(' ')
e = int(e)
w = int(w)

end = [(0, 0) for i in range(e)]

for i in range(e):
	x,y = input().split(' ')
	x = int(x)
	y = int(y)
	end[i] = (x, y)

wall = [(0, 0) for i in range(w)]

for i in range(w):
	x,y = input().split(' ')
	x = int(x)
	y = int(y)
	wall[i] = (x, y)

x,y = input().split(' ')
start = (int(x), int(y))

step_cost = float(input())
########### INPUT OVER #################


# print(grid, end, wall, start, step_cost)


############# HELPER FUNCTIONS ##############

def findValidMove(wall, i, j, n, m):
	action = [1, 1, 1, 1]  # NEWS
	if(j==0):
		action[2]=0
	elif(j==m-1):
		action[1]=0

	if(i==0):
		action[0]=0
	elif(i==n-1):
		action[3]=0

	if((i+1,j) in wall):
		action[3]=0

	if((i-1,j) in wall):
		action[0]=0

	if((i,j+1) in wall):
		action[1]=0

	if((i,j-1) in wall):
		action[2]=0

	return action

def update_utility(i, j, updated_grid, action, step_cost):
	maxi = [-(sys.maxsize), -(sys.maxsize), -(sys.maxsize), -(sys.maxsize)]
	#possibility = [1, 1, 1, 1]
	if(action[0]==1):
		temp = 0.8*updated_grid[i-1][j]
	else:
		temp = 0.8*updated_grid[i][j]
	if(action[1]==1):
		temp += 0.1*updated_grid[i][j+1]
	else:
		temp += 0.1*updated_grid[i][j]
	if(action[2]==1):
		temp += 0.1*updated_grid[i][j-1]
	else:
		temp += 0.1*updated_grid[i][j]
	maxi[0] = temp + step_cost

	if(action[1]==1):
		temp = 0.8*updated_grid[i][j+1]
	else:
		temp = 0.8*updated_grid[i][j]
	if(action[0]==1):
		temp += 0.1*updated_grid[i-1][j]
	else:
		temp += 0.1*updated_grid[i][j]
	if(action[3]==1):
		temp += 0.1*updated_grid[i+1][j]
	else:
		temp += 0.1*updated_grid[i][j]
	maxi[1] = temp + step_cost

	if(action[2]==1):
		temp = 0.8*updated_grid[i][j-1]
	else:
		temp = 0.8*updated_grid[i][j]
	if(action[0]==1):
		temp += 0.1*updated_grid[i-1][j]
	else:
		temp += 0.1*updated_grid[i][j]
	if(action[3]==1):
		temp += 0.1*updated_grid[i+1][j]
	else:
		temp += 0.1*updated_grid[i][j]
	maxi[2] = temp + step_cost

	if(action[3]==1):
		temp = 0.8*updated_grid[i+1][j]
	else:
		temp = 0.8*updated_grid[i][j]
	if(action[1]==1):
		temp += 0.1*updated_grid[i][j+1]
	else:
		temp += 0.1*updated_grid[i][j]
	if(action[2]==1):
		temp += 0.1*updated_grid[i][j-1]
	else:
		temp += 0.1*updated_grid[i][j]
	maxi[3] = temp + step_cost
	#print(maxi, i, j)
	if(max(maxi)==maxi[0]): policy[i][j]='N'
	elif(max(maxi)==maxi[1]): policy[i][j]='E'
	elif(max(maxi)==maxi[2]): policy[i][j]='W'
	elif(max(maxi)==maxi[3]): policy[i][j]='S'
	return max(maxi)

def wantToBreak(grid, updated_grid, wall, end):
	#print(grid, updated_grid)
	for i in range(n):
		for j in range(m):
			if((i,j) in wall): continue
			if((i,j) in end): continue
			if(grid[i][j]!=0):
				relative = (abs(grid[i][j]-updated_grid[i][j])*100)/grid[i][j]
				#print(relative, i, j)
			else:
				relative = 2
			if(relative > 1): return False
	return True

s=0
updated_grid = deepcopy(grid)

################### MAIN LOOP #####################################

# for i in range(n):
# 		for j in range(m):
# 			valid_actions = findValidMove(wall, i, j, n, m)
# 			print(valid_actions, i, j)

while True:
	# print(policy[0])
	# print(policy[1])
	# print(policy[2])
	# print(policy[3])
	# print("")
	for i in range(n):
		for j in range(m):
			grid[i][j] = float(format(grid[i][j], '.3f'))
	# print(grid[0])
	# print(grid[1])
	# print(grid[2])
	# print(grid[3])
	# print("")
	# print("")

	for i in range(n):
		for j in range(m):
			if((i,j) in wall): continue
			if((i,j) in end): continue
			valid_actions = findValidMove(wall, i, j, n, m)

			updated_grid[i][j] = update_utility(i, j, updated_grid, valid_actions, step_cost)
			
	check_break = wantToBreak(grid, updated_grid, wall, end)
	grid = deepcopy(updated_grid)

	if(check_break): break
	s+=1

print(policy[0])
print(policy[1])
print(policy[2])
print(policy[3])
print("")
for i in range(n):
		for j in range(m):
			grid[i][j] = float(format(grid[i][j], '.3f'))
print(grid[0])
print(grid[1])
print(grid[2])
print(grid[3])