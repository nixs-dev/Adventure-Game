import pygame

class Mushroom(pygame.sprite.Sprite):
	scene = None
	speed = 7
	gravity = 7
	isJumping = False
	onTheGround = False
	canGo = True
	canBack = True
	GoToRight = False
	spawn_pos = [500, 40]
	sprite_size = [30, 30]
	idle_sprite = pygame.image.load('assets/chars_sprites/monsters/mushroom/idle.png')

	def __init__(self, scene):
		super(Mushroom, self).__init__()
		self.scene = scene

		self.idle_sprite = pygame.transform.scale(self.idle_sprite, self.sprite_size)
		self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
		self.surf.blit(self.idle_sprite, (0,0))
		self.rect = self.surf.get_rect(x=self.spawn_pos[0], y=self.spawn_pos[1])

	def move(self):
		if not self.onTheGround:
			return

		if self.GoToRight:
			if self.canGo:
				self.rect.x += self.speed
			else:
				self.GoToRight = False
		else:
			if self.canBack:
				self.rect.x -= self.speed
			else:
				self.GoToRight = True
		
		self.checkLimits()

	def checkLimits(self):
		if self.rect.x <= 0:
			self.canBack = False
		else:
			self.canBack = True

		if self.rect.x >= self.scene.screen_size[0] - self.sprite_size[0]:
			self.canGo = False
		else:
			self.canGo = True

	def fallDueGravity(self):
		if not self.isJumping and not self.onTheGround:
			self.rect.y += self.gravity
