import pygame as pg
pg.init()
pg.display.set_caption('The Dirty Dozen')

# Constants:
tileLength = 100
marginLength = 10
boardWidth = 6
boardHeight = 5

# Colors:
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
lightGrey = (211,211,211)
darkGrey = (105,105,105)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Calculated Constants
displayW = tileLength * boardWidth + marginLength * 2
displayH = tileLength * boardHeight + marginLength * 2
clock = pg.time.Clock()
screen = pg.display.set_mode((displayW, displayH))

class Piece:
	pieces = []
	tileKey = {0: [(0, 0), (1, 0), (1, 1), (0, 1)], 1: [(0, 0)], 2: [(0, 0), (1, 0)], 3: [(0, 0), (0, 1)], 4: [(0, 0), (0, 1), (1, 1)], 5: [(0, 0), (0, 1), (1, 0)], 6: [(0, 0), (1, 0), (1, 1)], 7: [(0, 1), (1, 0), (1, 1)]}
	def __init__(self, shape, pos):
		"""Refer to 'Shape key.png' for meaining of self.shape and position of self.pos"""
		self.shape = shape
		self.image = self.get_image()
		self.pos = pos
		self.exact_pos = self.find_exact_pos(self.pos)
		self.tiles = self.get_tiles()
		self.color = black
		self.grabbed = False

	def grab(self, mouse_pos):
		self.grabbed = True
		self.initial_mouse_pos = mouse_pos
		self.mouse_offset = [self.exact_pos[0] - mouse_pos[0], self.exact_pos[1] - mouse_pos[1]]
		self.determine_axis()

	def determine_axis(self):
		xaxis = ((-1, 0), (1, 0))
		yaxis = ((0, -1), (0, 1))
		leftFree = True
		rightFree = True
		upFree = True
		downFree = True
		for tile_pos in self.tiles:
			if get_piece(adjust(tile_pos, xaxis[0])) not in [None, self]:
				leftFree = False
			if get_piece(adjust(tile_pos, xaxis[1])) not in [None, self]:
				rightFree = False
			if get_piece(adjust(tile_pos, yaxis[0])) not in [None, self]:
				upFree = False
			if get_piece(adjust(tile_pos, yaxis[1])) not in [None, self]:
				downFree = False
		self.xfree = leftFree or rightFree
		self.yfree = upFree or downFree
		if not (self.xfree and self.yfree):
			self.determine_boundaries()

	def determine_boundaries(self):
		if self.xfree or self.yfree:
			if self.xfree:
				boardLength = boardWidth
				pos_index = 0
			else:
				boardLength = boardHeight
				pos_index = 1
			default_first_boundary = marginLength
			default_second_boundary = marginLength + (boardLength - 1) * tileLength
			self.first_boundary = default_first_boundary
			self.second_boundary = default_second_boundary
			counter = self.pos[pos_index]
			while counter >= 0:
				exact_coord = marginLength + tileLength * counter
				for rel_x, rel_y in Piece.tileKey[self.shape]:
					tile_pos = adjust(self.pos, (rel_x, rel_y))
					if self.xfree:
						search_tile = [counter + rel_x - 1, tile_pos[1]]
					else:
						search_tile = [tile_pos[0], counter + rel_y - 1]
					if get_piece(search_tile) not in [None, self] and self.first_boundary < exact_coord:
						self.first_boundary = exact_coord
				if self.first_boundary == default_first_boundary:
					counter -= 1
				else:
					break

			counter = self.pos[pos_index]
			while counter < boardLength:
				exact_coord = marginLength + tileLength * counter
				for rel_x, rel_y in Piece.tileKey[self.shape]:
					tile_pos = adjust(self.pos, (rel_x, rel_y))
					if self.xfree:
						search_tile = [counter + rel_x + 1, tile_pos[1]]
					else:
						search_tile = [tile_pos[0], counter + rel_y + 1]
					if get_piece(search_tile) not in [None, self] and self.second_boundary > exact_coord:
							self.second_boundary = exact_coord
				if self.second_boundary == default_second_boundary:
					counter += 1
				else:
					break

	def move(self, mouse_pos):
		if self.xfree or self.yfree:
			if self.xfree and self.yfree:
				mouse_delta = adjust(mouse_pos, self.initial_mouse_pos, negate=True)
				if abs(mouse_delta[0]) > abs(mouse_delta[1]):
					self.yfree = False
					self.determine_boundaries()
				elif abs(mouse_delta[0]) < abs(mouse_delta[1]):
					self.xfree = False
					self.determine_boundaries()
			else:
				if self.xfree:
					x = mouse_pos[0] + self.mouse_offset[0]
					if x < self.first_boundary:
						x = self.first_boundary
					elif x > self.second_boundary:
						x = self.second_boundary
					self.exact_pos[0] = x
				else:
					y = mouse_pos[1] + self.mouse_offset[1]	
					if y < self.first_boundary:
						y = self.first_boundary
					elif y > self.second_boundary:
						y = self.second_boundary
					self.exact_pos[1] = y
				
	def drop(self):
		self.grabbed = False
		self.pos = self.find_closest_tile(self.exact_pos)
		self.exact_pos = self.find_exact_pos(self.pos)
		self.tiles = self.get_tiles()
		#Testing win condition:
		# if get_piece

	def get_tiles(self):
		tiles = []
		rel_poses = Piece.tileKey[self.shape]
		for rel_pos in rel_poses:
			tile = [self.pos[0] + rel_pos[0], self.pos[1] + rel_pos[1]]
			tiles.append(tile)
		return tiles

	def get_image(self):
		file_path = f'{self.shape}.png'
		return pg.image.load(file_path)

	def draw(self):
		if not self.grabbed:
			for tile in self.tiles:
				x = marginLength + tile[0] * tileLength
				y = marginLength + tile[1] * tileLength
				screen.blit(self.image, self.exact_pos)
		else:
			x, y = self.exact_pos
			for rel_pos in Piece.tileKey[self.shape]:
				new_x = x + rel_pos[0] * tileLength
				new_y = y + rel_pos[1] * tileLength
				screen.blit(self.image, self.exact_pos)

	@staticmethod
	def find_exact_pos(pos):
		return [marginLength + pos[0] * tileLength, marginLength + pos[1] * tileLength]

	@staticmethod
	def find_closest_tile(exact_pos):
		tile = [round((exact_pos[0] - marginLength) / tileLength), round((exact_pos[1] - marginLength) / tileLength)]
		return tile


def checkerboard(screen):
	screen.fill(grey)
	color = lightGrey
	for i in range(boardWidth):
		for ii in range(boardHeight):
			if color == lightGrey:
				color = darkGrey
			else:
				color = lightGrey
			pg.draw.rect(screen, color, (marginLength + tileLength * i, marginLength + tileLength * ii, tileLength, tileLength))

def adjust(l1, l2, negate=False):
	if negate :
		return [x - y for x, y in zip(l1, l2)]
	else:
		return [x + y for x, y in zip(l1, l2)]

def mouse_tile(pos):
	if pos[0] < marginLength or pos[0] > marginLength + tileLength * boardWidth or pos[1] < marginLength or pos[1] > marginLength + tileLength * boardHeight:
		print('Out of Bounds')                                                                                #flag
	else:
		tile = [int((pos[0] - marginLength) / tileLength), int((pos[1] - marginLength) / tileLength)]
		return tile

def color_tile(tile, color):
	"""probably a temporary function"""
	x = marginLength + tile[0] * tileLength
	y = marginLength + tile[1] * tileLength
	pg.draw.rect(screen, color, (x, y, tileLength, tileLength))


def get_piece(tile):
	try:
		x, y = tile
	except TypeError:
		return None
	if x < 0 or y < 0 or x > 5 or y > 4:
		return 1
	for piece in Piece.pieces:
		if tile in piece.tiles:
			return piece
	return None


def main():
	screen.fill(white)
	checkerboard(screen)
	piece_type = 0
	pieces = []
	per_shape_list = []
	print(f'Now on Piece #{piece_type}')
	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				pressed_tile = mouse_tile(event.pos)
				Piece.pieces.append(Piece(piece_type, pressed_tile)) 
				per_shape_list.append(pressed_tile)

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				elif event.key == pg.K_RETURN:
					if len(per_shape_list) > 0:
						pieces.append([piece_type, per_shape_list])
						per_shape_list = []
					piece_type += 1
					print(f'Now on Piece #{piece_type}')
					if piece_type > 7:
						print(pieces)
						locked = False

		mouse_pos = pg.mouse.get_pos()

		checkerboard(screen)
		for piece in Piece.pieces:
			piece.draw()
		pg.display.update()
		clock.tick(60)

	pg.quit()


main()