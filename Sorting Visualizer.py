import pygame as pg
import random
import math

pg.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    ORANGE = 255, 165, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128 ,128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pg.font.SysFont('comicsans', 30)
    LARGE_FONT = pg.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150
    Y_MIN = 5

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pg.display.set_mode((width, height))
        pg.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = ((self.height - self.TOP_PAD) // (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending, key_val):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'} - Speed = {key_val}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, draw_info.Y_MIN))
    
    controls = draw_info.FONT.render("SPACE = Start Sorting | R = Reset | A = Ascending | D = Decending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, draw_info.Y_MIN +55))
    
    sorting = draw_info.FONT.render("Sort Type: B = Bubble | S = Selection | I = Insertion | Q = Quick", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, draw_info.Y_MIN + 95))
    
    draw_list(draw_info)
    pg.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pg.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pg.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pg.display.update()

def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.RED, j + 1: draw_info.GREEN}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i -=  1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.RED, i: draw_info.GREEN}, True)
            yield True

    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        cur_min = i

        for j in range(i, len(lst)):
            if (lst[j] < lst[cur_min] and ascending) or (lst[j] > lst[cur_min] and not ascending):
                cur_min = j
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.ORANGE, cur_min: draw_info.RED}, True)
            yield True
            
        lst[i], lst[cur_min] = lst[cur_min], lst[i]

        draw_list(draw_info, {i: draw_info.GREEN, cur_min: draw_info.RED}, True)
        yield True

    return lst

def quick_sort(draw_info, start=0, end=None, ascending=True):
    lst = draw_info.lst

    if end == None:
        end = len(lst) - 1
    
    if start < end:
        pvt_index = partition(lst, start, end, draw_info, ascending)

        quick_sort(lst, start, pvt_index - 1, ascending)
        quick_sort(lst, pvt_index + 1, end, ascending)    
        
    return lst

def partition(lst, start, end, draw_info, ascending=True):
    pvt_index = start
    pvt_value = lst[end]

    for i in range(start, end):
        if (lst[i] < pvt_value and ascending) or (lst[i] > pvt_value and not ascending):
            lst[i], lst[pvt_index] = lst[pvt_index], lst[i]
            pvt_index += 1

        draw_list(draw_info, {start: draw_info.GREEN, pvt_index: draw_info.RED, i: draw_info.ORANGE}, True)
        yield True
        
    lst[pvt_index], lst[end] = lst[end], lst[pvt_index]
    

    return pvt_index

def main():
    running = True
    clock = pg.time.Clock()
    speed = 60
    key_val = 5

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1000, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while running:
        clock.tick(speed)
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, key_val)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type != pg.KEYDOWN:
                continue
            
            if event.key == pg.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pg.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pg.K_a and not sorting:
                ascending = True
            elif event.key == pg.K_d and not sorting:
                ascending = False
            elif 49 <= event.key <= 57:
                key_val = event.key - 48
                multiplier = key_val / 9
                speed = round(60 * multiplier)
            elif event.key == pg.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pg.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pg.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pg.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

    pg.quit()


if __name__ == "__main__":
    main()