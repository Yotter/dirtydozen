"""
The Dirty Dozen 1.0

To Do:
	Allow pieces to push each other
	Add comments
	Make the last piece slide-out-able
	Make end screen
	Update Textures

"""

import pygame as pg
import pickle
from time import sleep
pg.init()
pg.display.set_caption('The Dirty Dozen')
pg.display.set_icon(pg.image.load('0-small.png'))

# Constants:
tileLength = 100
marginLength = 25
boardWidth = 6 
boardHeight = 5

# Colors:
green = (100, 255, 100)
grey = (128,128,128)
lightGrey = (211,211,211)

backgroundColor = grey
marginColor = lightGrey

# Calculated Constants
displayW = tileLength * boardWidth + marginLength * 2
displayH = tileLength * boardHeight + marginLength * 2
clock = pg.time.Clock()
screen = pg.display.set_mode((displayW, displayH))

class Board:
	pieceKey = {
	0: [[0, [[0, 0]]], [1, [[2, 0], [3, 0], [2, 1], [3, 1], [2, 2], [3, 2]]], [2, [[4, 0], [4, 1], [4, 2]]], [5, [[0, 3], [3, 3]]], [7, [[1, 3], [4, 3]]]],
	1: [[0, [[0, 0]]], [1, [[2, 0], [3, 0], [4, 0], [3, 1], [4, 1], [2, 1]]], [2, [[0, 2], [2, 2], [4, 2]]], [5, [[0, 3], [3, 3]]], [7, [[1, 3], [4, 3]]]],
	2: [[0, [[0, 0]]], [1, [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4]]], [2, [[0, 2], [0, 3], [0, 4]]], [5, [[3, 0], [3, 2]]], [7, [[4, 0], [4, 2]]]],
	3: [[0, [[0, 0]]], [1, [[5, 0], [5, 1], [5, 2], [4, 2], [4, 3], [4, 4]]], [2, [[2, 2], [2, 3], [2, 4]]], [5, [[2, 0], [0, 2]]], [7, [[3, 0], [0, 3]]]],
	4: [[0, [[0, 0]]], [1, [[4, 0], [5, 0], [4, 1], [5, 1], [4, 2], [5, 2]]], [2, [[2, 0], [2, 1], [2, 2]]], [5, [[0, 3], [3, 3]]], [7, [[1, 3], [4, 3]]]],
	5: [[0, [[0, 0]]], [1, [[2, 0], [3, 0], [2, 1], [3, 1], [4, 0], [4, 1]]], [2, [[0, 2], [0, 3], [0, 4]]], [5, [[2, 2], [4, 2]]], [7, [[2, 3], [4, 3]]]],
	6: [[0, [[0, 0]]], [1, [[2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 2]]], [2, [[0, 2], [0, 3], [0, 4]]], [5, [[3, 0], [3, 3]]], [7, [[4, 0], [4, 3]]]],
	7: [[0, [[0, 0]]], [1, [[0, 2], [1, 2], [0, 3], [1, 3], [0, 4], [1, 4]]], [2, [[2, 2], [2, 3], [2, 4]]], [5, [[3, 0], [4, 2]]], [7, [[4, 0], [4, 3]]]],
	8: [[0, [[0, 0]]], [1, [[5, 0], [4, 0], [4, 1], [5, 1], [4, 2], [5, 2]]], [2, [[0, 2], [0, 3], [0, 4]]], [5, [[2, 0], [2, 3]]], [7, [[2, 1], [3, 3]]]],
	9: [[0, [[2, 2]]], [1, [[2, 0], [2, 1], [1, 1], [0, 1], [0, 2], [1, 2]]], [2, [[0, 3], [0, 4], [2, 4]]], [5, [[3, 0], [4, 2]]], [7, [[4, 0], [4, 3]]]],
	10: [[0, [[0, 0]]], [1, [[2, 2], [2, 2], [3, 2], [4, 1], [5, 0], [3, 3], [3, 3], [3, 4]]], [2, [[0, 2]]], [3, [[4, 3], [5, 3]]], [5, [[3, 0], [0, 3]]], [7, [[1, 3], [4, 1]]]],
	11: [[0, [[2, 2]]], [1, [[0, 2], [1, 2], [1, 3], [0, 3], [0, 4], [1, 4]]], [2, [[2, 4]]], [3, [[5, 1], [4, 2]]], [5, [[1, 0], [4, 0]]], [7, [[2, 0], [4, 3]]]],
	12: [[0, [[0,0]]]]
	}

	def place_pieces(self):
		pieces = Board.pieceKey[self.level]
		self.pieces = []
		for shape, tiles in pieces:
			for pos in tiles:
				self.pieces.append(Piece(self, shape, pos))

	def draw_background(self):
		"""Draws the simple background with margins"""
		screen.fill(marginColor)
		x, y = (marginLength, marginLength)
		width = tileLength * boardWidth
		height = tileLength * boardHeight
		pg.draw.rect(screen, backgroundColor, (x, y, width, height))

	def get_piece(self, tile):
		x, y = tile
		if x < 0 or y < 0 or x > 5 or y > 4:
			return 1
		for piece in self.pieces:
			if tile in piece.tiles:
				return piece
		return None

	@staticmethod
	def mouse_tile(pos):
		if pos[0] < marginLength or pos[0] > marginLength + tileLength * boardWidth:
			return None
		elif pos[1] < marginLength or pos[1] > marginLength + tileLength * boardHeight:
			return None
		else:
			return [int((pos[0] - marginLength) / tileLength), int((pos[1] - marginLength) / tileLength)]
	@staticmethod
	def color_tile(tile, color):
		x, y = Piece.find_exact_pos(tile)
		pg.draw.rect(screen, color, (x, y, tileLength, tileLength))


class Piece:
	tileKey = {
	0: [(0, 0), (1, 0), (1, 1), (0, 1)], 
	1: [(0, 0)], 
	2: [(0, 0), (1, 0)], 
	3: [(0, 0), (0, 1)], 
	4: [(0, 0), (0, 1), (1, 1)], 
	5: [(0, 0), (0, 1), (1, 0)], 
	6: [(0, 0), (1, 0), (1, 1)], 
	7: [(0, 1), (1, 0), (1, 1)]
	}

	def __init__(self, board, shape, pos):
		"""Refer to 'Shape key.png' for meaning of self.shape and position of self.pos"""
		self.board = board
		self.shape = shape
		self.image = self.get_image()
		self.pos = pos
		self.exact_pos = self.find_exact_pos(self.pos)
		self.tiles = self.get_tiles()
		self.grabbed = False
		self.pushed = False

	def grab(self, mouse_pos):
		"""This method is run when the piece is first clicked on."""
		self.grabbed = True
		self.pushed_pieces = []
		self.initial_mouse_pos = mouse_pos
		self.mouse_offset = [self.exact_pos[0] - mouse_pos[0], self.exact_pos[1] - mouse_pos[1]]
		self.determine_axis()

	def push(self, pushed_piece, mouse_pos):
		pushed_piece.pushed = True
		pushed_piece.pushing_piece = self
		self.pushed_pieces.append(pushed_piece)

	def determine_axis(self):
		xaxis = ((-1, 0), (1, 0))
		yaxis = ((0, -1), (0, 1))
		self.xfree = self.movable(xaxis[0]) or self.movable(xaxis[1])
		self.yfree = self.movable(yaxis[0]) or self.movable(yaxis[1])

	def movable(self, direction, is_pushing=False):
		"""determines if the piece is pushable in a given direction. 
		'direction' should be a tuple or list of a relative coordinate. eg. (0, -1) for up and (1, 0) for right"""
		clear = self.clear(direction)
		if type(clear) == list:
			for piece in clear:
				if not piece.movable(direction, is_pushing):
					return False
			return True
		else:
			return clear

	def clear(self, direction):
		"""determines if the squares adjacent to a piece are clear. If there are pieces in the way, returns a list of those pieces.
		'direction' should be a tuple or list of relative coordinate. eg. direction=(0, -1) for up and direction=(1, 0) for right"""
		pieces = []
		for tile in self.tiles:
			pot_piece = self.board.get_piece(self.adjust(tile, direction))
			if pot_piece not in [None, self]:
				if pot_piece == 1:
					return False
				else:
					piece.append(pot_piece)
		if len(pieces) == 0:
			return True
		else:
			return pieces

	def move(self, mouse_pos):
		if self.xfree ^ self.yfree:
			if self.xfree:
				x = mouse_pos[0] + self.mouse_offset[0]
				pushBlock = copy(self.pushed_pieces)
				pushBlock.append(self)

				movable = True
				for mainPiece in pushBlock:
					for mainTile in mainPiece.tiles:
						for otherPiece in self.board.pieces:
							for otherTile in otherPiece.tiles:




			else:
				y = mouse_pos[1] + self.mouse_offset[1]	
				if y < self.first_boundary:
					y = self.first_boundary
				elif y > self.second_boundary:
					y = self.second_boundary
				self.exact_pos[1] = y
			self.set_new_pos()

		elif self.xfree and self.yfree:
			mouse_delta = self.adjust(mouse_pos, self.initial_mouse_pos, negate=True)
			if abs(mouse_delta[0]) > abs(mouse_delta[1]):
				self.yfree = False
			elif abs(mouse_delta[0]) < abs(mouse_delta[1]):
				self.xfree = False
	
	def collide(self, other):
		for selfTile in self.tiles:
			for otherTile in other.tiles:
				selfPos = self.adjust()

	def drop(self):
		self.grabbed = False
		self.exact_pos = self.find_exact_pos(self.pos)
		#Test for win condition:
		if self.shape == 0 and self.pos == [boardWidth - 2, boardHeight - 2]:
			self.board.draw_background()
			for piece in self.board.pieces:
				piece.draw()
			win()

	def set_new_pos(self):
		self.pos = self.find_closest_tile(self.exact_pos)
		self.tiles = self.get_tiles()

	def get_tiles(self):
		tiles = []
		rel_poses = Piece.tileKey[self.shape]
		for rel_pos in rel_poses:
			tile = [self.pos[0] + rel_pos[0], self.pos[1] + rel_pos[1]]
			tiles.append(tile)
		return tiles

	def get_image(self):
		file_path = f'{self.shape}.png'
		return Image(file_path)

	def draw(self):
		screen.blit(self.image.image, self.exact_pos)

	@staticmethod
	def find_exact_pos(pos):
		return [marginLength + pos[0] * tileLength, marginLength + pos[1] * tileLength]

	@staticmethod
	def find_closest_tile(exact_pos):
		tile = [round((exact_pos[0] - marginLength) / tileLength), round((exact_pos[1] - marginLength) / tileLength)]
		return tile

	@staticmethod
	def adjust(l1, l2, negate=False):
		if negate:
			return [x - y for x, y in zip(l1, l2)]
		else:
			return [x + y for x, y in zip(l1, l2)]


class Image:
	def __init__(self, filename):
		self.filename = filename
		self.filepath = filename
		self.image = pg.image.load(self.filepath)
		self.size = self.image.get_size()
		self.width, self.height = self.size


	def center(self):
		return (self.center_W(), self.center_H())


	def center_W(self):
		return int((displayW - self.width) / 2)


	def center_H(self):
		return int((displayH - self.height) / 2)


def normalize(pos):
	direction = []
	for i in pos:
		direction.append(int(i/abs(i)))
	return direction

def reset_wins():
	playerdata = open('playerdata.pickle', 'wb')
	won_boards = [False for i in range(12)]
	pickle.dump(won_boards, playerdata)
	playerdata.close()

def win():
	playerdata = open('playerdata.pickle', 'rb')
	won_boards = pickle.load(playerdata)
	won_boards[board.level] = True
	playerdata.close()
	playerdata = open('playerdata.pickle', 'wb')
	pickle.dump(won_boards, playerdata)
	playerdata.close()

	winImage = Image("You Win.png")
	screen.blit(winImage.image, winImage.center())
	locked = True
	pg.display.update()
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
				pg.quit()
				quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
					pg.quit()
					quit()
				else:
					board.pieces = []
					main()


def level_select():
	"""Displays the 'Select level:' screen. Returns the board choice (0-11)"""
	global board
	board = Board()

	levelSelectImage = Image('Level Select.png')
	levelsImage = Image('Levels.png')
	screen.fill(lightGrey)

	playerdata = open('playerdata.pickle', 'rb') 
	won_boards = pickle.load(playerdata)
	for b, i in enumerate(won_boards):
		if i:
			tile = (b % 6, b // 6 + 3)
			Board.color_tile(tile, green)
	playerdata.close()

	screen.blit(levelSelectImage.image, (levelSelectImage.center_W(), int(displayH * 0.20)))
	screen.blit(levelsImage.image, (levelsImage.center_W(), 320))
	
	pg.display.update()

	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
				pg.quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
					pg.quit()
					quit()
				elif event.key == pg.K_t:
					locked = False
					board.level = 12
					board.place_pieces()
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				pressed_tile = Board.mouse_tile(event.pos)
				if pressed_tile != None and pressed_tile[1] in (3, 4):
					boardChoice = (pressed_tile[0] + 6 * (pressed_tile[1] - 3))
					locked = False
					board.level = boardChoice
					board.place_pieces()
	print(board.level)


def startup():
	screen.fill(lightGrey)
	ddImage = Image('Intro Splash.png')
	screen.blit(ddImage.image, ddImage.center())
	pg.display.update()
	sleep(2)


def main():
	level_select()
	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				pressed_tile = Board.mouse_tile(event.pos)
				if pressed_tile != None:
					grabbed_piece = board.get_piece(pressed_tile)
					if grabbed_piece not in [1, None]:
						grabbed_piece.grab(event.pos)

			elif event.type == pg.MOUSEBUTTONUP:
				for piece in board.pieces:
					if piece.grabbed:
						piece.drop()

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				elif event.key == pg.K_r:
					board.pieces = []
					main()

		mouse_pos = pg.mouse.get_pos()
		for piece in board.pieces:
			if piece.grabbed or piece.pushed:
				piece.move(mouse_pos)

		board.draw_background()
		for piece in board.pieces:
			piece.draw()
		pg.display.update()
		clock.tick()

	pg.quit()
	quit()


startup()
main()