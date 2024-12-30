import pygame
from LoginFile import *

# Initialise pygame
pygame.init()

# Define constants
SCREENWIDTH = 1600
SCREENHEIGHT = 1000
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
FPS = 60
font = pygame.font.Font('freesansbold.ttf', 32)
fontSmall = pygame.font.Font('freesansbold.ttf', 18)

# Create screen

SCREEN = pygame.display.set_mode(SCREENSIZE) 
pygame.display.set_caption('Td')

# Define clock
CLOCK = pygame.time.Clock()

class Player():
	def __init__(self):
		# Encapsulate some variables
		self.__score = 0
		self.__lives = 2
		self.state = 'menu'
		self.__wave = 0
		self.__currency = 0
		self.__ID = None

	def setID(self, id):
		self.__ID = id

	def currencyInc(self, num):
		# By getting magnitude, ensure currency increasing
		self.__currency += abs(round(num, 1))

	def currencyDec(self, num):
		# By getting magnitude, ensure currency decreasing
		self.__currency -= abs(round(num, 1))

	def getCurrency(self):
		return self.__currency
	
	def resetWave(self):
		# Reset wave counter
		self.__wave = 0

	def resetScore(self):
		# Reset score
		self.__score = 0

	def lifeLoss(self):
		# Decreases player life
		self.__lives -= 1
		# Check if now have 0 lives
		if self.__lives == 0:
			# Calls game over function
			self.gameOver()

	def setLives(self, num):
		# Check value > 0
		if num > 0:
			# Set lives to parameter
			self.__lives = num

	def incLives(self, num):
		# Check value > 0
		if num > 0:
			# Increase lives by number
			self.__lives += num

	def gameOver(self):
		# Change state to game over
		self.state = 'gameOver'
		# Call leaderboard save
		saveLeaderboard()

	def waveInc(self):
		# Increase wve by 1
		self.__wave += 1

	def getWave(self):
		# Return wave counter 
		return self.__wave

	def scoreInc(self, points):
		# Takes points to increase score by as parameter, increases score
		self.__score += int(points)

	def getScore(self):
		return self.__score
	
	def getLives(self):
		return player.__lives


class Map():
	def __init__(self):
		global targetIMG
		# Calculates width and height in terms of tile dimensions to work out number of columns and rows needed
		x = SCREENWIDTH // 50 
		y = SCREENHEIGHT // 50
		self.columns = x
		self.rows = y
		self.created = False
		self.waypoints = []
		self.toggleRangeVar = False
		self.togglecd = 5

		self.rect = targetIMG.get_rect()
		self.rect.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2)

		self.movingTarget = False

		# Creates blank array
		self.array = []

		self.wavePassed = True

	def get_targetPos(self):
		# Returns target position
		return self.rect.center
	
	def printTarget(self):
		# Prints target image to position
		SCREEN.blit(targetIMG, self.rect.topleft)

	def moveTarget(self):
		# Gets mouse position
		pos = pygame.mouse.get_pos()
		# Sets mouse position as new center point for target
		self.rect.center = pos


	def toggleRange(self):
		# Set cool down if called
		self.togglecd = 4
		
		# Toggle range variable
		if self.toggleRangeVar == False:
			self.toggleRangeVar = True
		else:
			self.toggleRangeVar = False
		
		# Loop through tiles
		for row in range(self.columns):
			for tile in range(self.rows):
				# If tile already free, move on
				if self.array[row][tile][1] != 'free':
					# If not - check if type is base or spawn
					if self.array[row][tile][1].type != 'base' and self.array[row][tile][1].type != 'spawn':
						# If not, set range to toggle variable
						self.array[row][tile][1].showRange = self.toggleRangeVar

	def newMap(self):
		# Clear waypoints and map array
		self.waypoints = []
		self.array = []
		# Creates blank arrays needed for creation of 3D array
		array = []
		array2 = []
		# Creates 3D array to store the map details,
		# Nested for loops create rows and columns: set to 'green' and 'free'
		# Loops to create rows
		for row in range(self.columns): 
			# Loops to create columns
			for tile in range(self.rows): 
				array = ['green', 'free']
				# Appends filled array to blank second array
				array2.append(array) 
			
			# Appends 2D array2 to main array
			self.array.append(array2) 
			# Resets array2
			array2 = []

	def clearTowers(self):
		# Loop through all tiles
		for row in range(self.columns):
			for tile in range(self.rows):
				# If tile already free, move on
				if self.array[row][tile][1] != 'free':
					# If not - check if type is base or spawn
					if self.array[row][tile][1].type != 'base' and self.array[row][tile][1].type != 'spawn':
						# If not, remove instance and replace instance with 'free'
						self.array[row][tile][1] = 'free'

	'''
		Display a tiled map and allow the user to draw 
		the enemy path by clicking tiles.
	'''
	def create(self):
		self.newMap()
		# Array to indicate the tile coords of the previously clicked tile
		prevPoint = None

		firstClick = True

		while not self.created:
			# Print map
			self.printMap()

			# Print any towers so user can see spawn location
			map.printTowers()

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
		
		# Checks if last clicked tile is same as clicked tile
		if prevPoint[0] == currPoint[0] and prevPoint[1] == currPoint[1]:
			# Changes accepted to true
			accepted = True

		if accepted:
			# If valid then creates base
			Base(currPoint)
			self.created = True

	def addSpawn(self, x, y):
		# As this is spawn location, all locations are valid
		coords = [x * 50 + 25, y * 50 + 25]
		self.waypoints.append(coords)
		self.array[x][y][0] = 'brown'
		# Creates spawn instance
		Spawn(coords)


	# Print function for map
	def printMap(self): 
		# Loops through x axis
		for xPos in range(self.columns): 	
			# Loops through y axis	
			for yPos in range(self.rows):
				# Checks tile type
				# Prints tile to the location
				if self.array[xPos][yPos][0] == 'green':
					SCREEN.blit(greenTile.image, (xPos * 50, yPos * 50))
					
				elif self.array[xPos][yPos][0] == 'brown':
					SCREEN.blit(brownTile.image, (xPos * 50, yPos * 50))

	# print function for towers on map
	def printTowers(self):
		# Loops through x axis
		for xPos in range(self.columns): 	
			# Loops through y axis	
			for yPos in range(self.rows):
				# Checks if tower is at location
				if self.array[xPos][yPos][1] != 'free':
					# If tower is at location, prints
					self.array[xPos][yPos][1].print()
					# Calls shoot procedure, this also checks cool down
					self.array[xPos][yPos][1].shoot()


class Enemy():
	# Init function
	def __init__(self, image, type, speed, cd, lives):
		# Declare variables and set image size to 40x40 pixels
		# Include original copy of image so can be used for rotation
		self.imageOriginal = pygame.transform.scale(image, (40,40))
		self.image = pygame.transform.scale(image, (40,40))
		self.rect = self.image.get_rect()
		# Set attributes for enemy
		self.speed = speed
		self.pathEnd = False
		self.type = type
		self.point = 0
		self.rotate = 0
		self.lives = 5
		self.cd = cd 
		self.cdTimer = 5

		# Enemy health increases in later waves
		self.lives = (lives * (1.05 ** player.getWave())) // 1
		self.score = self.lives


		# Uses waypoints from map creation for enemy path
		self.waypoints = map.waypoints 
		self.rect.center = self.waypoints[0]
		# Appends self to object array so it can be called and printed in one function
		enemies.append(self)

		self.rect.center = (self.waypoints[0])

	# Print function for the enemy class
	def print(self):
		# Calls the move function to calculate enemy movement
		self.move() 

		# Prints instance to screen
		SCREEN.blit(self.image, (self.rect.x, self.rect.y)) 
		
	def move(self):
		
		# Checks if point is pointing to item outside of list, or if pointer is null
		if self.point == len(self.waypoints) or self.point == -1:	
			# If enemy reaches end of path, set path end to True and return to exit the function
			self.pathEnd = True
			# Call life loss function to decrease player lives
			player.lifeLoss()
			# Set wave pass to false
			map.wavePassed = False
			# Change pointer to null
			self.point = -1

			return

		if self.cdTimer >= 1:
			self.cdTimer -= 1
			return

		self.cdTimer = self.cd
		
		# Takes waypoint positions of next location
		wpx = self.waypoints[self.point][0]
		wpy = self.waypoints[self.point][1]

		# Calculates distance between current position and waypoint location
		disX = wpx - self.rect.centerx
		disY = wpy - self.rect.centery
		
		# Finds total distance: abs() - gives magnitude of number
		disT = abs(disX) + abs(disY) 
		
		#if < 1, enemy at waypoint, need to move to next waypoint
		if disT <= 1:
			self.rect.center = self.waypoints[self.point]
			# Moves onto next waypoint
			self.point += 1

			# As just increased pointer, need to check if point is at that location
			if self.point == len(self.waypoints):
				# Change pointer to null and return, this exits function
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
		self.rect.centerx += (disX * self.speed / disT)
		self.rect.centery += (disY * self.speed / disT)
		self.cdTimer -= 1




	def getDirection(self, changeY, changeX):
		'''
		To change direction on enemy facing
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
	def __init__(self, image, type, mx, my, range, cd, bulletDMG, towerUpgrades):
		# Transforms tower image to 5 pixels smaller than tile size
		self.image = pygame.transform.scale(image, (greenTile.size - 5, greenTile.size - 5))
		self.rect = self.image.get_rect()
		self.type = type

		# Find x and y coord on grid
		self.x = mx // 50
		self.y = my // 50
		self.rect.center = (self.x * 50 + 25, self.y * 50 + 25)
		# Append object to location in map array 
		map.array[self.x][self.y][1] = self
		# Creates blank bullets array
		self.bullets = []
		self.cd = cd * pow(0.9, towerUpgrades.ROFLevel) // 1
		self.cdTimer = 3
		self.bulletDMG = bulletDMG * (1.2 ** towerUpgrades.damageLevel)
		self.rangeDist = range * (1.2 ** towerUpgrades.rangeLevel)
		self.showRange = True
		

		
	def print(self):
		SCREEN.blit(self.image, (self.x * 50, self.y * 50))
		# Checks to see if range needs to be printed too
		if self.showRange == True:
			# Prints range circle
			pygame.draw.circle(SCREEN, (255, 255, 255), (self.x * 50 + 25, self.y * 50 + 25), self.rangeDist, 2)

		
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
				if self.cdTimer <= 0:
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
		

class Bomb():
	def __init__(self, x, y, target, damage = 1000):
		# Define variables
		self.target = target
		self.radius = 20
		self.x = x
		self.y = y
		self.atTarget = False
		self.image = None
		self.explosionRange = 100
		self.damage = damage
		self.hit = False
		self.VarHit = 30

		# Calculate movement variables
		speed = 10
		disX = self.target[0] - self.x
		disY = self.target[1] - self.y
		disT = abs(disX) + abs(disY)
		self.dx = (disX * speed) / disT
		self.dy = (disY * speed) / disT

	def print(self):
		# If at target location
		if self.atTarget == True:
			# Decreases variable by 1
			self.VarHit -= 1
			if self.VarHit == 0:
				# If at 0, sets hit to true and instance deletes
				self.hit = True
			# Prints explosion image to screen
			SCREEN.blit(self.image, (self.x - self.explosionRange, self.y - self.explosionRange))
			# Exits print loop
			return
		
		# Moves bullet
		self.move()

		# Create and draw circle, this signifies bomb - 0 at end makes it solid
		pygame.draw.circle(SCREEN, 'black', (self.x, self.y), self.radius, 0)


	def move(self):
		# Finds total distance to move, abs() gives magnitude of number
		disT = abs(self.target[0] - self.x) + abs(self.target[1] - self.y)

		if disT <= 10:
			self.explode()
			return

		# Updates the rect positions - then displayed to screen in the print function
		self.x += self.dx
		self.y += self.dy


	def explode(self):
		global explosionIMG
		# Bomb has reached target
		self.atTarget = True
		# Sets image and scales to diameter of explosion range
		self.image = pygame.transform.scale(explosionIMG, (2 * self.explosionRange, 2 * self.explosionRange))
		# Creates rect out of image
		self.rect = self.image.get_rect()
		# Sets rect centre
		self.rect.center = (self.x + self.radius, self.y + self.radius)

		# Loops through all enemies
		for enemy in enemies:
			# Checks if enemy collides with image rect
			if enemy.rect.colliderect(self.rect):
				# Gets centre points of enemy and bomb
				enemyCentre = enemy.rect.center
				bombCentre = self.rect.center
				# Gets total distance (not straight line) between bomb and enemy
				disTotal = abs(enemyCentre[0] - bombCentre[0]) + abs(enemyCentre[1] - bombCentre[1])
				# Gets a multiplier for the damage done to enemies
				damageMult = ((self.explosionRange - disTotal)) / (self.explosionRange)
				# Finds minimum of 2 values, calculated damage done and 10% of bullet damage
				# This way, enemy in range always gets significant amount of damage done
				damageDone = min(self.damage * damageMult, self.damage / 10)

				# Deals damage
				enemy.lives -= damageDone

class Shot():
	def __init__(self, x, y, target, damage):
		# Define key variables
		self.damage = damage
		self.target = (600, 600)
		# Create rect
		self.rect = pygame.Rect(0, 0, 10, 10)
		# Set centre point
		self.rect.center = (x, y)
		self.hit = False
		
		# Find movement constants (change in y and x values)
		disT = abs(x - target[0]) + abs(y - target[1])
		speed = 20

		self.dy = speed * (target[1] - y) / disT
		self.dx = speed * (target[0] - x) / disT

	def print(self):
		global enemies

		# Move and print projectile
		self.move()

		pygame.draw.rect(SCREEN, 'white', self.rect)

		# Loops through enemies
		for i in range(len(enemies)):
			# Checks for collision between bullet and enemy
			if enemies[i].rect.colliderect(self.rect):
				# Gets enemy health
				hp = enemies[i].lives

				# If enemy health more than bullet damage
				if hp > self.damage:
					# Decrease enemy health
					enemies[i].lives -= self.damage
					# Delete bullet
					self.hit = True

				else:
					# Decrease damage by enemy life
					self.damage -= enemies[i].lives
					# Set enemy lives to 0
					enemies[i].lives = 0



	def move(self):
		# Move rect point
		self.rect.centerx += self.dx
		self.rect.centery += self.dy
	
		# Check if bullet is off screen, if is then need to remove by setting hit to True
		if self.rect.centerx < 0 or self.rect.centerx > SCREENWIDTH + 100:
			self.hit = True

		elif self.rect.centery < 0 or self.rect.centery > SCREENHEIGHT + 100:
			self.hit = True


	
class BasicTurret(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for the basic turret
		image = turretIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'turret', mx, my, 150, 200, 4, basicTurretLevels)

class MachineTurret(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for machine gun
		image = machineGunIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'machine', mx, my, 100, 50, 2, machineTurretLevels)

class BombTower(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for bomb tower
		image = bombTowerIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'bomb', mx, my, 120, 300, 200, bombTowerLevels)

	def print(self):
		SCREEN.blit(self.image, (self.x * 50, self.y * 50))
		# Checks to see if range needs to be printed too
		if self.showRange == True:
			# Prints range circle
			pygame.draw.circle(SCREEN, (255, 255, 255), (self.x * 50 + 25, self.y * 50 + 25), self.rangeDist, 2)

		
		instance = 0
		for bullet in self.bullets:
			# Prints bullets
			bullet.print()
			# Checks to see if bullet has hit enemy
			if bullet.hit == True:
				self.bullets.pop(instance)
			instance += 1

	def bulletCreate(self, enemy):
		x = enemy.rect.centerx
		y = enemy.rect.centery
		self.bullets.append(Bomb(self.rect.centerx, self.rect.centery, [x, y], self.bulletDMG))

class MegaShot(Tower):
	# Uses inheritance of tower class
	def __init__(self, mx, my):
		# Loads image for bomb tower
		image = megaTowerIMG

		# Calls tower class initiation with image, type, mouse position, range, cool down and damage
		super().__init__(image, 'mega', mx, my, 20000, 500, 1000, megaShotLevels)


	def bulletCreate(self):
		# Creates and adds bullet to list of bullets
		self.bullets.append(Shot(self.rect.centerx, self.rect.centery, map.get_targetPos(), self.bulletDMG))
		

	def shoot(self):
		# Searches through all enemies
		if self.cdTimer <= 0:
			self.bulletCreate()
			self.cdTimer = self.cd
					
		# Decreases cool down timer if not already 0
		if self.cdTimer != 0:
			self.cdTimer -= 1

	def print(self):
		# Prints tower
		SCREEN.blit(self.image, (self.x * 50, self.y * 50))

		instance = 0
		for bullet in self.bullets:
			# Prints bullets
			bullet.print()
			# Checks to see if bullet has hit enemy
			if bullet.hit == True:
				# Removes bullet
				self.bullets.pop(instance)
			instance += 1

class Soldier(Enemy):
	# Uses inheritance of enemy class
	def __init__(self):
		# Takes image for soldier
		image = soldierIMG
		
		# Calls enemy class initiation with image, type and move cool down
		super().__init__(image, 'soldier', 2, 1, 12)

		# Changes image size to smaller, as default is 40x40 pixels
		self.image = pygame.transform.scale(image, (10, 20))
		self.imageOriginal = pygame.transform.scale(image, (10,20))

		# Define enemy dimensions for use in rotation function
		self.size = 20

		
class Tank(Enemy):
	# Uses inheritance of enemy class
	def __init__(self):
		# Takes image for tank
		image = tankIMG

		# Calls enemy class initiation with image, type, and walk speed
		super().__init__(image, 'tank', 3, 2, 60)

		# Define enemy dimensions for use in rotation function
		self.size = 40

class Boss(Enemy):
	def __init__(self):
		# Takes image for boss
		image = bossIMG
		hp = 150

		# Calls enemy class initiation with image, type, walk speed and health
		super().__init__(image, 'boss', 1, 2, hp)

		# Define enemy dimensions for use in rotation function
		self.size = 45

		self.lives = hp * (1.25 ** (player.getWave() // 2))
		self.score = self.lives


# User base acts as a tower, has similar attributes - hence can use inheritance
class Base(Tower):
	def __init__(self, point):
		# Point parameter, takes point in terms of grid location - not pixels
		x = point[0]
		y = point[1]

		# Gets image for base
		image = baseIMG

		# Calls tower init function, with image, type, position, range, cool down and damage
		super().__init__(image, 'base', x * 50, y * 50, 0, 0, 0, blankLevels)
		
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
		super().__init__(image, 'spawn', x, y, 0, 0, 0, blankLevels)

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


# Create button parent class
class Button():
	# Define init case
	def __init__(self, x, y, height, width, text, colour, textColour = 'white'):
		
		self.colour = colour
		self.textColour = textColour
		self.hoverColour = 'green'
		
		# Render text parameter for button as text
		self.text = font.render(text, True, self.textColour)

		# Scale text to fit into button dimensions
		self.text = pygame.transform.scale(self.text, (height - 2, width - 4))

		# Get rect for text
		self.textrect = self.text.get_rect()
		self.textrect.center = (x, y)


		# Create button rect
		self.rect = pygame.Rect(0, 0, height, width)
		self.rect.center = (x, y)

	# Create print function for class
	def print(self):
		mPos = pygame.mouse.get_pos()

		# Check for mouse hover
		if self.rect.collidepoint(mPos):
			# Check for mouse press when mouse over button
			if pygame.mouse.get_pressed()[0]:
				self.press()
				colour = self.hoverColour
			else:
				# Change button colour if no click
				colour = self.hoverColour
		else:
			# Otherwise default button colour
			colour = self.colour

		# Draw button rect with colour
		pygame.draw.rect(SCREEN, colour, self.rect)
		# Output text
		SCREEN.blit(self.text, self.textrect)


	# Button colour change
	def colourChange(self, new):
		self.colour  = new

	# Use polymorphism to change states
	def press(self):
		pass

# Create button - child
class createMapButton(Button):
	def __init__(self, x, y):
		super().__init__(x, y, 200, 140, 'Create map', 'black')
	
	def press(self):
		player.state = 'mapCreate'

# Create button - child
class playMapButton(Button):
	def __init__(self, x, y):
		super().__init__(x, y, 200, 140, 'Play map', 'black')
	
	def press(self):
		player.state = 'playMap'
	
# Create button - child
class RCTDButton(Button):
	def __init__(self):
		super().__init__(800, 120, 400, 200, 'RC - TD', 'black')

	def press(self):
		player.state = 'menu'
	

# Create button - child
class upgradePageButton(Button):
	def __init__(self, x, y):
		super().__init__(x, y, 200, 140, 'Upgrade towers', 'black')

	def press(self):
		player.state = 'upgradeMenu'

class buyTower(Button):
	def __init__(self, x, y, tower):
		super().__init__(x, y, 30, 35, 'Buy', 'black')
		self.tower = tower

	def press(self):
		return self.tower

	# Create print function for button
	def print(self):
		# Mouse position
		mPos = pygame.mouse.get_pos()
		tower = False
		# Check for mouse hover
		if self.rect.collidepoint(mPos):
			# Check for mouse press when mouse over button
			if pygame.mouse.get_pressed()[0]:
				# Gets tower type when pressed
				tower = self.press()
				colour = self.hoverColour
				# Returns tower type
			else:
				# Change button colour if no click
				colour = self.hoverColour
		else:
			# Otherwise default button colour
			colour = self.colour

		# Gets player lives and cost of tower
		lives = player.getLives()
		for row in hotbar.towersDict:
			if row['name'] == self.tower:
				cost = row['cost']

		# If have enough lives to purchase tower, prints buy button
		if lives > cost:
			# Draw button rect with colour
			pygame.draw.rect(SCREEN, colour, self.rect)
			# Output text
			SCREEN.blit(self.text, self.textrect)

		return tower

class expandHotbar(Button):
	def __init__(self):
		# Call parent class init, text = '>'
		super().__init__(7, SCREENHEIGHT // 2, 20, 32, '>', 'white', 'black')
		# Default show to true
		self.show = True
		self.hoverColour = 'blue'

	def press(self):
		# Change self show to false
		self.show = False
		# Toggle hotbar show
		hotbar.toggle()
		# Change collapse button show
		hotbar.collapse.show = True
		# Set hotbar cool down
		hotbar.cdTimer = 40



class collapseHotbar(Button):
	def __init__(self):
		# Call parent class init, text = '<'
		super().__init__(187, SCREENHEIGHT // 2, 20, 32, '<', 'white', 'black')
		# Default show to false
		self.show = False
		self.hoverColour = 'blue'

	def press(self):
		# Change self show to false
		self.show = False
		# Toggle hotbar show
		hotbar.toggle()
		# Change expand button 
		hotbar.expand.show = True

class towerUpgrade():
	def __init__(self, towerName, x, y, levels = None):
		if levels == None:
			levels = {'damageLevel': 1, 'rangeLevel': 1, 'ROFLevel': 1}
		self.towerName = towerName
		# Set levels for damage, range and rate of fire
		self.damageLevel = levels['damageLevel']
		self.rangeLevel = levels['rangeLevel']
		self.ROFLevel = levels['ROFLevel']
		self.maxLevel = 5
		self.x = x
		self.y = y
		self.cd = 0
		

	def print(self):
		x = self.x
		y = self.y
		xGap = 160
		yGap = 40
		# Renders and prints tower name text
		SCREEN.blit((font.render(self.towerName, True, "blue")), (x + (0.5 * xGap), y))

		# Set text for the attributes and levels
		text = [['Range', self.rangeLevel], ['Damage', self.damageLevel], ['Fire rate', self.ROFLevel]]
		
		# Get mouse position
		mx, my = pygame.mouse.get_pos()
		
		# Loops through the text list
		for row in range(len(text)):
			for column in range(len(text[row])):
				# Checks the column
				if column == 1:
					# Renders and outputs the text level, positions scales with column and row
					SCREEN.blit((font.render(str(text[row][column]) + '/' + str(self.maxLevel), True, "blue")), (x + ((column) * xGap), y + ((row + 1) * yGap)))
				else:
					# Prints text
					SCREEN.blit((font.render(str(text[row][column]), True, "blue")), (x + ((column) * xGap), y + ((row + 1) * yGap)))

			# Prints button image when level less thn max level
			if text[row][1] < self.maxLevel and player.getCurrency() >= 1:
				# Gets position of image
				imagePos = [(x + ((column + 0.58) * xGap)), (y + ((row + 1) * yGap))]
				# Prints image
				SCREEN.blit(plusIMG, (imagePos))

				# Checks for click in the range of button
				if mx >= imagePos[0] and mx <= imagePos[0] + 32 and my >= imagePos[1] and my <= imagePos[1] + 32 and pygame.mouse.get_pressed()[0] and self.cd == 0:
					player.currencyDec(1)
					# Resets cool down - needed so that doesn't insta-click and spam the button
					self.cd = 10

					# Checks row and increases appropriate attribute
					if row == 0:
						self.rangeLevel += 1
					elif row == 1:
						self.damageLevel += 1
					elif row == 2:
						self.ROFLevel += 1
		
		# Decreases cool down if not 0
		if self.cd != 0:
			self.cd -= 1

# Create hotbar for tower placement
class Hotbar():
	def __init__(self):
		# Define height, width and rect
		self.height = 800
		self.width = 180
		self.rect = pygame.Rect(0, 100, self.width, self.height)
		# Define toggle variable - show
		self.__show = False

		# Expand and collapse buttons
		self.collapse = collapseHotbar()
		self.expand = expandHotbar()

		# Cool down variables
		self.cd = 15
		self.cdTimer = 0
		self.placing = 'none'

		size = (150, 150)

		machineGun = pygame.transform.scale(machineGunIMG, size)
		turret = pygame.transform.scale(turretIMG, size)
		bombTower = pygame.transform.scale(bombTowerIMG, size)
		megaShot = pygame.transform.scale(megaTowerIMG, size)

		self.towersDict = [
			{'name' : 'Basic Turret', 'image': turret, 'imageRect' : turret.get_rect(), 'quantity' : 1, 'cost' : 1},
			{'name' : 'Machine Gun',  'image': machineGun, 'imageRect' : machineGun.get_rect(), 'quantity' : 1, 'cost' : 2},
			{'name': 'Bomb Tower',  'image': bombTower, 'imageRect' : bombTower.get_rect(), 'quantity' : 1, 'cost' : 4},
			{'name': 'Mega Shot',  'image': megaShot, 'imageRect' : megaShot.get_rect(), 'quantity' : 1, 'cost' : 10}
		]

		for tower in range(len(self.towersDict)):
			pos = (10, 110 + ((tower) * 180))
			self.towersDict[tower]['imageRect'].topleft = pos
			newButton = buyTower(160, (250 + (tower * 180)), self.towersDict[tower]['name'])
			self.towersDict[tower]['button'] = newButton

	def toggle(self):
		# Checks show variable and changes accordingly
		if self.__show == True:
			self.__show = False
		else:
			self.__show = True

	def reset(self):
		# Reset quantity of each tower to 1
		for tower in self.towersDict:
			tower['quantity'] = 1

		# Reset key variables
		self.cdTimer = self.cd
		self.placing = 'none'
		self.__show = False

	
	def print(self):
		# Check if show true, if not then exit function
		if self.__show == False and self.placing == 'none':
			# Prints expand button - this also checks for a press
			self.expand.print()
			return

		# Check for tower placement
		if self.placing != 'none':
			# If left click
			if pygame.mouse.get_pressed()[0]:
				# If escape key pressed, cancels tower dragging
				if pygame.key.get_pressed()[pygame.K_ESCAPE]:
					self.placing = 'none'
				
				mPos = pygame.mouse.get_pos()
				# Align position to print tower with centre of mouse
				pos = (mPos[0] - 22, mPos[1] - 22)

				# Check tower placement tower type and print image
				if self.placing == 'Machine Gun':
					SCREEN.blit(machineGunIMG, (pos))

				elif self.placing == 'Basic Turret':
					SCREEN.blit(turretIMG, (pos))

				elif self.placing == 'Bomb Tower':
					SCREEN.blit(bombTowerIMG, (pos))

				elif self.placing == 'Mega Shot':
					SCREEN.blit(megaTowerIMG, pos)


			# If not placing tower and not left clicking
			elif not pygame.mouse.get_pressed()[0]:
				# Get mouse position
				mPos = pygame.mouse.get_pos()
				# Get tower
				tower = self.placing
				# Change placing - no longer holding left click
				self.placing = 'none'

				# Checks tile for building tower
				if checkTile(mPos[0], mPos[1]):
					# Decreases quantity of relevant tower
					for row in self.towersDict:
						if row['name'] == tower:
							row['quantity'] -= 1

					# Builds appropriate tower
					if tower == 'Machine Gun':
						MachineTurret(mPos[0], mPos[1])

					elif tower == 'Basic Turret':
						BasicTurret(mPos[0], mPos[1])

					elif tower == 'Bomb Tower':
						BombTower(mPos[0], mPos[1])
					
					elif tower == 'Mega Shot':
						MegaShot(mPos[0], mPos[1])

			# Exits print function, do not want to print hotbar if placing
			return


		# Prints button before hotbar
		self.collapse.print()

		# Otherwise prints
		pygame.draw.rect(SCREEN, 'white', self.rect)

		for index, tower in enumerate(self.towersDict):
			pos = (10, 110 + ((index) * 180))
			# Prints tower image in column,
			SCREEN.blit(tower['image'], tower['imageRect'].topleft)
			# Renders and prints quantity of towers to same location
			SCREEN.blit(fontSmall.render(str(tower['quantity']), True, 'black'), pos)
			# Renders and prints costs of towers to location
			SCREEN.blit(fontSmall.render(('cost: '+str(tower['cost'])), True, 'black'), (pos[0] + 100, pos[1]))

		buyAttempt = False

		# Tower printing and purchase check
		for index in range(len(self.towersDict)):
			# Prints tower out, this also returns the tower type if 'buy' is pressed
			tower = self.towersDict[index]['button'].print()
			
			# If no tower pressed, returns False 
			if tower != False and self.placing == 'none':
				# Buy attempt is now true regardless of cool down
				buyAttempt = True
				# Checks cool down
				if self.cdTimer == 0:
					# Gets lives and cost of tower
					lives = player.getLives()
					cost = self.towersDict[index]['cost']

					# Compares lives and cost
					# Strictly >, if equal to, could end up with 0 lives
					if lives > cost:
						# Increases quantity of tower by 1
						self.towersDict[index]['quantity'] += 1
						# Resets cool down timer
						self.cdTimer = self.cd

						# Decrease player lives by appropriate amount
						for _ in range(cost):
							player.lifeLoss()

					else:
						# Display message to user
						print('Insufficient funds')

		# Decrease cool down
		if self.cdTimer > 0:
			self.cdTimer -= 1

		# Checks for left click and no buy attempt
		if pygame.mouse.get_pressed()[0] and buyAttempt == False:
			# Gets current mouse position
			mPos = pygame.mouse.get_pos()
			# Loops through towers
			for tower in self.towersDict:
				# Checks for collision between image rect of tower and mouse pos
				if tower['imageRect'].collidepoint(mPos):
					# Checks own 1+ of the selected tower
					if tower['quantity'] > 0:
						# Begins placing
						self.placing = tower['name']
					else:
						# Outputs suitable message if no towers owned
						print('No towers available')


# Build tower procedure
def build(): 
	# Get mouse position
	mx, my = pygame.mouse.get_pos()

	# Get user input
	userInput = pygame.key.get_pressed()

	# Check tile is free
	if checkTile(mx, my):
		# Check if 1 key pressed
		if userInput[pygame.K_1]:
			# Creates basic turret
			BasicTurret(mx, my)

		# Checks if 2 key pressed
		elif userInput[pygame.K_2]:
			# Creates machine gun
			MachineTurret(mx, my)

# Check tile is free
def checkTile(mx, my):
	# Get tile coords on grid
	x = mx // 50
	y = my // 50
	# Check tile is green and has no tile built
	if map.array[x][y][0] == 'green' and map.array[x][y][1] == 'free':
		# Returns true if condition met
		return True
	else: 
		return False


# Enemy spawn function
def spawnEnemy():
	# Defines global variables - these are needed to be saved and kept up to date
	global count, wave, spawnDelay, delay

	# Check if list of enemies is empty
	if len(wave) == 0 and len(enemies) == 0:
		if map.wavePassed:
			# Gets value to increase lives by		
			livesInc = getLivesInc(player.getWave())
			# Increases lives
			player.incLives(livesInc)
			# Increments wave counter
			player.waveInc()
		# Creates new wave
		wave = newWave()
		
	
	# Increases count by 1 each frame
	count += 1

	if spawnDelay > delay:
		delay = spawnDelay

	# Delay can change for each enemy, check enemies left to spawn
	if count >= delay and len(wave) != 0:
		# Sets enemy type to  next enemy in list
		type = wave[0]
		
		# Checks if needs to create tank
		if type == 'tank':
			# Creates tank
			Tank()

		# Checks if needs to create soldier
		elif type == 'soldier':
			# Creates soldier
			Soldier()

		# Checks if needs to create boss
		elif type == 'boss':
			# Creates boss
			Boss()

		# When enemy created, delete from list
		wave.pop(0)

		# Reset count, will then increase until = 2 seconds later
		count = 0

		# Different spawn delays for different enemies
		# Dont want enemies to overlap each other when spawned
		if len(wave) != 0:
			if type == wave[0]:
				if type == 'soldier':
					delay = 40
				elif type == 'tank':
					delay = 70
				elif type == 'boss':
					delay = 200


def getLivesInc(wave):
	# Between 1 and 4, gain 2 lives
	if 1 <= wave <= 4:
		return 2
	# Between and 9, gain 3
	elif 6 <= wave <= 9:
		return 3
	# Between 11 and 14, gain 4
	elif 11 <= wave <= 14:
		return 4
	# Check if wave in list (5, 10) or between 15 and 20, gain 5 lives
	elif wave in {5, 10} or 15 <= wave <= 20:
		return 5
	# Between 25 and 44
	elif 25 <= wave <= 44:
		# 25-34 gain 6 (0 // 10 = 0, 0 + 6 = 6)
		# 35-44 gain 7 (5 // 10 = 1, 1 + 6 = 7), etc.
		# For each tenth wave, gain one extra life
		return (wave - 25) // 10 + 6
	# After wave 44, get 8 lives
	elif 45 <= wave <= 60:
		return 8
	# After wave 60, gain no lives
	else:
		return 0

	

def newWave():
	global spawnDelay
	map.wavePassed = True
	# Get current wave
	currentWave = player.getWave()
	# Decrease spawn delay - more enemies in short time span
	if spawnDelay >= 60:
		spawnDelay -= 2

	if currentWave <= 5:
		# Early waves: only soldiers, increasing in number
		wave = ['soldier'] * currentWave

	elif currentWave <= 15:
		# Intermediate waves: mix of soldiers and gradually more tanks
		wave = (['soldier'] * 8) + (['tank'] * (2 * (currentWave - 6)))

	elif currentWave % 10 == 0 and currentWave <= 30:
		# Boss waves (multiples of 10) up to wave 30: only bosses
		wave = ['boss'] * (currentWave // 10)

	elif currentWave <= 20:
		# Waves 16-20: Mix of soldiers and tanks to increase difficulty
		wave = (['soldier'] * 6) + (['tank'] * (currentWave - 10))

	elif currentWave <= 30:
		# Waves 21-30: Increasing count of soldiers and tanks with some bosses
		# Uses conditional expression, if wave number is multiple of 5, boss in wave
		wave = (['soldier'] * 10) + (['tank'] * 4) + ['boss'] * (1 if currentWave % 5 == 0 else 0)

	elif currentWave <= 40:
		# Waves 31-40: Heavier mix with more tanks and bosses
		wave = (['soldier'] * 12) + (['tank'] * 6) + ['boss'] * ((currentWave - 30) // 5)

	elif currentWave <= 50:
		# Waves 41-50: Significant boss presence with many soldiers and tanks
		wave = (['soldier'] * 15) + (['tank'] * 8) + ['boss'] * ((currentWave - 40) // 3)

	else:
		# Waves above 50: Exponentially harder - enemies double every 10 waves
		soldiers = 20 * (2 ** ((currentWave - 50) // 10))  # Double soldiers every 10 waves
		tanks = 10 * (2 ** ((currentWave - 50) // 5))  # Double tanks every 5 waves
		bosses = 1 * (2 ** ((currentWave - 50) // 10))  # Double bosses every 10 waves
		wave = (['soldier'] * soldiers) + (['tank'] * tanks) + (['boss'] * bosses)
	
	return wave



# Display lives and score within game
def displayLiveStats():
	livesText = font.render('Lives: '+str(player.getLives()), True, 'black')
	livesTextrect = livesText.get_rect()
	livesTextrect.topleft = (SCREENWIDTH * 0.9, 18)
	SCREEN.blit(livesText, livesTextrect)

	scoreText = font.render('Score: '+str(player.getScore()), True, 'black')
	scoreTextrect = scoreText.get_rect()
	scoreTextrect.topleft = (SCREENWIDTH * 0.02, 18)
	SCREEN.blit(scoreText, scoreTextrect)

	waveText = font.render('Wave: '+str(player.getWave()), True, 'black')
	waveTextrect = waveText.get_rect()
	waveTextrect.topleft = (SCREENWIDTH * 0.02, 60)
	SCREEN.blit(waveText, waveTextrect)

def displayGameOverStats(tokensEarned):
	# Blank rectangle
	pygame.draw.rect(SCREEN, 'white', pygame.Rect(733, 330, max(190, 115 + (20 * len(str(player.getScore())))), 180))

	# Score text display
	scoreText = font.render('Score: '+str(player.getScore()), True, 'black')
	scoreTextrect = scoreText.get_rect()
	# Set position
	scoreTextrect.topleft = (737, 334)
	SCREEN.blit(scoreText, scoreTextrect)

	# Wave text display
	waveText = font.render('Wave: '+str(player.getWave()), True, 'black')
	waveTextrect = waveText.get_rect()
	# Set position
	waveTextrect.topleft = (737, 405)
	SCREEN.blit(waveText, waveTextrect)

	tokenText = font.render('Tokens: '+str(tokensEarned), True, 'black')
	tokenTextrect = tokenText.get_rect()
	tokenTextrect.topleft = (737, 476)
	SCREEN.blit(tokenText, tokenTextrect)




# Procedure to display tower range when clicked on
def showRange():
	# Get position of click
	position = pygame.mouse.get_pos()
	# Find in terms of grid location
	pos = [position[0] // 50, position[1] // 50]

	# Find tower at that position
	tower = map.array[pos[0]][pos[1]][1]
	# Check tower exists - not free, spawn or base - these have no range
	if tower != 'free' and tower != 'spawn' and tower != 'base':
		# Switch showRange boolean value
		if map.array[pos[0]][pos[1]][1].showRange == True:
			map.array[pos[0]][pos[1]][1].showRange = False
		else:
			map.array[pos[0]][pos[1]][1].showRange = True


# Function to load leaderboard file
def loadLeaderboard():

	# Opens and reads leaderboard file
	LBFile = open("leaderboard.txt","r")
	text = eval(LBFile.read())
	LBScores = []
	LBFile.close()
	# Appends items in file to list
	for x in text:
		LBScores.append(x)
	# Returns list
	return LBScores
 

# Procedure to save leaderboard file
def saveLeaderboard():
	# Set score to any number for testing purposes
	score = player.getScore()

	# Calls function to load leaderboard
	LBScores = loadLeaderboard()

	# Loop through from lowest score in scores to highest
	for x in range(len(LBScores) - 1, -1, -1):
		# Checks if user score is less than score in list
		if LBScores[x] > score or x == 0:

			# Check for first case - user score is higher than all items in file
			if LBScores[0] < score:
				# Saves items in list to temp variable
				temp = LBScores
				# Set first item in list to user score
				LBScores = [score]

				# Appends items in temp variable to list
				for t in temp:
					LBScores.append(t)
				saveLBFile(LBScores)
				return

			# Takes variables for front and back of list - for resaving
			back = LBScores[x + 1:]
			front = LBScores[:x + 1]
			# Resets scores list
			LBScores = []

			# Appends front, score and back of the list in order, this works like an insertion sort
			for Q in front:
				LBScores.append(Q)
			LBScores.append(score)
			for Q in back:
				LBScores.append(Q)
			
			# If any items in the new list are blank, need removing

			# Define index start point
			index = 0

			# Loop through all items in list
			for pos in range(len(LBScores)):

				'''
				Try except loop
				Attempts code in try statement
				If works with no error then moves on
				If causes error then runs except statement
				
				In this case:
				If data at position is a digit, moves on
				If not, then deletes from LBScores
				'''

				try:
					if str(LBScores[index]).isdigit():
						pass

				except:
					# Removes item from list
					LBScores.pop(index)

					# As all items in list would shift places, decrease index to compensate
					index -= 1

				# Increase index to look at next item in list
				index += 1
			
			saveLBFile(LBScores)
			return

# Save data passed in to file	
def saveLBFile(LBScores):
	# Opens file in write mode
	LBFile = open('leaderboard.txt', 'w')
	# Writes top 5 scores in list to file
	LBFile.write(str(LBScores[:6]))

	# Closes file
	LBFile.close()

# Function to display leaderboard
def displayLeaderboard(x, y):
	LBScores = loadLeaderboard()

	text = font.render('All time leaderboard', True, "blue")
	SCREEN.blit(text, (x, y))

	# Takes item in LBScores
	for pos in range(len(LBScores)):
		# Gets text for item in list then renders the text
		current = font.render(str(LBScores[pos]), True, "blue")
		
		# Blits items to screen
		SCREEN.blit(current, (x, y + 10 + (40 * (pos + 0.8))))

# Procedure to display the main menu
def displayMenu():
	for button in mainMenu:
		button.print()
	
	displayLeaderboard(150, 250)

def displayCurrency():
	# Renders text for currency
	text = font.render('Tokens: ' + str(player.getCurrency()), True, "blue")
	# Prints text to screen
	SCREEN.blit(text, (30, 30))



'''
Loops for main states
'''
# All of map creation within 1 singular procedure
def mapCreate():
	# Gives user info about basic functions
	print("""
To place enemy spawn: left click on chosen tile
To create path: left click on tile with same x OR y coord as previous tile
To place your base: right click on either green tile or last clicked tile""")
	map.created = False
	# Map creation game loop
	while map.created == False:
		# Calls map creation function
		map.create()

		# Map creation update screen function
		mapCreateUpdate()
		pygame.display.update()
		for frame in range(132):
			CLOCK.tick(FPS)

		if map.created == True:
			player.state = 'menu'

# All of main game loop in 1 function
def gameLoop():
	# Sets loop to true, forces into main game loop
	loop = True
	newGame()

	while loop:
		# As loop is global variable, if window closed, does not try to update, so no error given
		if loop == False:
			pygame.quit()
			return
		# If player dies, state will change, need new screen
		if player.state != 'playMap':
			loop = False
			return

		# Calls update function to create, move and print objects to screen
		gameUpdate()

		# Updates game window
		pygame.display.update()
		CLOCK.tick(FPS)
	
# Function to clear stats for new game
def newGame():
	# Define global variables
	global wave, enemies, hotbar
	# Reset game stats
	player.setLives(5)
	player.resetScore()
	player.resetWave()
	wave = newWave()
	# Clear enemies
	enemies = []
	# Clear towers - not base/spawn
	map.clearTowers()
	# Reset hotbar
	hotbar.reset()


def upgradeMenuLoop():
	global loop
	loop = True
	while loop:
		upgradeMenuUpdate()

		if loop == False:
			return



'''
Loops for updating screen
'''
# Update function for main game loop
def gameUpdate():
	# Defines global variables
	global enemies, instance, loop

	# Checks for closing window
	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
			# Exits main game loop
			loop = False
			return
		
	# Checks for range toggle
	if pygame.key.get_pressed()[pygame.K_c] and map.togglecd <= 0:
		# Calls range toggle
		map.toggleRange()
	elif pygame.mouse.get_pressed()[0] and hotbar.placing == 'none':
		showRange()


	if map.movingTarget:
		# Moves target
		map.moveTarget()
		# Checks if no longer dragging target
		if not pygame.mouse.get_pressed()[0]:
			map.movingTarget = False

	elif not map.movingTarget:
		# Checks if target selected
		if pygame.mouse.get_pressed()[0] and map.rect.collidepoint(pygame.mouse.get_pos()) and hotbar.placing == 'none':
			map.movingTarget = True
			# Moves target
			map.moveTarget()

	
	# Decrease toggle cool down
	if map.togglecd > 0:
		map.togglecd -= 1
		

	# Prints map
	map.printMap()

 
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
				#return
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
	# Prints towers after printing map and enemies
	map.printTowers()

	# Prints hotbar
	hotbar.print()

	# Outputs player stats - score, lives
	displayLiveStats()

	map.printTarget()

# Update function to be used when creating map
def mapCreateUpdate():
	# Checks for events
	for events in pygame.event.get():
		# Checks for closing window
		if events.type == pygame.QUIT:
			pygame.quit()
			return
	
	# Prints map
	map.printMap()

	# Prints towers
	map.printTowers()


	# Updates display at normal FPS
	pygame.display.update()
	CLOCK.tick(FPS)

def upgradeMenuUpdate():
	global loop
	# Checks for closing window
	if player.state != 'upgradeMenu':
		loop = False
		return
	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
			# Exits main game loop
			loop = False
			return

	# Display text to upgrade screen
	SCREEN.fill('white')
	for tower in turretUpgrades:
		tower.print()
	for button in upgradeMenu:
		button.print()

	displayCurrency()

	

	pygame.display.update()
	CLOCK.tick(FPS)

def gameOverScreen():
	# Empty map towers - leave base and spawn
	map.clearTowers()

	wave = player.getWave()

	if wave // 10 <= 2:
		increase = wave / 10
	elif wave // 10 <= 4:
		increase = (wave / 10) + 4
	else:
		increase = wave // 6
	
	player.currencyInc(round(increase, 1))
	
	# Check player state
	while player.state == 'gameOver':
		# Check for window close
		for events in pygame.event.get():
			if events.type == pygame.QUIT:
				pygame.quit()
				# Exits main game loop
				return
		
		# Fill screen white
		SCREEN.fill('white')
		# Print map
		map.printMap()
		# Print spawn and base
		map.printTowers()
		# Print buttons in game over button list
		for button in gameOver:
			button.print()
		# Display stats
		displayGameOverStats(increase)

		# Update screen
		pygame.display.update()
		CLOCK.tick(FPS)



# Load images
soldierIMG = pygame.image.load('assets/images/soldier.png').convert_alpha()
tankIMG = pygame.image.load('assets/images/tank.png').convert_alpha()
bossIMG = pygame.image.load('assets/images/boss.png').convert_alpha()
greenIMG = pygame.image.load('assets/images/greenSq.png').convert_alpha()
brownIMG = pygame.image.load('assets/images/brownSq.png').convert_alpha()
turretIMG = pygame.image.load('assets/images/turret.png').convert_alpha()
machineGunIMG = pygame.image.load('assets/images/machineGun.png').convert_alpha()
bulletIMG = pygame.image.load('assets/images/bullet.png').convert_alpha()
baseIMG = pygame.image.load('assets/images/base.png').convert_alpha()
spawnIMG = pygame.image.load('assets/images/spawn.png').convert_alpha()
plusIMG = pygame.image.load('assets/images/plusSign.png').convert_alpha()
bombTowerIMG = pygame.image.load('assets/images/bombTower.png').convert_alpha()
megaTowerIMG = pygame.image.load('assets/images/megaShot.png').convert_alpha()
explosionIMG = pygame.image.load('assets/images/explosion.png').convert_alpha()
targetIMG = pygame.image.load('assets/images/crosshair.png').convert_alpha()

# Define a size variable for scaling (e.g., (width, height))
size = (45, 45)

# Scale all images using size variable
soldierIMG = pygame.transform.scale(soldierIMG, size)
tankIMG = pygame.transform.scale(tankIMG, size)
bossIMG = pygame.transform.scale(bossIMG, size)
greenIMG = pygame.transform.scale(greenIMG, size)
brownIMG = pygame.transform.scale(brownIMG, size)
turretIMG = pygame.transform.scale(turretIMG, size)
machineGunIMG = pygame.transform.scale(machineGunIMG, size)
bulletIMG = pygame.transform.scale(bulletIMG, size)
baseIMG = pygame.transform.scale(baseIMG, size)
spawnIMG = pygame.transform.scale(spawnIMG, size)
bombTowerIMG = pygame.transform.scale(bombTowerIMG, size)
megaTowerIMG = pygame.transform.scale(megaTowerIMG, size)
targetIMG = pygame.transform.scale(targetIMG, (30, 30))
plusIMG = pygame.transform.scale(plusIMG, (32, 32))



# Create instances of tile class
greenTile = Tile('green', greenIMG)
brownTile = Tile('brown', brownIMG)

# Creates map
map = Map()

# Creates hotbar
hotbar = Hotbar()

# Create instance of player class
player = Player()

# Enemy spawn delay variables
count = 0
spawnDelay = 120
delay = 1

# Define main buttons
#RCTD =  RCTDButton()

# Define main menu buttons
mainMenu = [createMapButton(800, 320), playMapButton(800, 470), RCTDButton(), upgradePageButton(800, 620)]

# Define game over screen buttons
gameOver = [RCTDButton(), upgradePageButton(695, 600), playMapButton(905, 600)]

# Define upgrade menu buttons
upgradeMenu = [RCTDButton()]

turretLevels = DBValues[0]
player.setID(DBValues[1])
print(turretLevels)

for tower in turretLevels:
	if tower['name'] == 'basicTurret':
		basicTurretLevels = towerUpgrade('Basic Turret', 60, 250, tower)
	elif tower['name'] == 'machineGun':
		machineTurretLevels = towerUpgrade('Machine Gun', 400, 250, tower)


	elif tower['name'] == 'bombTower':
		bombTowerLevels = towerUpgrade('Bomb Tower', 740, 250, tower)

	elif tower['name'] == 'megaShot':
		megaShotLevels = towerUpgrade('Mega Shot', 1080, 250, tower)



# Create blank levels for spawn and base - both classed as turrets
blankLevels = towerUpgrade('', 0, 0)

turretUpgrades = [basicTurretLevels, machineTurretLevels, bombTowerLevels, megaShotLevels]




# Testing game loop

test = False
if test:

	# Testing bomb movement

	test = Shot(30, 30, (900, 900), 50)


	while test:	 
		# Check for quit
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
				break
		# Screen white
		SCREEN.fill('black')
		
		# Move and print shot

		test.print()

		pygame.display.update()
		CLOCK.tick(FPS)




# Game loop
if test == False:
	run = True
else:
	run = False

while run:

	SCREEN.fill('white')
	if map.created:
		map.printMap()
		map.printTowers()
	
	if player.state == 'menu':
		displayMenu()

	elif player.state == 'mapCreate':
		mapCreate()

	elif player.state == 'playMap' and map.created:
		gameLoop()
	
	elif player.state == 'gameOver':
		gameOverScreen()

	elif player.state == 'playMap':
		player.state = 'menu'
		print('Must create map first')

	elif player.state == 'upgradeMenu':
		upgradeMenuLoop()

	
	pygame.display.update()
	 
	# Check for quit
	for event in pygame.event.get():	
		if event.type == pygame.QUIT:
			pygame.quit()
			run = False
			
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			pos = pygame.mouse.get_pos()
			for button in mainMenu:
				if button.rect.collidepoint(pos):
					button.press()
					break