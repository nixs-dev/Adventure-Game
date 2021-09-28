import pygame
from Objects.Player import Player
from Objects.Ground import Ground


class World():

	player = None
	ground = None
	screen_size = [1024, 500]

	screen = pygame.display.set_mode(screen_size)
	background = pygame.image.load('assets/sprites/background.jpg')
	background = pygame.transform.scale(background, screen_size)
	canRun = True
	
	def __init__(self):
		pygame.init()

		self.player = Player()
		self.ground = Ground(self.screen_size)

		while self.canRun:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.canRun = False

			self.checkCollision('PlayerWithGround')
			self.checkCommand()
			self.checkLimits()
			self.player.updateAnimFrame()
			self.drawWorld()
			pygame.display.flip()
			pygame.time.Clock().tick(30)

		pygame.quit()

	def checkCollision(self, interac):
		if interac == 'PlayerWithGround':
			self.player.onTheGround = pygame.sprite.collide_rect(self.player, self.ground)

	def checkCommand(self):
		if not self.player.onTheGround:
			self.player.fallDueGravity()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] and self.player.onTheGround:
			self.player.move(0, -1)
		elif keys[pygame.K_RIGHT]:
			self.player.move(1, 0)
		elif keys[pygame.K_LEFT]:
			self.player.move(-1, 0)
		else:
			self.player.move(0, 0)

	def checkLimits(self):
		if self.player.rect.x <= 0:
			self.player.canBack = False
		else:
			self.player.canBack = True

		if self.player.rect.x >= self.screen_size[0] - self.player.sprite_size[0]:
			self.player.canGo = False
		else:
			self.player.canGo = True			

	def drawWorld(self):

		self.screen.fill((255, 255, 255))
		self.screen.blit(self.background, [0, 0])
		self.screen.blit(self.ground.surf, self.ground.rect)

		if not self.player.flipped:
			self.screen.blit(self.player.surf, self.player.rect)
		else:
			self.screen.blit(pygame.transform.flip(self.player.surf, True, False), self.player.rect)

World()