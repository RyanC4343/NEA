import pygame, os, time

#initialise pygame
pygame.init()

SCREENWIDTH = 1600
SCREENHEIGHT = 1000
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
FPS = 60

#create screen

SCREEN = pygame.display.set_mode(SCREENSIZE) 
pygame.display.set_caption('Td')


CLOCK = pygame.time.Clock()

class Enemy():
	def __init__(self, image, type, speedA, speedB): #init function
		global waypoints
		self.image = pygame.transform.scale(image, (40,40)) #set enemy image size to 40x40
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = 20, 20
		self.speedA = speedA #2 speeds for control of enemy pace
		self.speedB = speedB
		self.pathEnd = False
		self.type = type
		self.point = 0
		if self.type == 'soldier':
			self.image = pygame.transform.scale(image, (20, 20))

		self.lives = 5

		self.waypoints = waypoints #sets waypoints for the enemy
		enemies.append(self) #appends self to object array so it can be called and printed in one function

	def print(self):
		self.move() #calls classes move function
		SCREEN.blit(self.image, (self.rect.x, self.rect.y)) #print instance to screen
		
	def move(self):
		
		if self.point == len(self.waypoints):			
			#if enemy reaches end of path, set path end to True
			self.pathEnd = True
			return

		wpx = self.waypoints[self.point][0] #takes x coord of next waypoint location
		wpy = self.waypoints[self.point][1] #takes y coord

		
		disX = wpx - self.rect.centerx #calculates distance between current position and waypoint location in terms of x coords
		disY = wpy - self.rect.centery #same for y coords
		
		disT = abs(disX) + abs(disY) #finds total distance: abs() - gives magnitude of number
		
		if disT <= 4: #if = 0, enemy at waypoint, need to move to next waypoint
			self.point += 1 #moves onto next waypoint
			return #exits loop
		

		#updates the rect positions - then displayed to screen in the print function
		self.rect.centerx += ((disX * self.speedB / disT) / self.speedA ) // 1
		self.rect.centery += ((disY * self.speedB / disT) / self.speedA) // 1

		
class Tile():
	def __init__(self, type, image):
		self.size = 50
		self.image = pygame.transform.scale(image, (50, 50)) #transforms image size to 50x50
		self.rect = self.image.get_rect()
		self.type = type #stores passed in type to instance

class Map():
	def __init__(self):
		#calculates width and height in terms of tile dimensions to work out number of columns and rows needed
		x = SCREENWIDTH // 50 
		y = SCREENHEIGHT // 50
		self.columns = x
		self.rows = y
		self.created = False
		self.waypoints = []

		self.dimensions = [] #creates blank array
		#creates blank arrays needed for creation of 3D array
		array = []
		array2 = []
		
		#creates 3D array to store the map details, nested for loops create rows, columns and tile data - default at 'green' and 'free'
		for row in range(x): #loops to create rows
			for tile in range(y): #loops to create columns
				array = ['green', 'free']
				array2.append(array) #appends filled array to blank second array
			self.dimensions.append(array2) #appends 2D array2 to main array
			array2 = [] #resets array2
			
			

	'''
		Display a tiled map and allow the user to draw 
		the enemy path by clicking tiles.
	'''
	def create(self):

		# Boolean to indicate if game loop is running
		creatingMap = True

		# Array to indicate the tile coords of the previously clicked tile
		prevPoint = None


		print("Reached Loop")
		while creatingMap:
			# Print map
			self.print()
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

					# Alter tile type to enemy path
					self.addpoint(x, y)

					# Set previous tile to tile that was just clicked
					prevPoint = [x, y]


				# Check for closing window
				elif event.type == pygame.QUIT:
					pygame.quit()
					return

		

	def addpoint(self, x, y):
		coords = [x * 50 + 25, y * 50 + 25 ]
		self.waypoints.append(coords)
		self.dimensions[x][y][0] = 'brown'
		
	def addbase(self, x, y):
		self.addpoint(x, y)
		self.dimensions[x][y][0] = 'base' #need to find tile to print to this location, need to add enemy delete and user life loss at this location



	def print(self): #print function for map
		#finds columns and rows in dimensions array
		x = len(self.dimensions)
		y = len(self.dimensions[0])

		for xPos in range(x): #loops through x axis		
			for yPos in range(y): #checks rows
				if self.dimensions[xPos][yPos][0] == 'green': #checks if position value is green
					SCREEN.blit(greenTile.image, (xPos * 50, yPos * 50)) #prints green tile to location
					
				elif self.dimensions[xPos][yPos][0] == 'brown': #checks if  position value is brown
					SCREEN.blit(brownTile.image, (xPos * 50, yPos * 50)) #prints brown tile to location
				
				#elif self.dimensions[xPos][yPos][0] == 'base': #checks if  position value is brown
				#	SCREEN.blit(base.image, (xPos * 50, yPos * 50)) #prints brown tile to location

			
class Tower():
	def __init__(self, image, type, mx, my, range, cd, bulletDMG):
		self.image = pygame.transform.scale(image, (greenTile.rect.height-5, greenTile.rect.width-5)) #transforms tower image to 5 pixels smaller than tile size
		self.rect = self.image.get_rect()
		self.type = type
		#takes x and y coord on grid
		self.x = mx // 50
		self.y = my // 50
		self.rect.center = (self.x * 50 + 25, self.y * 50 + 25)
		map.dimensions[self.x][self.y][1] = type
		towers.append(self)
		self.bullets = []
		self.cd = cd
		self.cdTimer = 1
		

		self.rangeDist = range

		
	def print(self):
		x = len(map.dimensions)
		y = len(map.dimensions[0])

		for xPos in range(x):			
			for yPos in range(y):
				if map.dimensions[xPos][yPos][1] == self.type:
					SCREEN.blit(self.image, (xPos * 50, yPos * 50))
					pygame.draw.circle(SCREEN, (255, 255, 255), (xPos * 50 + 25, yPos* 50 + 25), self.rangeDist, 2)
					instance = 0
					for bullet in self.bullets:
						bullet.print()
						if bullet.hit == True:
							bullet.enemy.lives -= bullet.damage
							self.bullets.pop(instance)
						instance += 1
	
	
	def shoot(self):
		for enemy in enemies:
			x, y = enemy.rect.center
			x1, y1 = self.rect.center
			if (x - x1) ** 2 + (y - y1) ** 2 <= (self.rangeDist ** 2):
				if self.cdTimer == 0:
					self.bulletCreate(enemy)
					self.cdTimer = self.cd
			if self.cdTimer != 0:
				self.cdTimer -= 1 
				

				return

	def bulletCreate(self, enemy):
		global bulletIMG
		bullet = Bullet(enemy, self.rect.center, bulletIMG)
		
		self.bullets.append(bullet)


class Bullet():
	def __init__(self, enemy, pos, image, x = 0, y = 0):
		self.image = pygame.transform.scale(image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.center = pos 
		self.damage = 1
		self.hit = False
		self.enemy = enemy

		
		
	def print(self):
		self.move() #calls classes move function
		SCREEN.blit(self.image, (self.rect.x, self.rect.y)) #print instance to screen


	def move(self):
		wpx, wpy = self.enemy.rect.center #takes y coord

		if self.rect.colliderect(self.enemy.rect):
			self.hit = True
			return

		disX = wpx - self.rect.x #calculates distance between current position and waypoint location in terms of x coords
		disY = wpy - self.rect.y #same for y coords
		
		disT = abs(disX) + abs(disY) #finds total distance: abs() - gives magnitude of number
		

		#updates the rect positions - then displayed to screen in the print function
		self.rect.x += (disX * 10 / disT) // 2 
		self.rect.y += (disY * 10 / disT) // 2
		
	
class BasicTurret(Tower):
	def __init__(self, mx, my):
		image = turretIMG
		super().__init__(image, 'turret', mx, my, 150, 100, 10)

class MachineTurret(Tower):
	def __init__(self, mx, my):
		image = machineGunIMG
		super().__init__(image, 'machine', mx, my, 100, 20, 2)

class Soldier(Enemy):
	def __init__(self):
		image = soldierIMG
		super().__init__(image, 'soldier', 2, 6)
		
class Tank(Enemy):
	def __init__(self):
		image = tankIMG
		super().__init__(image, 'tank', 4, 8)



		
	
def build(): 
	mx, my = pygame.mouse.get_pos()
	userInput = pygame.key.get_pressed()
	if userInput[pygame.K_1]:
		tower = BasicTurret(mx, my)
	if userInput[pygame.K_2]:
		tower = MachineTurret(mx, my)

count = 0
order = ['soldier']
order = ['soldier', 'tank', 'soldier', 'tank', 'soldier', 'tank', 'soldier', 'tank']

def spawn():	
	global count, order, FPS, enemies
	if len(order) == 0:
		return
	count += 1
	if count == FPS * 0.5:
		type = order[0]
		if type == 'tank':
			enemy = Tank()
		elif type == 'soldier':
			enemy = Soldier()


		order.pop(0)
		count = 0

 
def Update():
	global enemies, instance, loop
	map.print()
	for tower in towers:
		tower.print()
		tower.shoot()
		
	spawn()
	if len(enemies) != 0:
		instance = 0
		for enemy in enemies:
			if enemy.lives <= 0:
				enemies.pop(instance)
				return
			else:
				enemy.print()
			
			instance += 1
		if len(enemies) != 0:
			if enemies[0].pathEnd == True:
				enemies.pop(0) #enemy reach base location

	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
			loop = False
			
		elif events.type == pygame.MOUSEBUTTONDOWN:
			build()		
	

	#print(CLOCK.get_fps())
	#os.system('cls')


	

#load image
soldierIMG = pygame.image.load('assets/images/soldier.png').convert_alpha()
tankIMG = pygame.image.load('assets/images/tank.png').convert_alpha()
greenIMG = pygame.image.load('assets/images/greenSq.png').convert_alpha()
brownIMG = pygame.image.load('assets/images/brownSq.png').convert_alpha()
turretIMG = pygame.image.load('assets/images/turret.png').convert_alpha()
machineGunIMG = pygame.image.load('assets/images/machineGun.png').convert_alpha()
bulletIMG = pygame.image.load('assets/images/bullet.png').convert_alpha()
baseIMG = pygame.image.load('assets/images/base.png').convert_alpha()

waypoints = [
	[100, 100], [1500, 100] ,[1500, 200], [100, 200], [ 1500, 900]
]

#create instance of class

greenTile = Tile('green', greenIMG)
brownTile = Tile('brown', brownIMG)
baseTile = Tile('base', baseIMG)

map = Map()

towers = []
enemies = []

def tempUpdate():
	
	map.print()
	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
	
	pygame.display.update()
	CLOCK.tick(FPS)

#print(map.dimensions)

while map.created == False:
	map.create()
	tempUpdate()

loop = False

while loop:
	pygame.display.update()
	Update()
	CLOCK.tick(FPS)
	
  