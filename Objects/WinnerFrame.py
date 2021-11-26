import pygame

class WinnerFrame(pygame.sprite.Sprite):

	frame_sprite = pygame.image.load('assets/general_sprites/winnerFrame.png')
	button = None
	sprite_size = [300, 300]
	

	def __init__(self, screen_size):
		super().__init__()

		position = [(screen_size[0] - self.sprite_size[0])/2, (screen_size[1] - self.sprite_size[1])/2]

		self.frame_sprite = pygame.transform.scale(self.frame_sprite, self.sprite_size)

		self.surf = pygame.Surface(self.sprite_size, pygame.SRCALPHA)
		self.surf.blit(self.frame_sprite, (0,0))

		self.rect = self.surf.get_rect(x=position[0], y=position[1])


class PlayAgainButton(pygame.sprite.Sprite):
	button_size = [200, 100]
	button_sprite = pygame.image.load('assets/general_sprites/tryAgainButton.png')
	
	def __init__(self, screen_size):
		super().__init__()

		position = [(screen_size[0] - self.button_size[0])/2, (screen_size[1] - self.button_size[1])/2]
		self.button_sprite = pygame.transform.scale(self.button_sprite, self.button_size)

		self.surf = pygame.Surface(self.button_size, pygame.SRCALPHA)
		self.surf.blit(self.button_sprite, (0, 0))
		self.rect = self.surf.get_rect(x=position[0], y=position[1])

	def checkClick(self, event, world):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.rect.collidepoint(x, y):
					world.load_initial_world_data()