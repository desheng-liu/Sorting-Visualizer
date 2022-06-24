import pygame
import random
import math
from playsound import playsound
from pygame.mixer import Sound
pygame.init()



class DrawInformation:
	black = 0, 0, 0
	white = 255, 255, 255
	green = 0, 255, 0
	red = 255, 0, 0
	pasteltan = 248, 228, 204
	background_color = pasteltan

	gradient = [(21, 52, 80), (68, 114, 148), (143, 188, 219)]

	mainfont = pygame.font.SysFont('cosmicsans', 30)
	largefont = pygame.font.SysFont('cosmicsans', 40)

	side_padding = 100
	top_padding = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width,height))
		pygame.display.set_caption("Sorting Algorithm Visualizer")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		# these calulations standardize how tall and wide the pillars that represent the list will be 
		self.block_width = round((self.width - self.side_padding)) / len(lst)
		# total area that is "drawable"/ size of list to figure out width of the blocks
		self.block_height = math.floor((self.height - self.top_padding) / (self.max_val - self.min_val))
		# same thing, just with the height of a "block"
		self.start_xcord = self.side_padding // 2
		#where to start drawing the "blocks" on the screen

def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.background_color)

	title = draw_info.largefont.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.black)
	draw_info.window.blit(title, ( draw_info.width/2 - title.get_width()/2 , 20))

	controls = draw_info.mainfont.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.black)
	draw_info.window.blit(controls, ( draw_info.width/2 - controls.get_width()/2 , 70))

	sorting = draw_info.mainfont.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.black)
	draw_info.window.blit(sorting, ( draw_info.width/2 - sorting.get_width()/2 , 100))


	draw_list(draw_info)
	pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_background = False):
	lst = draw_info.lst

	if clear_background:
		clear_rect = (draw_info.side_padding//2, draw_info.top_padding,
				 draw_info.width - draw_info.side_padding, draw_info.height - draw_info.top_padding)
		pygame.draw.rect(draw_info.window, draw_info.background_color, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_xcord + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.gradient[i % 3] #pillars next to each other will have different shades

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_background:
		pygame.display.update()



#function that generates the list
def generate_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst

#sorting functions
def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst
	sound = pygame.mixer.Sound('sortingsound.mp3')
	for i in range(len(lst) - 1 ):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				#sound.play()
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				#playsound('sortingsound.mp3')
				sound.set_volume(.1)
				sound.play()
				draw_list(draw_info, {j: draw_info.green, j + 1: draw_info.red}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst
	sound = pygame.mixer.Sound('sortingsound.mp3')
	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i -1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break


			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.green, i: draw_info.red}, True)
			sound.set_volume(.1)
			sound.play()
			yield True

	return lst

def selection_sort(draw_info, ascending = True):
	lst = draw_info.lst
	sound = pygame.mixer.Sound('sortingsound.mp3')
	if ascending == True:
		for i in range(len(lst)):
			min_indx = i

			for j in range(i + 1, len(lst)):

				if lst[j] < lst[min_indx]:
					min_indx = j


			lst[i], lst[min_indx] = lst[min_indx], lst[i] 
			draw_list(draw_info, {i: draw_info.green, min_indx: draw_info.red}, True)
			sound.set_volume(.1)
			sound.play()
			yield True

		return lst

	if ascending == False: #for descending sort
		for i in range(len(lst)):
			min_indx = i

			for j in range(i + 1, len(lst)):

				if lst[j] > lst[min_indx]:
					min_indx = j


			lst[i], lst[min_indx] = lst[min_indx], lst[i] 
			draw_list(draw_info, {i: draw_info.green, min_indx: draw_info.red}, True)
			sound.set_volume(.1)
			sound.play()
			yield True

		return lst


#main driver code that renders the screen being displayed
def main():
	run = True
	clock = pygame.time.Clock()

	n = 100
	min_val = 0
	max_val = 200



	lst = generate_list(n, min_val, max_val)
	draw_info = DrawInformation(1200, 600, lst)
	sorting = False
	ascending = True


	sorting_algo = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algo_generator = None


	while run:
		clock.tick(500) # max is x fps being runned
		
		if sorting:
			try:
				next(sorting_algo_generator)
			except StopIteration:
				sorting = False

		else:
			draw(draw_info, sorting_algo_name, ascending)




		for event in pygame.event.get():
			if event.type == pygame.QUIT: #to end the visualizer
				run = False
			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_r:
				lst = generate_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algo_generator = sorting_algo(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algo = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algo = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algo = selection_sort
				sorting_algo_name = "Selection Sort"



	pygame.quit()

if __name__ == "__main__":
	main()




