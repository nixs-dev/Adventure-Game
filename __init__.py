import pygame
from Objects.Player import Player
from Objects.Ground import Ground
from Objects.Monster_Mushroom import Mushroom
from Objects.GameOverFrame import GameOverFrame, TryAgainButton


class World():

	player = None
	ground = None
	screen_size = [1024, 500]
	monsterAmount = 1
	monsters = []
	currentMonster = None
	gameEnd = False
	gameOver = None
	tryAgainButton = None

	screen = pygame.display.set_mode(screen_size)
	background = pygame.image.load('assets/sprites/background.jpg')
	background = pygame.transform.scale(background, screen_size)
	canRun = True
	
	def __init__(self):
		pygame.init()

		self.loadInitialWorldData()
		
		while self.canRun:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:	
					self.canRun = False

				self.player.checkCoolDowns(event) if not self.gameEnd else 0
				self.tryAgainButton.checkClick(event, self) if self.gameOver != None else 0 

			self.drawWorld()

			##FRAME OBJECTS ACTIONS###
			if not self.gameEnd:
				self.drawPlayer()
				self.drawMonsters()
				self.checkCollision()
				self.objetsMovement()
				self.player.updateAnimFrame()
			else:
				self.drawGameOver()

			pygame.display.flip()
			pygame.time.Clock().tick(30)

		pygame.quit()


	def loadInitialWorldData(self):
		self.monsters = []
		self.currentMonster = None
		self.gameEnd = False
		self.gameOver = None
		self.tryAgainButton = None
		self.canRun = True
		self.player = Player(self)
		self.ground = Ground(self.screen_size)
		self.loadMonsters()

	def drawGameOver(self):
		self.gameOver = GameOverFrame(self.screen_size)
		self.tryAgainButton = TryAgainButton(self.screen_size)

		self.screen.blit(self.gameOver.surf, self.gameOver.rect)
		self.screen.blit(self.tryAgainButton.surf, self.tryAgainButton.rect)

	def loadMonsters(self):
		for i in range(0, self.monsterAmount):
			self.monsters.append(Mushroom(self))

		self.currentMonster = self.monsters[0]

	def checkCollision(self):
		self.player.onTheGround = pygame.sprite.collide_rect(self.player, self.ground)
		self.currentMonster.onTheGround = pygame.sprite.collide_rect(self.currentMonster, self.ground)
		self.player.loseLife() if pygame.sprite.collide_rect(self.currentMonster, self.player) else 0

	def objetsMovement(self):
		self.player.fallDueGravity()
		self.currentMonster.fallDueGravity()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] and self.player.onTheGround:
			self.player.move(0, -1)
		elif keys[pygame.K_RIGHT]:
			self.player.move(1, 0)
		elif keys[pygame.K_LEFT]:
			self.player.move(-1, 0)
		else:
			self.player.move(0, 0)

		self.currentMonster.move()			

	def drawWorld(self):
		self.screen.fill((255, 255, 255))
		self.screen.blit(self.background, [0, 0])
		self.screen.blit(self.ground.surf, self.ground.rect)

	
	def drawMonsters(self):
		self.currentMonster = self.monsters[0]
		self.screen.blit(self.currentMonster.surf, self.currentMonster.rect)

	
	def drawPlayer(self):
		if not self.player.flipped:
			self.screen.blit(self.player.surf, self.player.rect)
		else:
			self.screen.blit(pygame.transform.flip(self.player.surf, True, False), self.player.rect)

		for i in self.player.lifes:
			self.screen.blit(i.surf, i.rect)
World()