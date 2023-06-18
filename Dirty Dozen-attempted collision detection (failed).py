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
	tileKey = {0: [(0, 0), (1, 0), (1, 1), (0, 1)], 1: [(0, 0)], 2: [(0, 0), (1, 0)], 3: [(0, 0), (0, 1)], 4: [(0, 0), (0, 1), (1, 1)], 5: [(0, 0), (0, 1), (1, 0)], 6: [(0, 0), (1, 0), (1, 1)], 7: [(0, 0), (1, 0), (1, -1)]}
	def __init__(self, shape, pos):
		"""Refer to 'Shape key.png' for meaining of self.shape and position of self.pos"""
		self.shape = shape
		self.pos = pos
		self.exact_pos = self.find_exact_pos(self.pos)
		self.tiles = self.get_tiles()
		self.color = black
		self.grabbed = False

	def move_piece(self, mouse_pos, rel_pos_of_exact_pos):
		"""Handles movement and collision of pieces. Sorry it's so confusing, that's collision for ya."""
		x = mouse_pos[0] + rel_pos_of_exact_pos[0]
		y = mouse_pos[1] + rel_pos_of_exact_pos[1]

		piecesShortList = pieces.copy()
		piecesShortList.remove(self)

		for rel_x, rel_y in Piece.tileKey[self.shape]:
			old_tile_exact_pos = [self.exact_pos[0] + rel_x * tileLength, self.exact_pos[1] + rel_y * tileLength]
			tile_exact_pos = [x + rel_x * tileLength, y + rel_y * tileLength]

			if tile_exact_pos[0] < marginLength:
				x = marginLength - rel_x * tileLength
			elif tile_exact_pos[0] + tileLength > marginLength + tileLength * (boardWidth):
				x = marginLength + tileLength * (boardWidth - 1) - rel_x * tileLength

			if tile_exact_pos[1] < marginLength:
				y = marginLength - rel_y * tileLength
			elif tile_exact_pos[1] + tileLength > marginLength + tileLength * (boardHeight):
				y = marginLength + tileLength * (boardHeight - 1) - rel_y * tileLength

			for static_piece in piecesShortList:
				for static_rel_x, static_rel_y in Piece.tileKey[static_piece.shape]:
					static_tile_exact_pos = [static_piece.exact_pos[0] + static_rel_x * tileLength, static_piece.exact_pos[1] + static_rel_y * tileLength]

					if tile_exact_pos[0] < static_tile_exact_pos[0] + tileLength and tile_exact_pos[0] + tileLength > static_tile_exact_pos[0] and tile_exact_pos[1] < static_tile_exact_pos[1] + tileLength and tile_exact_pos[1] + tileLength > static_tile_exact_pos[1]: 

						if old_tile_exact_pos[0] + tileLength <= static_tile_exact_pos[0]:
							print('from the left')
							x = static_tile_exact_pos[0] - tileLength - rel_x * tileLength
						elif old_tile_exact_pos[0] - tileLength >= static_tile_exact_pos[0]:
							print('from the right')
							x = static_tile_exact_pos[0] + tileLength - rel_x * tileLength

						if old_tile_exact_pos[1] + tileLength <= static_tile_exact_pos[1]:
							print('from the top')
							y = static_tile_exact_pos[1] - tileLength - rel_y * tileLength
						elif old_tile_exact_pos[1] - tileLength >= static_tile_exact_pos[1]:
							print('from the bottom')								#flag
							y = static_tile_exact_pos[1] + tileLength - rel_y * tileLength


			self.exact_pos[0] = x
			self.exact_pos[1] = y

	def drop(self):
		self.grabbed = False
		self.pos = self.find_closest_tile(self.exact_pos)
		self.tiles = self.get_tiles()
		self.exact_pos = self.find_exact_pos(self.pos)

	def get_tiles(self):
		tiles = []
		rel_poses = Piece.tileKey[self.shape]
		for rel_pos in rel_poses:
			tile = [self.pos[0] + rel_pos[0], self.pos[1] + rel_pos[1]]
			tiles.append(tile)
		return tiles

	def draw(self):
		if not self.grabbed:
			for tile in self.tiles:
				x = marginLength + tile[0] * tileLength
				y = marginLength + tile[1] * tileLength
				pg.draw.rect(screen, self.color, (x, y, tileLength, tileLength))
		else:
			x, y = self.exact_pos
			for rel_pos in Piece.tileKey[self.shape]:
				new_x = x + rel_pos[0] * tileLength
				new_y = y + rel_pos[1] * tileLength
				pg.draw.rect(screen, self.color, (new_x, new_y, tileLength, tileLength))

	@staticmethod
	def find_exact_pos(pos):
		return [marginLength + pos[0] * tileLength, marginLength + pos[1] * tileLength]

	@staticmethod
	def find_closest_tile(exact_pos):
		tile = [round((exact_pos[0] - marginLength) / tileLength), round((exact_pos[1] - marginLength) / tileLength)]
		return tile


def checkerboard(screen):
	screen.fill(black)
	color = lightGrey
	for i in range(boardWidth):
		for ii in range(boardHeight):
			if color == lightGrey:
				color = darkGrey
			else:
				color = lightGrey
			pg.draw.rect(screen, color, (marginLength + tileLength * i, marginLength + tileLength * ii, tileLength, tileLength))

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
	for piece in pieces:
		if tile in piece.tiles:
			return piece
	return None


def main():
	global pieces
	screen.fill(white)
	checkerboard(screen)
	piece1 = Piece(7, [2,2])
	piece2 = Piece(4, [0,0])
	piece3 = Piece(1, [4,4])
	pieces = [piece1, piece2, piece3]
	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.MOUSEBUTTONDOWN:
				pressed_tile = mouse_tile(event.pos)
				grabbed_piece = get_piece(pressed_tile)
				if grabbed_piece != None:
					grabbed_piece.grabbed = True
					rel_pos_of_exact_pos = [grabbed_piece.exact_pos[0] - event.pos[0], grabbed_piece.exact_pos[1] - event.pos[1]]

			elif event.type == pg.MOUSEBUTTONUP:
				for piece in pieces:
					if piece.grabbed:
						piece.drop()

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False

		mouse_pos = pg.mouse.get_pos()
		for piece in pieces:
			if piece.grabbed:
				piece.move_piece(mouse_pos, rel_pos_of_exact_pos)

		checkerboard(screen)
		for piece in pieces:
			piece.draw()
		pg.display.update()
		clock.tick(60)

	pg.quit()


main()