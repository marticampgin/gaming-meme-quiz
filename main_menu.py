from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
from player import Player

import random
import time
import threading

class Main_menu:
	def __init__(self, root, canvas, win_h, win_w, pictures_path, game):

		# Parameters
		self.root = root
		self.canvas = canvas
		self.pictures_path = pictures_path

		self.win_h = win_h
		self.win_w = win_w

		self.players = []
		self.player_names = []
		self.taken_chars = []
		self.player_tag = "pl0"
		self.player_x = 1080
		self.player_y = 210
		self.pl_name_x = 1062
		self.pl_name_y = 175

		self.moving_constant_x = 160
		self.moving_constant_y = 150

		self.button_width = 210
		self.button_height = 55

		self.logo_x = 1000
		self.logo_y = 40

		self.start_button_x = 1280
		self.start_button_y = 540
		self.exit_button_x = 1280
		self.exit_button_y = 660 

		self.pl_bckg_x = 1000
		self.pl_bckg_y = 40

		self.back_button_x = 1260
		self.back_button_y = 710

		self.add_player_button_x = 1260
		self.add_player_button_y = 540

		self.remove_player_button_x = 1260
		self.remove_player_button_y = 620

		self.start_quiz_button_x = 1520
		self.start_quiz_button_y = 540

		self.finished_flag = False
		self.game = game


		# Images
		self.character_images = [PhotoImage(file=self.pictures_path + "chars" + "\\" + str(i) + ".png") for i in range(1, 99)]

		self.bgimg = PhotoImage(file=self.pictures_path + "background.png")
		self.logo = PhotoImage(file=self.pictures_path + "logo.png")
		self.player_background_img = PhotoImage(file=self.pictures_path + "charboard.png")

		self.start_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "start.png")
		self.quit_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "quit.png")
		self.back_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "back.png")
		self.add_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "add_player.png")
		self.remove_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "remove_player.png")
		self.lesgo_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "les_go.png")


		# Widgets
		self.player_count_entry = Entry(self.root, width=50)
		self.quiz_progress_bar = ttk.Progressbar(root, 
												orient=HORIZONTAL,
												length=700, 
												mode="determinate")

		
		self.start_game_button = Button(self.root,  
										width=self.button_width, 
										height=self.button_height, 
									    command=self.start_game,
									    image=self.start_img,
									    bd=0)

		self.exit_game_button = Button(self.root, 
									   width=self.button_width, 
									   height=self.button_height,
									   image=self.quit_img,
									   command=lambda: self.root.quit(),
									   bd=0)

		self.back_button = Button(self.root,  
								  width=self.button_width, 
								  height=self.button_height,
								  image=self.back_img, 
							      command=self.go_back_to_menu,
								  bd=0)


		self.add_player_button = Button(self.root,
										width=self.button_width,
										height=self.button_height,
										image=self.add_img,
										command=self.add_player,
										bd=0)

		self.remove_player_button = Button(self.root,
										   width=self.button_width,
										   height=self.button_height,
										   image=self.remove_img,
										   command=self.remove_player,
										   bd=0)

		self.start_quiz_button = Button(self.root,
										width=self.button_width,
										height=self.button_height,
										image=self.lesgo_img,
										command=self.start_quiz,
										bd=0)


		# Init sound engine
		mixer.init()

		# Initiating main menu
		self.canvas.create_image((0, 0), anchor="nw", image=self.bgimg, tag="bg")
		self.canvas.create_image((self.logo_x, self.logo_y), anchor="nw", image=self.logo, tag="logo")
		self.start_game_button.place(x=self.start_button_x, y=self.start_button_y)
		self.exit_game_button.place(x=self.exit_button_x, y=self.exit_button_y)

		mixer.music.load(r"audio\intro.mp3")
		mixer.music.play()


	def start_game(self):
		"""
		Hides buttons, logo, adds new buttons and a player board.
		Equal to switching to 'add player menu'
		"""

		# Hide buttons/logos
		self.start_game_button.place_forget()
		self.exit_game_button.place_forget()
		self.canvas.delete("logo")

		# Place new buttons/widgets
		self.back_button.place(x=self.back_button_x, y=self.back_button_y)
		self.add_player_button.place(x=self.add_player_button_x, y=self.add_player_button_y)
		self.remove_player_button.place(x=self.remove_player_button_x, y=self.remove_player_button_y)
		self.start_quiz_button.place(x=self.start_quiz_button_x, y=self.start_quiz_button_y)

		self.canvas.create_image((self.pl_bckg_x, self.pl_bckg_y), 
								anchor="nw", 
								image=self.player_background_img, 
								tag="player_board")


	def go_back_to_menu(self):
		"""
		Goes back to the main menu by hiding buttons/widgets
		and placing menu buttons and widgets
		"""

		# Hide buttons/widgets
		self.canvas.delete("player_board")

		self.back_button.place_forget()
		self.add_player_button.place_forget()
		self.remove_player_button.place_forget()
		self.start_quiz_button.place_forget()

		# Remove newly added players
		for _ in range(len(self.players)):
			self.remove_player()

		# Restore main menu
		self.canvas.create_image((self.logo_x, self.logo_y), anchor="nw", image=self.logo, tag="logo")

		self.start_game_button.place(x=self.start_button_x, y=self.start_button_y)
		self.exit_game_button.place(x=self.exit_button_x, y=self.exit_button_y)



	def add_player(self):
		"""
		Adds a new player. Max. num. of players = 8.
		Each char. icon is chosen randomly. 

		"""
		if len(self.players) < 8:
			char_index = random.randint(0, len(self.character_images)-1)  # random char.
			character = self.character_images.pop(char_index)
			self.taken_chars.append(character)
			self.player_tag = self.player_tag[:-1] + str(int(self.player_tag[-1]) + 1)
			self.canvas.create_image((self.player_x, self.player_y), 
									anchor="nw", 
									image=character, 
									tag=self.player_tag)

			player_name = Entry(self.root, width=15)
			player_name.place(x=self.pl_name_x, y=self.pl_name_y)

			player = Player(character)
			player.assign_name(player_name.get())

			self.players.append(player)
			self.player_names.append(player_name)

			self.player_x += self.moving_constant_x
			self.pl_name_x += self.moving_constant_x

			# If 4 chars. are present, switch to a lower row to all
			# chars. on the player board widget
			if len(self.players) == 4:
				self.player_y += self.moving_constant_y
				self.player_x = 1080
				self.pl_name_y += self.moving_constant_y
				self.pl_name_x = 1062

	def remove_player(self):
		"""
		Removes the player. Restores previous char. logo position,
		removes char. from the char list. 
		"""
		if len(self.players) > 0:
			# If deleted char. was the 5-th one, move coordinates to upper row
			if len(self.players) == 4:
				self.player_x += self.moving_constant_x * 3
				self.pl_name_x += self.moving_constant_x * 3
				self.player_y -= self.moving_constant_y
				self.pl_name_y -= self.moving_constant_y

			else:
				self.player_x -= self.moving_constant_x
				self.pl_name_x -= self.moving_constant_x

			del self.players[-1]
			self.player_names[-1].place_forget()
			del self.player_names[-1]
			character = self.taken_chars.pop(-1)
			self.character_images.append(character) # appends the char. back to the pool

			self.canvas.delete(self.player_tag)
			self.player_tag = self.player_tag[:-1] + str(int(self.player_tag[-1]) - 1)


	def remove_player_icons(self):
		"""
		Hides each chars. icon based on their tag. 
		"""
		tag = "pl0"
		for i in range(1, len(self.players) + 1):
			tag = tag[:-1] + str(int(tag[-1]) + 1)
			self.canvas.delete(tag)

		for name in self.player_names:
			name.place_forget()


	def start_quiz(self):
		"""
		Starts the quiz. Assigns given name to each char. Hides buttons/widgets. 
		"""
		if len(self.players) >= 2:   # only if two players are present
			mixer.music.load(r"audio\obeme.mp3")
			mixer.music.play()

			for i, name in enumerate(self.player_names):
				self.players[i].assign_name(name)

			# Hide buttons/widgets
			self.remove_player_icons()
			self.back_button.place_forget()

			self.add_player_button.place_forget()
			self.remove_player_button.place_forget()
			self.start_quiz_button.place_forget()

			self.canvas.delete("player_board")

			# Place progresss bar
			self.quiz_progress_bar.place(x=980, y=400)

			random_sentences = ["Звоним Тинькову..",
								"Запускаем струю Дона Симона..",
								"Нажимаем на красную кнопку..",
								"SUS",
								"Записываем обращение Обэме..",
								]

			# Just adds more diversity to the loading bar                       
			for i in range(5):
				self.canvas.delete("text")

				idx = random.randint(0, len(random_sentences) - 1)

				text = random_sentences.pop(idx)
				text_canvas = self.canvas.create_text(980, 430, anchor="nw", tag="text")
				self.canvas.itemconfig(text_canvas, text=text, fill="black", font='Helvetica 20 bold')

				self.quiz_progress_bar["value"] += 20

				self.root.update()

				# Sleep for 1-3 seconds, drawn uniformly
				wait_time = random.uniform(1, 3)
				time.sleep(wait_time)

			# Add last piece of text after "loading"
			self.canvas.delete("text")
			text_canvas = self.canvas.create_text(980, 430, anchor="nw", tag="text")
			self.canvas.itemconfig(text_canvas, text="Готово", fill="black", font='Helvetica 20 bold')
			self.root.update()

			time.sleep(1)

			self.quiz_progress_bar.place_forget()
			self.canvas.delete("text")
			self.canvas.delete("bg")

			# Loading next (mundo-monologue) scene
			# Sleep adds delay
			self.mundo = PhotoImage(file=self.pictures_path + "mundo.png")
			self.dialog = PhotoImage(file=self.pictures_path + "dialog.png")
			self.bcg = PhotoImage(file=self.pictures_path + "space_bcg.png")

			self.canvas.create_image((0, 0), anchor="nw", image=self.bcg, tag="bg")
			self.root.update()

			time.sleep(1) 

			self.canvas.create_image((1300, 200), anchor="nw", image=self.mundo, tag="mundo")
			self.root.update()

			mixer.music.load(r"audio\blop.mp3")
			mixer.music.play()
			
			time.sleep(1)  

			self.canvas.create_image((50, 200), anchor="nw", image=self.dialog, tag="dialogue")
			self.root.update()

			mixer.music.load(r"audio\blop.mp3")
			mixer.music.play()

			canvas_text = self.canvas.create_text((150, 300), anchor="nw", tag="text")

			def generate_audiotext(audio, test_string, wait=False, last=False):
				"""
				Inner function for delayed text creation. Suits very well with the
				voice of the character. 
				"""

				# Needed if several phrases are used
				if wait:
					time.sleep(wait)
				delta = 90
				delay = 0

				if audio:
					mixer.music.load(audio)
					mixer.music.play()

				for i in range(len(test_string) + 1):
					s = test_string[:i]
					update_text = lambda s = s: self.canvas.itemconfig(canvas_text, 
																	   text=s, 
																	   fill="white",
																	   font="Fixedsys 18 bold")
					self.canvas.after(delay, update_text)
					self.root.update()
					delay += delta

				time.sleep(7) 

				# If the generated was last, assign players to the Game-class object, 
				# Place proceed button of the Game-class object
				if last:
					self.game.players = self.players
					self.game.proceed_button.place(x=500, y=700)


			# Wrappers that help to use functons with threading 
			def wrapper():
				generate_audiotext(r"audio\dr_1.mp3", test_string)

			def wrapper_2():
				generate_audiotext(r"audio\dr_2.mp3", test_string_2, wait=10)

			def wrapper_3():
				generate_audiotext(r"audio\dr_3.mp3", test_string_3, wait=21)

			def wrapper_4():
				generate_audiotext(r"audio\dr_4.mp3", test_string_4, wait=39, last=True) # should wait
				
			time.sleep(1)

			test_string = "Здарова пачаны! Добро пожаловать в викторину Дона Симона,\n" + \
						  "я ее ведущий Доктор... эм.. а, на месте!"

			test_string_2 = "Правила игры очень простые: ответил правильно - заработал\n" + \
						  "очко. Ответил неправильно - потерял очко. Да. Пизда."

			test_string_3 = "В игре присутствуют элементы обыкновенной викторины,\n" + \
							"командной викторины, где все обьединяют силы, вопросы\n" + \
							"на скорость, плюс всякие фичы и интерактивы, которые\n" + \
							"вы увидите по ходу игры. Я хочу пиццу."

			test_string_4 = "Дальше короче разберетесь сами, желаю вам жид... \n" + \
							"эээм, замечательной игры!"

			# Try join at some point
			t1 = threading.Thread(target=wrapper)
			t2 = threading.Thread(target=wrapper_2)
			t3 = threading.Thread(target=wrapper_3)
			t4 = threading.Thread(target=wrapper_4)
			
			t1.start()
			t2.start()
			t3.start()
			t4.start()

	

