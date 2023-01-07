import PySimpleGUI as sg 
from random import choice
from csv import reader, writer
import json

sg.theme('Black')

red ='#90090d'
blue = '#190aa1'
green = '#097325'
yellow = '#b5ad14'
purple = '#720278'
pink = '#e8a2eb'
orange = '#a1610d'
silver = '#505050'

colors = [red, blue, green, yellow, purple]

high_scores = {'Endless':[['Zorak',1705,192,0],
						['Actual Cat',1600,175,0],
						['Pinky Toe',1203,143,0],
						['Eat',990,128,0],
						['at',870,103,0],
						['Joe\'s',620,70,0],
						['HAM',310,90,0],
						['AAA',250,82,0],
						['PAC',180,65,0],
						['???',10,7,0]],
				'Marathon 50':[['Jimmy',601,0,0],
								['???',600,0,0],
								['Joe\'s',528,0,0],
								['at',492,0,0],
								['HAM',463,0,0],
								['Zorak',410,0,0],
								['Eat',387,0,0],
								['PAC',238,0,0],
								['AAA',150,0,0],
								['Actual Cat',32,0,0]],
				'Marathon 100':[['Jimmy',830,0,0],
								['HAM',735,0,0],
								['at',710,0,0],
								['Zorak',699,0,0],
								['PAC',624,0,0],
								['AAA',601,0,0],
								['Actual Cat',555,0,0],
								['???',350,0,0],
								['Fake Cat',120,0,0],
								['Todd',0,0,0]]
								}

try:
	with open('scores.dat', 'r') as file:
		high_scores = json.load(file)
except FileNotFoundError:
	pass



move = 0
score = 0
game=False
moves_left = True
player_name = ''
mode = 'Endless'
mara_limit = 0
endless_tt = 'Play until you run out of moves! Careful, it gets harder the more you match!'
marathon_50_tt = 'Score as high as you can in 50 moves!'
marathon_100_tt = 'Score as high as you can in 100 moves!'

def save_high_scores():
	global high_scores
	with open('scores.dat', 'w') as file:
		json.dump(high_scores, file)


def randomize_colors():
	for row in blocks:
		for block in row:
			window[block.key].update(button_color=choice(colors))

def clear_blocks(block_key, mode):
	global move, score
	below = (block_key[0], block_key[1]-1)
	above = (block_key[0], block_key[1]+1)
	right = (block_key[0]+1, block_key[1])
	left = (block_key[0]-1, block_key[1])
	adjacent = [left, right, above, below]
	target_color = window[block_key].ButtonColor
	points = 0
	combo = 0
	valid_move = False
	while adjacent:
		for block in adjacent:
			if block[0] >=0 and block[0] <= 8 and block[1] >=0 and block[1] <= 8:
				if window[block].ButtonColor == target_color:
					valid_move=True
					match combo:
						case 0:
							points += 1
							combo += 1
						case 1:
							points += 2
							combo += 1
						case 2:
							points += 3
							combo += 1
						case 3:
							points += 4
							combo += 1
						case 4:
							points += 6
							combo += 1
						case 5:
							points += 8
							combo += 1
						case 6:
							points += 10
							combo += 1
						case 7:
							points += 12
							combo += 1
						case 8:
							points += 15
							combo += 1
						case other:
							points += 20
							combo += 1 
					window[block].update(button_color = '#ffffff')
					window[block_key].update(button_color = '#ffffff')
					if window[block].key[1] -1 >= 0:
						adjacent.append((window[block].key[0], window[block].key[1]-1))
					if window[block].key[1] +1 <= 8:
						adjacent.append((window[block].key[0], window[block].key[1]+1))
					if window[block].key[0] -1 >= 0:
						adjacent.append((window[block].key[0]-1, window[block].key[1]))
					if window[block].key[0] +1 <= 8:
						adjacent.append((window[block].key[0]+1, window[block].key[1]))
			adjacent.remove(block)
	score += points
	window['SCORE'].update(score)
	if valid_move:
		if mode == 'Endless':
			move += 1
		else:
			move -= 1
		match combo:
			case 0:
				window['COMBO'].update(' ')
			case 1:
				window['COMBO'].update(' ')
			case 2:
				window['COMBO'].update(' ')
			case 3:
				window['COMBO'].update(' ')
			case 4:
				window['COMBO'].update('Good Combo!')
			case 5:
				window['COMBO'].update('Good Combo!')
			case 6:
				window['COMBO'].update('Great Combo!')
			case 7:
				window['COMBO'].update('Super Combo!')
			case 8:
				window['COMBO'].update('Giga Combo!')
			case other:
				window['COMBO'].update('ULTRA COMBO!!')

		window['MOVES'].update(move)

def blocks_fall(block_grid):
	block_grid.reverse()
	for x in range(10):
		for block in block_grid:
			if window[block].key[1] <8:
				if window[block].ButtonColor == ('#000000','#ffffff'):
					window[block].update(button_color=window[((window[block].key[0]),(window[block].key[1]+1))].ButtonColor)
					window[((window[block].key[0]),(window[block].key[1]+1))].update(button_color='#FFFFFF')
			else:
				if window[block].ButtonColor == ('#000000','#ffffff'):
					window[block].update(button_color=choice(colors))

def check_for_moves(block_grid):
	for block in block_grid:
		below = (block[0], block[1]-1)
		above = (block[0], block[1]+1)
		right = (block[0]+1, block[1])
		left = (block[0]-1, block[1])
		adjacent = [left, right, above, below]
		target_color = window[block].ButtonColor
		for sub_block in adjacent:
			if sub_block[0] >=0 and sub_block[0] <= 8 and sub_block[1] >=0 and sub_block[1] <= 8:
				if window[sub_block].ButtonColor == target_color:
					return True
	return False

def game_over(score, moves, mode, m_moves=0):
	global high_scores, player_name
	game_mode = 'Endless'

	if mode == 'Marathon':
		moves = m_moves - moves
		if m_moves == 50:
			game_mode = 'Marathon 50'
		else:
			game_mode = 'Marathon 100'

	if len(player_name) > 10:
		player_name = player_name[:10]



	high_scores[game_mode].append([player_name, score, moves, game_mode])
	high_scores[game_mode].sort(reverse=True, key=lambda x:int(x[1]))

	if len(high_scores[game_mode])>10:
		high_scores[game_mode].pop()
	save_high_scores()



	layout = [	[sg.Text('Game Over!')],
				[sg.Text(f'{mode} Mode')],
				[sg.Text(f'You scored {score} points in {moves} moves')],	
				[sg.Button('OK')]	]

	window = sg.Window('Game Over', layout, modal=True, font=('any', 20), element_justification='center')

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

def new_game():
	global move, mode, mara_limit, player_name

	layout = [	[sg.Text('Welcome to the game! To start, please select\na mode and enter your name.')],
				[sg.InputText(size=15, key='NAME')],
				[sg.Button(button_text='Endless Mode', tooltip=endless_tt, size=13),
				sg.Button(button_text='Marathon 50', tooltip=marathon_50_tt, size=13),
				sg.Button(button_text='Marathon 100', tooltip=marathon_100_tt, size=13)]	]

	window = sg.Window('New Game', layout, font=('any', 20), modal=True, disable_close=True, disable_minimize=True, element_justification='center')

	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED:

			break
		if event == 'Endless Mode' and values['NAME']:
			move = 0
			mode = 'Endless'
			mara_limit = 0
			player_name = values['NAME']
			break
		if event == 'Marathon 50' and values['NAME']:
			move = 50
			mode = 'Marathon'
			mara_limit = 50
			player_name = values['NAME']
			break
		if event == 'Marathon 100' and values['NAME']:
			move = 100
			mode = 'Marathon'
			mara_limit = 100
			player_name = values['NAME']
			break


	window.close()

def about():

	layout = [	[sg.Text('Program by Reimi Wazny')],
				[sg.Text('Powered by Python and PySimpleGUI.')],
				[sg.OK()]]

	window = sg.Window('About', layout, font=('any',20), element_justification='center')

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

def how_to_play(red=red,blue=blue,green=green,yellow=yellow):

	ex_blocks_line = [	[sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', blue), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', green), disabled=True)],
						[sg.Button(size=(3,1),pad=0,button_color=('#000000', yellow), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', yellow), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', yellow), disabled=True)],
						[sg.Button(size=(3,1),pad=0,button_color=('#000000', blue), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', green), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True)],
						[sg.Text('V')],
						[sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', yellow), disabled=True)],
						[sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', blue), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', green), disabled=True)],
						[sg.Button(size=(3,1),pad=0,button_color=('#000000', blue), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', green), disabled=True),sg.Button(size=(3,1),pad=0,button_color=('#000000', red), disabled=True)]]

	explanation = [	[sg.Text('Click on groups of two or more\nblocks to clear them for points!')],
					[sg.Text('When you clear blocks, the \nblocks above will fall down.\nIf you can\'t make any more\nmoves, game over!')],
					[sg.Text('The more blocks you clear at once,\nthe more points you get!')]	]


	layout = [	[sg.Frame(title=None,layout=ex_blocks_line, element_justification='center', border_width=0), sg.Frame(title=None,layout=explanation, border_width=0)],
				[sg.OK()]	]

	window = sg.Window(title='How to Play', layout=layout, font=('any',20), modal=True, element_justification='center')

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'OK'):
			break

	window.close()

def show_high_scores(scores):

	endless_win = [	[sg.Text(f'{scores["Endless"][0][0]} . . . {scores["Endless"][0][1]}pts. in {scores["Endless"][0][2]} moves', size=30, justification='center')],
					[sg.Text(f'{scores["Endless"][1][0]} . . . {scores["Endless"][1][1]}pts. in {scores["Endless"][1][2]} moves')],
					[sg.Text(f'{scores["Endless"][2][0]} . . . {scores["Endless"][2][1]}pts. in {scores["Endless"][2][2]} moves')],
					[sg.Text(f'{scores["Endless"][3][0]} . . . {scores["Endless"][3][1]}pts. in {scores["Endless"][3][2]} moves')],
					[sg.Text(f'{scores["Endless"][4][0]} . . . {scores["Endless"][4][1]}pts. in {scores["Endless"][4][2]} moves')],
					[sg.Text(f'{scores["Endless"][5][0]} . . . {scores["Endless"][5][1]}pts. in {scores["Endless"][5][2]} moves')],
					[sg.Text(f'{scores["Endless"][6][0]} . . . {scores["Endless"][6][1]}pts. in {scores["Endless"][6][2]} moves')],
					[sg.Text(f'{scores["Endless"][7][0]} . . . {scores["Endless"][7][1]}pts. in {scores["Endless"][7][2]} moves')],
					[sg.Text(f'{scores["Endless"][8][0]} . . . {scores["Endless"][8][1]}pts. in {scores["Endless"][8][2]} moves')],
					[sg.Text(f'{scores["Endless"][9][0]} . . . {scores["Endless"][9][1]}pts. in {scores["Endless"][9][2]} moves')]	]

	m_50_win = [	[sg.Text(f'{scores["Marathon 50"][0][0]} . . . {scores["Marathon 50"][0][1]}pts.', size=30, justification='center')],
					[sg.Text(f'{scores["Marathon 50"][1][0]} . . . {scores["Marathon 50"][1][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][2][0]} . . . {scores["Marathon 50"][2][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][3][0]} . . . {scores["Marathon 50"][3][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][4][0]} . . . {scores["Marathon 50"][4][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][5][0]} . . . {scores["Marathon 50"][5][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][6][0]} . . . {scores["Marathon 50"][6][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][7][0]} . . . {scores["Marathon 50"][7][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][8][0]} . . . {scores["Marathon 50"][8][1]}pts.')],
					[sg.Text(f'{scores["Marathon 50"][9][0]} . . . {scores["Marathon 50"][9][1]}pts.')]	]

	m_100_win = [	[sg.Text(f'{scores["Marathon 100"][0][0]} . . . {scores["Marathon 100"][0][1]}pts.', size=30, justification='center')],
					[sg.Text(f'{scores["Marathon 100"][1][0]} . . . {scores["Marathon 100"][1][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][2][0]} . . . {scores["Marathon 100"][2][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][3][0]} . . . {scores["Marathon 100"][3][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][4][0]} . . . {scores["Marathon 100"][4][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][5][0]} . . . {scores["Marathon 100"][5][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][6][0]} . . . {scores["Marathon 100"][6][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][7][0]} . . . {scores["Marathon 100"][7][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][8][0]} . . . {scores["Marathon 100"][8][1]}pts.')],
					[sg.Text(f'{scores["Marathon 100"][9][0]} . . . {scores["Marathon 100"][9][1]}pts.')]	]

	layout = [	[sg.Frame(title='Endless', layout=endless_win, title_location='n', element_justification='center'),
				sg.Frame(title='Marathon 50', layout=m_50_win, title_location='n', element_justification='center'),
				sg.Frame(title='Marathon 100', layout=m_100_win, title_location='n', element_justification='center')],
				[sg.Button('Back')] ]

	window = sg.Window('High Scores', layout, font=('any', 14), modal=True)

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, 'Back'):
			break

	window.close()

	


menu_def = [	['&Game', ['&New Game', 'High &Scores', '&Quit']],
				['&Help',['How to &Play', '&About']]
		]

blocks = [	[sg.Button(size=(3,1),pad=0,key=(0,8)),sg.Button(size=(3,1),pad=0,key=(1,8)),sg.Button(size=(3,1),pad=0,key=(2,8)),sg.Button(size=(3,1),pad=0,key=(3,8)),sg.Button(size=(3,1),pad=0,key=(4,8)),sg.Button(size=(3,1),pad=0,key=(5,8)),sg.Button(size=(3,1),pad=0,key=(6,8)),sg.Button(size=(3,1),pad=0,key=(7,8)),sg.Button(size=(3,1),pad=0,key=(8,8))],
			[sg.Button(size=(3,1),pad=0,key=(0,7)),sg.Button(size=(3,1),pad=0,key=(1,7)),sg.Button(size=(3,1),pad=0,key=(2,7)),sg.Button(size=(3,1),pad=0,key=(3,7)),sg.Button(size=(3,1),pad=0,key=(4,7)),sg.Button(size=(3,1),pad=0,key=(5,7)),sg.Button(size=(3,1),pad=0,key=(6,7)),sg.Button(size=(3,1),pad=0,key=(7,7)),sg.Button(size=(3,1),pad=0,key=(8,7))],
			[sg.Button(size=(3,1),pad=0,key=(0,6)),sg.Button(size=(3,1),pad=0,key=(1,6)),sg.Button(size=(3,1),pad=0,key=(2,6)),sg.Button(size=(3,1),pad=0,key=(3,6)),sg.Button(size=(3,1),pad=0,key=(4,6)),sg.Button(size=(3,1),pad=0,key=(5,6)),sg.Button(size=(3,1),pad=0,key=(6,6)),sg.Button(size=(3,1),pad=0,key=(7,6)),sg.Button(size=(3,1),pad=0,key=(8,6))],
			[sg.Button(size=(3,1),pad=0,key=(0,5)),sg.Button(size=(3,1),pad=0,key=(1,5)),sg.Button(size=(3,1),pad=0,key=(2,5)),sg.Button(size=(3,1),pad=0,key=(3,5)),sg.Button(size=(3,1),pad=0,key=(4,5)),sg.Button(size=(3,1),pad=0,key=(5,5)),sg.Button(size=(3,1),pad=0,key=(6,5)),sg.Button(size=(3,1),pad=0,key=(7,5)),sg.Button(size=(3,1),pad=0,key=(8,5))],
			[sg.Button(size=(3,1),pad=0,key=(0,4)),sg.Button(size=(3,1),pad=0,key=(1,4)),sg.Button(size=(3,1),pad=0,key=(2,4)),sg.Button(size=(3,1),pad=0,key=(3,4)),sg.Button(size=(3,1),pad=0,key=(4,4)),sg.Button(size=(3,1),pad=0,key=(5,4)),sg.Button(size=(3,1),pad=0,key=(6,4)),sg.Button(size=(3,1),pad=0,key=(7,4)),sg.Button(size=(3,1),pad=0,key=(8,4))],
			[sg.Button(size=(3,1),pad=0,key=(0,3)),sg.Button(size=(3,1),pad=0,key=(1,3)),sg.Button(size=(3,1),pad=0,key=(2,3)),sg.Button(size=(3,1),pad=0,key=(3,3)),sg.Button(size=(3,1),pad=0,key=(4,3)),sg.Button(size=(3,1),pad=0,key=(5,3)),sg.Button(size=(3,1),pad=0,key=(6,3)),sg.Button(size=(3,1),pad=0,key=(7,3)),sg.Button(size=(3,1),pad=0,key=(8,3))],
			[sg.Button(size=(3,1),pad=0,key=(0,2)),sg.Button(size=(3,1),pad=0,key=(1,2)),sg.Button(size=(3,1),pad=0,key=(2,2)),sg.Button(size=(3,1),pad=0,key=(3,2)),sg.Button(size=(3,1),pad=0,key=(4,2)),sg.Button(size=(3,1),pad=0,key=(5,2)),sg.Button(size=(3,1),pad=0,key=(6,2)),sg.Button(size=(3,1),pad=0,key=(7,2)),sg.Button(size=(3,1),pad=0,key=(8,2))],
			[sg.Button(size=(3,1),pad=0,key=(0,1)),sg.Button(size=(3,1),pad=0,key=(1,1)),sg.Button(size=(3,1),pad=0,key=(2,1)),sg.Button(size=(3,1),pad=0,key=(3,1)),sg.Button(size=(3,1),pad=0,key=(4,1)),sg.Button(size=(3,1),pad=0,key=(5,1)),sg.Button(size=(3,1),pad=0,key=(6,1)),sg.Button(size=(3,1),pad=0,key=(7,1)),sg.Button(size=(3,1),pad=0,key=(8,1))],
			[sg.Button(size=(3,1),pad=0,key=(0,0)),sg.Button(size=(3,1),pad=0,key=(1,0)),sg.Button(size=(3,1),pad=0,key=(2,0)),sg.Button(size=(3,1),pad=0,key=(3,0)),sg.Button(size=(3,1),pad=0,key=(4,0)),sg.Button(size=(3,1),pad=0,key=(5,0)),sg.Button(size=(3,1),pad=0,key=(6,0)),sg.Button(size=(3,1),pad=0,key=(7,0)),sg.Button(size=(3,1),pad=0,key=(8,0))]	]

grid = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),
		(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),
		(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),
		(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),
		(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),
		(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),
		(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),
		(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),
		(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]

status_window = [	[sg.Text('Endless', key='MODE', size=15, justification='center')],
					[sg.Text('SCORE')],
					[sg.Text(000000000, key='SCORE')],
					[sg.Text('MOVES')],
					[sg.Text(0, key='MOVES')],
					[sg.Text('', key='COMBO')]
					]

layout = [[sg.Menu(menu_def, tearoff=False, pad=(200,1), font=('any',10), background_color = '#ffffff', text_color='#000000')],
		[sg.Frame(title=None, border_width=0, layout = blocks), sg.Frame(title=None, layout=status_window, element_justification='center')] ]

window = sg.Window('Block Matcher', layout, font=('any', 20))



while True:
	event, values = window.read()
	if event in (sg.WIN_CLOSED,'Quit'):
		break
	if event == 'How to Play':
		how_to_play()
	if event == 'About':
		about()
	if event == 'High Scores':
		show_high_scores(high_scores)
	if event == 'New Game':
		window['SCORE'].update(000000000)
		score = 0
		new_game()
		if mode == 'Endless':
			colors = [red, blue, green, yellow, purple]
		elif mode == 'Marathon' and mara_limit == 50:
			colors = [red, blue, green, yellow, purple, pink]
		else:
			colors = [red, blue, green, yellow, purple, pink, orange]
		window['MODE'].update(mode)
		window['MOVES'].update(move)
		window['COMBO'].update('')
		randomize_colors()
		game=True
		moves_left=True
	if game:
		moves_left = check_for_moves(grid)
		if mode == 'Marathon' and move == 0:
			moves_left = False
		if moves_left:
			if mode == 'Endless':
				if move == 50:
					colors.append(pink)
				elif move == 100:
					colors.append(orange)
				elif move == 150:
					colors.append(silver)
			if event in grid:
				if window[event].ButtonColor != ('#000000','#ffffff'):
					clear_blocks(event, mode)
					blocks_fall(grid)

		else:
			game=False

			game_over(score, move, mode, mara_limit)


