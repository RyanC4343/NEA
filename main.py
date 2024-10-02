import pygame, time

# Initialise pygame
pygame.init()

# Define variables
SCREENWIDTH = 1600
SCREENHEIGHT = 1000
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
FPS = 60

# Create screen

SCREEN = pygame.display.set_mode(SCREENSIZE) 
pygame.display.set_caption('Td')

# Define clock
CLOCK = pygame.time.Clock()

class Player():
	def __init__(self):
		self.__score = 0
		self.__lives = 8

	def lifeLoss(self):
		# Decreases player life
		self.__lives -= 1
		# Check if now have 0 lives
		if self.__lives == 0:
			# Calls game over function
			self.gameOver()

	def gameOver(self):
		pass

	def scoreInc(self, points):
		# Takes points to increase score by as parameter, increases score
		self.__score += points

	def getScore(self):
		return self.__score
	
	def getLives(self):
		return player.__lives



class Map():
	def __init__(self):
		# Calculates width and height in terms of tile dimensions to work out number of columns and rows needed
		x = SCREENWIDTH // 50 
		y = SCREENHEIGHT // 50
		self.columns = x
		self.rows = y
		self.created = False
		self.waypoints = []

		# Creates blank map array
		self.array = [] 
		
		# Creates blank arrays needed for creation of 3D array
		array = []
		array2 = []
		
		# Creates 3D array to store the map details, nested for loops create rows, columns and tile data - default at 'green' and 'free'
		# Loops to create rows
		for row in range(x): 
			# Loops to create columns
			for tile in range(y): 
				array = ['green', 'free']
				# Appends filled array to blank second array
				array2.append(array) 
			
			# Appends 2D array2 to main array
			self.array.append(array2) 
			# Resets array2
			array2 = [] 
			

	'''
		Display a tiled map and allow the user to draw 
		the enemy path by clicking tiles.
	'''
	def create(self):

		# Array to indicate the tile coords of the previously clicked tile
		prevPoint = None

		firstClick = True

		while not self.created:
			# Print map
			self.print()

			# Print any towers so user can see spawn location
			for tower in towers:
				tower.print()

			pygame.display.update()


			# Iterate over events
			for event in pygame.event.get():
				# Check for mouse click on map
				if event.type == pygame.MOUSEBUTTONDOWN:

					# Get mouse coords
					mx, my = pygame.mouse.get_pos()

					# Get coords of tile that was clicked
					x = mx // 50
					y = my // 50
					
					# If first click - create spawn location
					if firstClick and event.button == 1:
						# Alter tile to spawn location
						self.addSpawn(x, y)
						# Set previous tile to tile that was just clicked
						prevPoint = [x, y]

						# Sets first click to false
						firstClick = False


					# Check for left click: add point
					elif event.button == 1:
						# Alter tile type to enemy path
						valid = self.addpoint(prevPoint, [x, y])
						if valid:
							# Set previous tile to tile that was just clicked
							prevPoint = [x, y]

					# Check for right click: add base
					elif event.button == 3 and not firstClick:
						# Alter tile to base to defend
						self.addBase(prevPoint, [x, y]) 
						

				# Check for closing window
				elif event.type == pygame.QUIT:
					pygame.quit()
					return

		

	def addpoint(self, prevCoords, curtCoords):
		# Finds coordinates in terms of pixels
		coords = [curtCoords[0] * 50 + 25, curtCoords[1] * 50 + 25]

		# Need to validate coords
		if prevCoords[0] == curtCoords[0] or prevCoords[1] == curtCoords[1]:
			valid = True
		else:
			return False
		
		''' 
		Have to make 4 separate functions to check the 4 directions.
		This is because when looping, the indexing ignores the last value,
		however this means the last value does not get changed. 
		Had to make a different loop for each of the possible directions
		'''
		# Checks if x coords are same - only y position changed
		if prevCoords[0] == curtCoords [0]:
			if curtCoords[1] > prevCoords[1]:
				# Checks if any of the positions between previous and current click are brown
				for change in range(prevCoords[1] + 1, curtCoords[1] + 1):
					if self.array[curtCoords[0]][change][0] == 'brown':
						# Returns false if any are brown
						return False
				# If no brown tiles are found, all tiles then changed to brown
				for change in range(prevCoords[1], curtCoords[1] + 1):
					self.array[curtCoords[0]][change][0] = 'brown'
				# Coord added to waypoints list
				self.waypoints.append(coords)
				return True
			
			elif curtCoords[1] < prevCoords[1]:
				# Checks if any of the positions between previous and current click are brown
				for change in range(prevCoords[1] - 1, curtCoords[1] - 1, -1):
					if self.array[curtCoords[0]][change][0] == 'brown':
						# Returns false if any are brown
						return False
				
				for change in range(prevCoords[1], curtCoords[1] - 1, -1):
					self.array[curtCoords[0]][change][0] = 'brown'
				# Coord added to waypoints list
				self.waypoints.append(coords)
				return True				

		# Checks if y coords are same
		elif prevCoords[1] == curtCoords[1]:
			if curtCoords[0] > prevCoords[0]:
				# Checks if any of the positions between previous and current click are brown
				for change in range(prevCoords[0] + 1, curtCoords[0] + 1, 1):
					if self.array[change][curtCoords[1]][0] == 'brown':
						return False


				for change in range(prevCoords[0], curtCoords[0] + 1, 1):
					self.array[change][curtCoords[1]][0] = 'brown'
				# Coord added to waypoints list
				self.waypoints.append(coords)
				return True
			
			elif curtCoords[0] < prevCoords[0]:
				# Checks if any of the positions between previous and current click are brown
				for change in range(prevCoords[0] - 1, curtCoords[0] - 1, -1):
					if self.array[change][curtCoords[1]][0] == 'brown':
						return False
				
				for change in range(prevCoords[0], curtCoords[0] - 1, -1):
					self.array[change][curtCoords[1]][0] = 'brown'
				# Coord added to waypoints list
				self.waypoints.append(coords)
				return True
		else:
			return False



		
	def addBase(self, prevPoint, currPoint):
		# Checks if point is valid
		accepted = self.addpoint(prevPoint, currPoint)
		if accepted:
			# If valid then creates base
			base = Base(currPoint)
			self.created = True

	def addSpawn(self, x, y):
		# As this is spawn location, all locations are valid
		coords = [x * 50 + 25, y * 50 + 25]
		self.waypoints.append(coords)
		self.array[x][y][0] = 'brown'
		# Creates spawn instance
		Spawn(coords)


	# Print function for map
	def print(self): 
		# Finds columns and rows in dimensions array
		x = len(self.array)
		y = len(self.array[0])

		# Loops through x axis
		for xPos in range(x): 	
			# Loops through y axis	
			for yPos in range(y):
				# Checks tile type
				# Prints tile to the location
				if self.array[xPos][yPos][0] == 'green':
					SCREEN.blit(greenTile.image, (xPos * 50, yPos * 50))
					
				elif self.array[xPos][yPos][0] == 'brown':
					SCREEN.blit(brownTile.image, (xPos * 50, yPos * 50))


class Enemy():
	# Init function
	def __init__(self, image, type, speedA, speedB):
		# Declare variables and set image size to 40x40 pixels
		# Include original copy of image so can be used for rotation
		self.imageOriginal = pygame.transform.scale(image, (40,40))
		self.image = pygame.transform.scale(image, (40,40))
		self.rect = self.image.get_rect()
		self.rect = self.image.get_rect()
		# 2 speeds for control of enemy pace
		self.speedA = speedA 
		self.speedB = speedB
		self.pathEnd = False
		self.type = type
		self.point = 0
		self.rotate = 0
		self.lives = 5

		# Uses waypoints from map creation for enemy path
		self.waypoints = map.waypoints 
		self.rect.center = self.waypoints[0]
		# Appends self to object array so it can be called and printed in one function
		enemies.append(self)

	# Print function for the enemy class
	def print(self):
		# Calls the move function to calculate enemy movement
		self.move() 

		# Prints instance to screen
		SCREEN.blit(self.image, (self.rect.x, self.rect.y)) 
		
	def move(self):
		
		if self.point == len(self.waypoints) or self.point == -1:	
			# If enemy reaches end of path, set path end to True and return to exit the function
			self.pathEnd = True
			# Call life loss function to decrease player lives
			player.lifeLoss()
			print(player.getLives())
			# Change pointer to null
			self.point = -1

			return

		# Takes waypoint positions of next location
		wpx = self.waypoints[self.point][0]
		wpy = self.waypoints[self.point][1]

		# Calculates distance between current position and waypoint location
		disX = wpx - self.rect.centerx
		disY = wpy - self.rect.centery
		
		# Finds total distance: abs() - gives magnitude of number
		disT = abs(disX) + abs(disY) 
		
		#if = 0, enemy at waypoint, need to move to next waypoint
		if disT <= 1 and self.point != len(self.waypoints):
			self.rect.center = self.waypoints[self.point]
			# Moves onto next waypoint
			self.point += 1

			# As just increased pointer, need to check if point is at that location
			if self.point == len(self.waypoints):
				# If not, change point to null, and exit function
				self.point = -1				
				return
			
			# Takes waypoint positions of next location
			wpx = self.waypoints[self.point][0]
			wpy = self.waypoints[self.point][1]

			# Calculates distance between current position and waypoint location
			disX = wpx - self.rect.centerx
			disY = wpy - self.rect.centery

			# Change direction of enemy sprite facing
			self.getDirection(disX, disY)

			return



		# Updates the rect positions - then displayed to screen in the print function
		self.rect.centerx += ((disX * self.speedB / disT) / self.speedA ) // 1
		self.rect.centery += ((disY * self.speedB / disT) / self.speedA) // 1

	def getDirection(self, changeY, changeX):
		'''
		To change direction of enemy facing
		Find which of x or y coord is changing
		find which way changing
		Now I want to rotate so it is facing North, South, East or West
		
		'''
		
		if changeY > 0:
			self.rotate = -90

		elif changeY < 0:
			self.rotate = 90

		elif changeX > 0:
			self.rotate = 180
		
		elif changeX < 0:
			self.rotate = 0

		self.image = pygame.transform.rotate(self.imageOriginal, self.rotate)
		self.image = pygame.transform.scale(self.image, (self.size, self.size))

		
class Tile():
	def __init__(self, type, image):
		self.size = 50
		# Transforms image size to 50x50
		self.image = pygame.transform.scale(image, (50, 50))
		self.type = type


class Tower():
	# Initialise tower class
	def __init__(self, image, type, mx, my, range, cd, bulletDMG):
		# Transforms tower image to 5 pixels smaller than tile size
		self.image = pygame.transform.scale(image, (greenTile.size - 5, greenTile.size - 5))
		self.rect = self.image.get_rect()
		self.type = type

		# Find x and y coord on grid
		self.x = mx // 50
		self.y = my // 50
		self.rect.center = (self.x * 50 + 25, self.y * 50 + 25)
		map.array[self.x][self.y][1] = type
		# Appends self to the towers array
		towers.append(self)
		# Creates blank bullets array
		self.bullets = []
		self.cd = cd
		self.cdTimer = 1
		self.bulletDMG = bulletDMG

		self.rangeDist = range
		self.showRange = True

		
	def print(self):
		# Finds dimensions of map to then loop through
		x = len(map.array)
		y = len(map.array[0])

		# Loops through x coords
		for xPos in range(x):
			# Loops through y coords		
			for yPos in range(y):
				# Checks for self, prints tower to screen
				if map.array[xPos][yPos][1] == self.type:
					SCREEN.blit(self.image, (xPos * 50, yPos * 50))
					# Checks to see if range needs to be printed too
					if self.showRange == True:
						# Prints range circle
						pygame.draw.circle(SCREEN, (255, 255, 255), (xPos * 50 + 25, yPos* 50 + 25), self.rangeDist, 2)
					instance = 0
					for bullet in self.bullets:
						# Prints bullets
						bullet.print()

						# Checks to see if bullet has hit enemy
						if bullet.hit == True:
							# Removes bullet damage from enemy if hit
							bullet.enemy.lives -= bullet.damage

							# Removes bullet from bullet array
							self.bullets.pop(instance)
						instance += 1
				
	
	
	def shoot(self):
		# Searches through all enemies
		for enemy in enemies:
			x, y = enemy.rect.center
			x1, y1 = self.rect.center


			# Creates equation of circle, with radius of the range
			if (x - x1) ** 2 + (y - y1) ** 2 <= (self.rangeDist ** 2):
				# Checks cool down timer for tower
				if self.cdTimer == 0:
					# If cool down is 0, creates a bullet targetted at the enemy
					self.bulletCreate(enemy)

					# Resets cool down timer
					self.cdTimer = self.cd
					
		# Decreases cool down timer if not already 0
		if self.cdTimer != 0:
			self.cdTimer -= 1


	def bulletCreate(self, enemy):
		global bulletIMG

		# Creates instance of bullet class
		bullet = Bullet(enemy, self.rect.center, bulletIMG, self.bulletDMG)
		
		# Appends instance to tower's bullet array
		self.bullets.append(bullet)


class Bullet():
	# Bullet init function
	def __init__(self, enemy, pos, image, damage):
		self.image = pygame.transform.scale(image, (10, 10))
		self.rect = self.image.get_rect()

		# Sets bullet spawn point to tower centre position
		self.rect.center = pos 
		self.damage = damage
		self.hit = False

		# Saves enemy, so that its position can be fetched when update function called
		self.enemy = enemy

		
		
	def print(self):
		# Calls classes move function
		self.move() 

		# Prints instance to screen
		SCREEN.blit(self.image, (self.rect.x, self.rect.y))


	def move(self):
		# Gets enemy coords
		wpx, wpy = self.enemy.rect.center

		# Checks for collisions
		if self.rect.colliderect(self.enemy.rect):
			# If collision change self.hit, bullet then deleted
			self.hit = True
			return

		# Calculates distances between current bullet position and the waypoint
		disX = wpx - self.rect.x
		disY = wpy - self.rect.y
		
		# Finds total distance to move, abs() gives magnitude of number
		disT = abs(disX) + abs(disY)
		

		# Updates the rect positions - then displayed to screen in the print function
		self.rect.x += (disX * 10 / disT) // 2 
		self.rect.y += (disY * 10 / disT) // 2
		
	
class BasicTurret(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for the basic turret
		image = turretIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'turret', mx, my, 150, 200, 4)

class MachineTurret(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for machine gun
		image = machineGunIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'machine', mx, my, 100, 20, 2)


class Soldier(Enemy):
	# Uses inheritance of enemy class
	def __init__(self):
		# Takes image for soldier
		image = soldierIMG
		
		# Calls enemy class initiation with image, type, and walk speed
		super().__init__(image, 'soldier', 2, 6)

		# Changes image size to smaller, as default is 40x40 pixels
		self.image = pygame.transform.scale(image, (20, 20))

		# Define enemy dimensions for use in rotation function
		self.size = 20

		# Sets number of lives for solider
		self.lives = 10

		# Sets score worth for enemy
		self.score = 10		
		
class Tank(Enemy):
	# Uses inheritance of enemy class
	def __init__(self):
		# Takes image for tank
		image = tankIMG

		# Calls enemy class initiation with image, type, and walk speed
		super().__init__(image, 'tank', 4, 8)

		# Define enemy dimensions for use in rotation function
		self.size = 40

		# Sets number of lives for tank		
		self.lives = 20

		# Sets score worth for enemy
		self.score = 25


# User base acts as a tower, has similar attributes - hence can use inheritance
class Base(Tower):
	def __init__(self, point):
		# Point parameter, takes point in terms of grid location - not pixels
		x = point[0]
		y = point[1]

		# Gets image for base
		image = baseIMG

		# Calls tower init function, with image, type, position, range, cool down and damage
		super().__init__(image, 'base', x * 50, y * 50, 0, 0, 0)
		
		# Changes image size to fill tile
		self.image = pygame.transform.scale(image, (greenTile.size, greenTile.size))
		
		# As base has no range, change to false, despite range being set to 0, do not need to print
		self.showRange = False

	# Override shoot function, does not shoot so not needed
	def shoot(self):
		return
	
	# Override bullet creation function, does not shoot so not needed
	def bulletCreate(self):
		return
	
# Enemy spawn acts as a tower, has similar attributes - hence can use inheritance
class Spawn(Tower):
	def __init__(self, point):
		# Point parameter, takes point in terms of grid location - not pixels
		x = point[0]
		y = point[1]

		# Gets image for base
		image = spawnIMG

		# Calls tower init function, with image, type, position, range, cool down and damage
		super().__init__(image, 'spawn', x, y, 0, 0, 0)

		# Changes image size to fill tile
		self.image = pygame.transform.scale(image, (greenTile.size, greenTile.size))
		
		# Has no range, do not need to print
		self.showRange = False

	# Override shoot function, does not shoot so not needed
	def shoot(self):
		return

	# Override bullet creation function, does not shoot so not needed
	def bulletCreate(self):
		return

		
	
# Build tower procedure
def build(): 
	# Get mouse position
	mx, my = pygame.mouse.get_pos()

	# Get user input
	userInput = pygame.key.get_pressed()
	
	# Check if 1 key pressed
	if userInput[pygame.K_1]:
		# Creates basic turret
		tower = BasicTurret(mx, my)

	# Checks if 2 key pressed
	elif userInput[pygame.K_2]:
		# Creates machine gun
		tower = MachineTurret(mx, my)

# Count acts as delay for spawning enemies
count = 0

# List of enemies to be created
order = ['soldier', 'tank', 'soldier', 'tank', 'soldier', 'tank', 'soldier', 'tank']
#order = ['tank']


# Enemy spawn function
def spawnEnemy():
	# Defines global variables - these are needed to be saved and kept up to date
	global count, order

	# Check if list of enemies is empty
	if len(order) == 0:
		# Exits function
		return
	
	# Increases count by 1 each frame
	count += 1

	# Every 0.5 seconds, new enemy spawned
	if count == FPS * 0.5:
		# Sets enemy type to  next enemy in list
		type = order[0]
		
		# Checks if needs to create tank
		if type == 'tank':
			# Creates tank
			enemy = Tank()

		# Checks if needs to create soldier
		elif type == 'soldier':
			# Creates soldier
			enemy = Soldier()

		# When enemy created, delete from list
		order.pop(0)

		# Reset count, will then increase until = .5 seconds later
		count = 0


# Update function for main game loop
def Update():
	# Defines global variables
	global enemies, instance, loop

	# Prints map
	map.print()

	# Outputs player score
	#print(player.getScore())

	# Spawns any enemies	
	spawnEnemy()

	# Check if number of enemies on screen is 0
	if len(enemies) != 0:

		instance = 0

		# Checks for each enemy		
		for enemy in enemies:
			# If enemy lives <= 0 then deletes enemy
			if enemy.lives <= 0:
				# Increase score by amount for enemy
				player.scoreInc(enemy.score)

				# Deletes enemy
				enemies.pop(instance)
				return
			else:
				# If enemy not out of lives then prints enemy to screen
				enemy.print()
			
			# Updates instance, this is used to delete enemies
			instance += 1

		# Check again if length of enemies is 0 - last enemy could have been deleted
		if len(enemies) != 0:
			# Defaults instance to 0, so can be used for popping enemies
			instance = 0
			# Checks if enemy reached end of path
			for enemy in enemies:
				if enemy.pathEnd == True:
					# Deletes enemy at instance location
					enemies.pop(instance)
					# Increment instance
					instance += 1

	# Checks for closing window
	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
			# Exits main game loop
			loop = False
			return
		
		# If user clicks, tower build function called
		elif events.type == pygame.MOUSEBUTTONDOWN:
			build()		
	
	# For each tower in list of towers
	for tower in towers:
		# Prints tower
		tower.print()

		# Checks if needs to shoot
		tower.shoot()

	#print(CLOCK.get_fps())
	#os.system('cls')


	

# Load images
soldierIMG = pygame.image.load('assets/images/soldier.png').convert_alpha()
tankIMG = pygame.image.load('assets/images/tank.png').convert_alpha()
greenIMG = pygame.image.load('assets/images/greenSq.png').convert_alpha()
brownIMG = pygame.image.load('assets/images/brownSq.png').convert_alpha()
turretIMG = pygame.image.load('assets/images/turret.png').convert_alpha()
machineGunIMG = pygame.image.load('assets/images/machineGun.png').convert_alpha()
bulletIMG = pygame.image.load('assets/images/bullet.png').convert_alpha()
baseIMG = pygame.image.load('assets/images/base.png').convert_alpha()
spawnIMG = pygame.image.load('assets/images/spawn.png').convert_alpha()


# Create instances of tile class
greenTile = Tile('green', greenIMG)
brownTile = Tile('brown', brownIMG)

# Create blank lists for towers and enemies to be stored in
towers = []
enemies = []

# Creates map
map = Map()

# Create instance of player class
player = Player()

# Update function to be used when creating map
def mapCreateUpdate():
	
	# Prints map
	map.print()

	# Checks for events
	for events in pygame.event.get():
		# Checks for closing window
		if events.type == pygame.QUIT:
			pygame.quit()
			break
	
	for tower in towers:
		tower.print()


	# Updates display at normal FPS
	pygame.display.update()
	CLOCK.tick(FPS)

# Map creation game loop
while map.created == False:
	# Calls map creation function
	map.create()

	# Map creation update screen function
	mapCreateUpdate()


# Sets loop to true, forces into main game loop
loop = True

while loop:
	# Calls update function to create, move and print objects to screen
	Update()

	# As loop is global variable, if window closed, does not try to update, so no error given
	if loop == False:
		break
	# Updates game window
	pygame.display.update()
	CLOCK.tick(FPS)
	
  