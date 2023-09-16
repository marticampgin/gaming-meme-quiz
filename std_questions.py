from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
import time 
import threading
import random
import itertools

class StandardQuestions:
	def __init__(self, players, root, canvas, pictures_path, questions):
		self.root = root
		self.canvas = canvas
		self.pictures_path = pictures_path
		self.players = players
		self.all_questions = questions

		# Randomly rolling first section
		self.section = "Я ОДИН ЗДЕСЬ НАХУЙ" # random.choice(list(self.all_questions.keys()))
		self.questions = self.all_questions[self.section]
		del self.all_questions[self.section]

		self.button_width = 30
		self.button_height = 30

		self.wide_button_width = 210
		self.wide_button_height = 55

		self.button_container = []

		self.player_x = 350
		self.player_y = 630

		self.pl_name_x = 365
		self.pl_name_y = 615

		self.pl_moving_const_x = 150
		self.add_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "add_pts.png")
		self.next_q_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "next_qst.png")
		self.next_rnd_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "nxt_rnd.png")
		self.show_ans_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "show_ans.png")

		self.next_qst_button = Button(self.root,
									   width=self.wide_button_width,
									   height=self.wide_button_height,
									   image=self.next_q_img,
									   command=self.next_qst)

		self.show_ans_button = Button(self.root,
									   width=self.wide_button_width,
									   height=self.wide_button_height,
									   image=self.show_ans_img,
									   command=self.show_right_anwser)

		self.timer_flag = False

		self.current_right_answer = None
		self.current_right_tag = None

		self.introduce_section(self.section)

		time.sleep(1)

		self.initiate()

	def introduce_section(self, section):
			if section == "Это знать надо!":
				self.canvas.create_text((435, 300),
									anchor="nw",
									text=f"    Категория: {section}",
									fill="white",
									font="Fixedsys 46 bold",
									tag="sec.intro")
				
				self.root.update()

				self.canvas.create_text((345, 350),
										anchor="nw",
										text="Либо вы знаете ответ, либо идете нахуй.\n" + \
											"  В принципе, оба варианта неплохие.",
										fill="white",
										font="Fixedsys 40 bold",
										tag ="section.txt")


				self.root.update()
				time.sleep(5)

			elif section == "Я ОДИН ЗДЕСЬ НАХУЙ":
				self.canvas.create_text((450, 300),
									anchor="nw",
									text=f"Категория: {section}",
									fill="white",
									font="Fixedsys 46 bold",
									tag="sec.intro")

				self.root.update()

				self.canvas.create_text((230, 380),
										anchor="nw",
										text="Жду правильный вариант ответа, как хуй минета.",
										fill="white",
										font="Fixedsys 39 bold",
										tag ="section.txt")

				self.root.update()
				time.sleep(5)


			self.canvas.delete("sec.intro")
			self.root.update()

			time.sleep(0.5)
			self.canvas.delete("section.txt")
			self.root.update()

				

	def initiate(self):
		self.question_board = PhotoImage(file=self.pictures_path + "question_board.png")
		self.canvas.create_image((200, 80),
								  anchor="nw",
								  image=self.question_board,
								  tag="question_board")
		mixer.music.load(r"audio\blop.mp3")
		mixer.music.play()

		time.sleep(0.4)	

		self.show_characters()


	def show_characters(self):
		button_actions = [self.add_point_pl1, self.add_point_pl2, self.add_point_pl3, self.add_point_pl4,
						  self.add_point_pl5, self.add_point_pl6, self.add_point_pl7, self.add_point_pl8]


		for i, player in enumerate(self.players):
			self.canvas.create_image((self.player_x,
									  self.player_y),
									  anchor="nw",
									  image=player.character,
									  tag=player.name.get())

			self.canvas.create_text((self.pl_name_x, self.pl_name_y),
									text=player.name.get(),
									fill="white",
									font="Fixedsys 16 bold",
									tag=player.name.get() + "text",
									width="10c",
									justify="center")

			self.point_button = Button(self.root,
									   width=self.button_width,
									   height=self.button_height,
									   image=self.add_img,
									   command=button_actions[i],
									   bd=0)

			self.canvas.create_text((self.player_x + 5, self.player_y + 70),
									text=player.score,
									fill="white",
									font="Fixedsys 16 bold",
									tag=player.name.get() + "score")


			self.point_button.place(x=self.player_x + 70, y=self.player_y + 15)
			self.button_container.append(self.point_button)

			mixer.music.load(r"audio\appearance.mp3")
			mixer.music.play()
			self.root.update()
			self.player_x += self.pl_moving_const_x
			self.pl_name_x += self.pl_moving_const_x
			time.sleep(0.5)

		self.display_start_timer()
		self.next_qst_button.place(x=1300, y=840)
		self.show_ans_button.place(x=1000, y=840)
		self.next_qst_button["state"] = DISABLED
		self.show_ans_button["state"] = DISABLED
		self.init_random_question()

	def display_start_timer(self, sleep=False):
		if sleep:
			time.sleep(0.8)

		for i in range(3, 0, -1):
			self.canvas.create_text((950, 400),
									text=str(i),
									fill="white",
									font="Fixedsys 60 bold",
									tag="digit")
			self.root.update()
			mixer.music.load(r"audio\tick.mp3")
			mixer.music.play()
			time.sleep(1)
			self.canvas.delete("digit")

		self.canvas.create_text((950, 400),
									text="ВПЕРЕД АЛЕКС",
									fill="white",
									font="Fixedsys 60 bold",
									tag="alex")
		mixer.music.load(r"audio\\alex.mp3")
		mixer.music.play()
		self.root.update()							
		time.sleep(1)

		self.canvas.delete("alex")	


	def display_qst_timer(self):
		self.canvas.delete("digit")
		time.sleep(3)
		self.timer_flag = False
		for i in range(45, 0, -1):
			if self.timer_flag:
				return
			if i <= 5:
				self.canvas.create_text((950, 550),
									text=str(i),
									fill="red",
									font="Fixedsys 55 bold",
									tag="digit")
			else:
				self.canvas.create_text((950, 550),
										text=str(i),
										fill="white",
										font="Fixedsys 55 bold",
										tag="digit")

			time.sleep(1)
			self.canvas.delete("digit")

		self.canvas.create_text((950, 545),
								text="TIME'S UP",
								fill="RED",
								font="Fixedsys 35 bold",
								tag="digit")


	def next_qst(self):
		if self.section == "Я ОДИН ЗДЕСЬ НАХУЙ":
			tag = "ans"
			for i in range(4):
				self.canvas.delete(tag + str(i))

		elif self.section == "Это знать надо!":
			self.canvas.delete("ans")

		self.next_qst_button["state"] = DISABLED
		self.show_ans_button["state"] = DISABLED
		self.timer_flag = True
		self.canvas.delete("rnd_q")
		if len(list(self.questions.keys())) > 0:
			self.init_random_question()
		else:
			self.canvas.delete("digit")
			if len(list(self.all_questions.keys())) == 0:
				self.canvas.create_text((950, 300),
									text="Игра закончена!",
									fill="white",
									font="Fixedsys 50 bold",
									justify="center",
									tag="game_end",
									width="15c")

				for btn in self.button_container:
					btn.place_forget()
					
				self.choose_winner()
			else:
				self.canvas.create_text((950, 300),
										text="Раунд закончен!",
										fill="white",
										font="Fixedsys 50 bold",
										justify="center",
										tag="rnd_end")

				self.next_rnd_button = Button(self.root,
											width=self.wide_button_width,
											height=self.wide_button_height,
											image=self.next_rnd_img,
											command=self.next_rnd)

				self.next_rnd_button.place(x=845, y=500)


	def next_rnd(self):
		self.canvas.delete("rnd_end")
		self.root.update()
		self.next_rnd_button.place_forget()
		self.root.update()
		# Rolling next section
		self.section = random.choice(list(self.all_questions.keys()))
		self.questions = self.all_questions[self.section]
		del self.all_questions[self.section]
		
		self.next_qst_button["state"] = DISABLED
		self.show_ans_button["state"] = DISABLED		

		self.introduce_section(self.section)
		self.display_start_timer(sleep=True)
		self.init_random_question()


	def show_right_anwser(self):
		if self.section == "Я ОДИН ЗДЕСЬ НАХУЙ":
			self.canvas.itemconfigure(self.current_right_tag, fill="green")
		elif self.section == "Это знать надо!":
			self.canvas.create_text((950, 450),
									text=self.current_right_answer,
									fill="green",
									font="Fixedsys 30 bold",
									tag="ans",
									width="15c",
									justify="center")
		self.timer_flag = True


	def enable_button(self):
		time.sleep(3)
		self.next_qst_button["state"] = ACTIVE
		self.show_ans_button["state"] = ACTIVE


	def init_random_question(self):
		rnd_q = random.choice(list(self.questions.keys()))
		rnd_ans = self.questions.pop(rnd_q)

		if self.section == "Я ОДИН ЗДЕСЬ НАХУЙ":
			self.current_right_answer = rnd_ans[1]
			# DISPLAY THEM, REMEMBER TO HIGHLIGHT THE RIGHT ANSWER 
			init_x = 500
			init_y = 420
			detected_big_option = False
			options = []
			for i, option in enumerate(rnd_ans[0]):

				if option == self.current_right_answer:
					self.current_right_tag = "ans" + str(i)


				if len(option) > 13:
					detected_big_option = True

				options.append(option)

			for i, option in enumerate(options):

				if detected_big_option:
					self.canvas.create_text((init_x, init_y),
										text=str(i + 1) + ". " + option,
										fill="white",
										font="Fixedsys 18 bold",
										tag="ans" + str(i),
										justify="center",
										width="13c")

				else:
					self.canvas.create_text((init_x, init_y),
											text=str(i + 1) + ". " + option,
											fill="white",
											font="Fixedsys 30 bold",
											tag="ans" + str(i),
											justify="center",
											width="13c")

				if i == 1:
					init_x -= 850
					init_y += 90
				else:
					init_x += 850
				
			
		
		elif self.section == "Это знать надо!":
			self.current_right_answer = rnd_ans


		rnd_q = rnd_q.split()
		
		if len(rnd_q) > 80:
			self.canvas.create_text((935, 270),
								text=rnd_q,
								fill="white",
								font="Fixedsys 20 bold",
								tag="rnd_q",
								anchor="center",
								justify="center",
								width="20c")
		else: 

			self.canvas.create_text((935, 270),
									text=rnd_q,
									fill="white",
									font="Fixedsys 27 bold",
									tag="rnd_q",
									anchor="center",
									justify="center",
									width="20c")

		timer_thread = threading.Thread(target=self.display_qst_timer)
		timer_thread.start()

		button_thread = threading.Thread(target=self.enable_button)
		button_thread.start()


	def choose_winner(self):
		winners = []
		scores = []
		for player in self.players:
			scores.append(player.score)
		
		max_value = max(scores)
		max_index = scores.index(max_value)

		winner = self.players.pop(max_index)

		winners.append(winner)
		# Checking the rest
		for player in self.players:
			if player.score == max_value:
				winners.append(player)

		init_x = 980
		init_y = 470

		init_name_x = 985	
		init_name_y = 460

		self.canvas.create_text((750, 500),
									text="Победители:",
									fill="white",
									font="Fixedsys 40 bold",
									justify="center",
									tag="winners",
									width="15c")

		for player in winners:
			self.canvas.create_image((init_x,
									  init_y),
									  anchor="nw",
									  image=player.character,
									  tag=player.name.get())

			self.canvas.create_text((init_name_x, init_name_y),
									text=player.name.get(),
									fill="white",
									font="Fixedsys 16 bold",
									tag=player.name.get() + "text",
									width="10c",
									justify="center")
			
			init_x += self.pl_moving_const_x
			init_name_x += self.pl_moving_const_x

		mixer.music.load(r"audio\\esketit.mp3")
		mixer.music.play()

		
	def add_point_pl1(self):
		self.players[0].add_points(10)
		self.canvas.itemconfigure(self.players[0].name.get() + "score", text=self.players[0].score)

	def add_point_pl2(self):
		self.players[1].add_points(10)
		self.canvas.itemconfigure(self.players[1].name.get() + "score", text=self.players[1].score)

	def add_point_pl3(self):
		self.players[2].add_points(10)
		self.canvas.itemconfigure(self.players[2].name.get() + "score", text=self.players[2].score)
	def add_point_pl4(self):

		self.players[3].add_points(10)
		self.canvas.itemconfigure(self.players[3].name.get() + "score", text=self.players[3].score)

	def add_point_pl5(self):
		self.players[4].add_points(10)
		self.canvas.itemconfigure(self.players[4].name.get() + "score", text=self.players[4].score)

	def add_point_pl6(self):
		self.players[5].add_points(10)
		self.canvas.itemconfigure(self.players[5].name.get() + "score", text=self.players[5].score)

	def add_point_pl7(self):
		self.players[6].add_points(10)
		self.canvas.itemconfigure(self.players[6].name.get() + "score", text=self.players[6].score)

	def add_point_pl8(self):
		self.players[7].add_points(10)
		self.canvas.itemconfigure(self.players[7].name.get() + "score", text=self.players[7].score)




		