from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pygame import mixer
from tkVideoPlayer import TkinterVideo
from std_questions import StandardQuestions

import time 
import threading
import random


class Game:
	def __init__(self, root, canvas, pictures_path):

		# Parameters
		self.root = root
		self.canvas = canvas
		self.pictures_path = pictures_path

		self.players = None
		
		self.button_width = 210
		self.button_height = 55

		self.player_x = 310
		self.player_y = 210

		self.pl_name_x = 325
		self.pl_name_y = 192

		self.moving_constant_x = 160
		self.moving_constant_y = 150


		self.init_img = PhotoImage(file=self.pictures_path + "buttons" + "\\" + "init.png")


		# Contains all the questions in the whole quiz
		self.questions =	{"Это знать надо!": 
											 {"Персонаж Bowser является главным антагонистом какой игры?": "Mario",

						   					  "Какая компания выпустилу культовую игру Donkey Kong?": "Nintendo",

						   					  "Какой разработчик создал Starcraft?": "Blizzard",

						   					  "Никнейм Маркуса Перссона, разработчика Minecraft?": "Notch",

						   					  "Кому продал права на Minecraft Маркус Перссон в 2014 году?": "Microsoft",

						   					  "Какие предметы должен фармить Соник, чтобы выживать?": "Золотые кольца",

					   					      "Полное название замечательной игры, в которую мы много играли у Серёги на квартире?": "Crash Team Racing",

					   					      "Как расшифровывается SNES (игровая консоль, выпущенная Nintendo)?": "Super Nintendo Entertainment System",

					   					      "До появления расы Амфибий, какие расы были в игре Perfect World?": "Люди, Сиды, Зооморфы",

					   					      "Как называется главный лечащий предмет в Dark Souls?": "Фляга с Эстусом",

					   					      "Как называется главный лечащий предмет в Elden Ring?": "Фляга багровых слёз",

					   					      "Как называется главный лечащий предмет в Demon Souls?": "Трава полулуния/Трава полнолуния",

					   					      "Как называется главный лечащий предмет в Sekiro?": "Фляга с лекарством",
					   					   
					   					      "Как называется главный лечащий предмет в Bloodborne?": "Пузырек крови",

											  "В какой игре происходят события на вымышленном материке под названием Тамриэль?": "The Elder Scrolls V: Skyrim",
											  
											  "Как зовут зелёного динозавра, приятеля Марио и Луиджи в франшизе Марио?" : "Yoshi",
											  
											  "Какая консоль, выпущенная в 2006 году впервые интегрировала motion control?": "Nintendo Wii",

											  "Какой Playstation платформер был выпущен в 1996 году, название которое идентично с именем главного персонажа?": "Crash Bandicoot",
											  
											  "Как называется open-world игра, где главный персонаж с помощью луком сражается с гигантскими звероподобными роботами?": "Horizon Zero Dawn",
											  
											  "Какая игра, выпущенная в 1996 году, положила начало кино- и игровой франшизе, а так сделала жанр хоррор мейнстримным?": "Resident Evil",
											  
											  "Что за игровой движок пренадлежит Epic Games, компанию выпуствишую Fortnite?": "Unreal Engine",
											  
											  "В 2008 году, игра _______ Paradise положила начало гоночным играм с открытым миром": "Burnout",
											  
											  "В какой игре можно дрифтить под фонк, воровать у друзей, а так же получить пизды на кладбище?": "Pummel Party",
											  
											  "Desmond Miles является протагонистом в первых нескольких частях какой серии игр?": "Assassin's Creed",
											  
											  "В какой игре главным антагонистом является Vaas Montenegro?": "Far Cry 3",
											  
											  "Самая продаваемая в мире игровая консоль - это: ": "Playstation 2",
											  
											  "AMD или Intel?": "Obama",
											  
											  "Кого пытается спасти Mario?": "Princess Peach",
											  
											  "Как зовут популярное фиолетовое существо, являвшигося своебразным символом Playstation?": "Spyro The Dragon",
											  
											  "Какая консоль вышла первой: N64, Sega Saturn, PlayStation?" : "Sega Saturn",
											  
											  "По какой популярной файтинг игре 90-х со временем сняли фильм?": "Mortal Kombat",
											  
											  "Какого игрового персонажа женского пола со временем сыграла Анджелина Джоли?": "Lara Croft",
											  
											  "Какой персонаж из Мортал Комбата умеет контроллировать молнию?": "Raiden",
											  
											  "Какая была последняя консоль выпущенная SEGA?": "Sega Dreamcast",
											  
											  "Какая игра вышла раньше: Street Fighter или Tekken?": "Street Fighter",
											  
											  "Какая популярная игра N64 с медведем и красной птицой была выпущена в 1998?":" Banjo-Kazooie",
											  
											  "Последний босс в Sekiro - это?": "Иссин, Мастер меча",
											  
											  "Последний босс в Dark Souls 3 - это?": "Душа пепла",
											  
											  "Последний босс в террарии - это?": "Moonlord",
											  
											  "Имя и фамилия протагониста Half-life": "Gordon Freeman",
											  
											  "Когда вышел Minecraft?": "2011",
											  
											  "Какой предмет нужен в Minecraft, чтобы сделать все зелья? ": "Бутылка с водой",
											  
											  "Кто боится оцелотов (котов из джунглей) в Minecraft?": "Creeper",
											  
											  "Имя человека, который написал серию Metal Gear": "Hideo Kojima",
											  
											  "Какой Бог противостоит Кратосу в конце God of War (2018)?": "Thor",
											  
											  "Как называется магазин оружия в GTA San Andreas?": "Ammu-nation",
											  
											  "Полное имя CJ из GTA San Andreas": "Carl Johnson",

											  "Каких двух главных персонажей (имена) в конце игры предстоит убить CJ в Gta San Andreas?": "Big Smoke & Officer Tenpenny"
											  
											  },

											  

											   


					   	  "Я ОДИН ЗДЕСЬ НАХУЙ": 
					   	  					 {"Какой разработчик игр в 2006 году выпустил игру Bully?": [["Bandai Namco", "Capcom", "Rockstar", "Warner Bros"], "Rockstar"],

					   	  					  "Имена каких персонажей в LOL явлются псевдонимами основателей этой игры?": [["Garen & Darius", 
																										   					   "Jax & Taric", 
																									   					   	   "Ryze & Tryndamere", 
																									   					       "Twisted Fate & Kayle"], 
																									   					       "Ryze & Tryndamere"],

					   					      "Какого персонажа в LOL ненавидит игрок SUPER CRAB?": [["Vayne", "Riven", "Quinn", "Zoe"], "Vayne"],

					   					      "В какой исторический периуд происходят действия первой части Call of Duty?": [["WW1", "WW2", "Modern", "Future"], "WW2"],

					   					      "Какой уровень был максимальным в игре World of Warcraft до появления дополнений?": [["50", "60", "70", "80"], "60"],

					   					      "Какой была последняя (и самая легендарная) версия Minecraft, перед введением механик голода и спринта?": [["1.7.2", "1.7.3", "1.7.4", "1.8"], "1.7.3"],

					   					      "В какой версии Minecraft был добавлен Дракон Края?": [["1.9", "1.10", "1.0", "1.19"], "1.0"],

					   					      "В каком году была выпущена первая часть игр серии GTA?": [["1997", "1998", "1999", "2000"], "1997"],

					   					      "Самая продаваемая игра в мире - это:": [["PUBG", "Tetris", "GTA V", "Minecraft"], "Minecraft"],

											  "Имя главного протагониста игры The Legend of Zelda?" : [["Rayman", "Strife", "Link", "Asura"], "Link"],
											# "" : [["", "", "", "" ], ""]
											  "Какое любимое животное у Дум Гая?": [["Кролик", "Шиншила", "Заяц", "Белка"], "Кролик"],

											  "Какой рост у Дум Гая?" : [["169", "184", "175", "215" ], "215"],

											  "За что Дум Гая послали на Марс, когда он был человеком?" : [["За заслуги на службе", 
											  																"За собственые связи", 
																											"За вступления в ряды марсиан", 
																											"За нарушение в приказе" ], "За нарушение в приказе"],

											  "Почему Дум Гай убивает демонов?" : [["чтобы защитить землю", 
											  										"Из-за ненависти к ним", 
																					"Из-за справедливости", 
																					"Чтобы закрыть врата и невпускать демонов в мир" ], "Из-за ненависти"],

											  "Настоящие имя Дум Гая, это: " : [["Flynn", "Abraham", "Jackson", "Sam" ], "Flynn"],

											  "Какое обозначение название оружие 'bfg9000'?" : [["Brave from gods", 
											  													 "Big fear gun", 
																								 "Big fucking gun", 
																								 "Boom for grow" ], "Big fucking gun"],

											  "Куда попал Дум Гай, после первого пребывания тысячи лет в аду?" : [["Рай", 
											  																	   "Аргент д'нур", 
																												   "Обратно на марс", 
																												   "Парящем острове над землёй" ], "Аргент д'нур"],
											  "Что чувствуют демоны при виде палача рока?" : [["Страх", "Ненависть", "Ярость", "Паника" ], "Страх"],

											  "Аргент энергия -  это" : [["Новое электричество на Марсе", 
											  							  "Энергетик на станции Марса", 
																		  "Новая энергия по обогащению Марса кислородом", 
																		  "Энергия созданая из душ" ], "Энергия созданая из душ"],

											  "Почему заточили палача рока в саркофаг в первый раз" : [["Из-за того что демоны не знали как его побороть", 
											  															"По ошибке", 
																										"Из-за предательства Аргент д'нура", 
																										"Из-за Сэмуэля Хайдена" ], "Из-за того что демоны не знали как его побороть"],

											  
											  "Первая игра в серии Total war - это" : [["Rome: Total War", "Empire: Total War", "Ничего из перечисленного", "Shogun: Total War" ], "Shogun: Total War"],

											  "Разработчик игры Total war - это" : [["SEGA", 
											  										"Electronic Arts", 
																					"The Creative Assembly", 
																					"Activision" ], "The Creative Assembly"],

											  " Какой временной промежуток затрагивает игра Rome: Total War?" : [["1 век н.э. - 21 век н.э.", 
											  																	  "470 г. до н.э. - 75 г. до н.э.", 
																												  "1914 г. н.э. - 1945 г. н.э.", 
																												  "270 г. до н.э. - 14 г. н.э" ], 
																												  "270 г. до н.э. - 14 г. н.э."],
											  "Столица Российской империи в игре Empire: Total War?" : [["Москва", "Санкт-Петербург", "Ленинград", "Динабург" ], "Москва"],

											  "Какая из частей серии Total war является самой продаваемой?" : [["Total War: Shogun 2", 
																												"Rome: Total War", 
																												"Total War: Warhammer II", 
																												"Total War: Rome 2" ], " Total War: Warhammer II"],

											  "Сколько DLC имеет игра серии Total War: Rome 2?" : [["2", "6", "0", "33" ], "6"],

											  "Гунны являются сильным и грозным соперником в игре Total War: Attila. Если начать игру за их фракцию, какая базовая сложность будет при старте сессии?" : [["Низкая", 
											  																																								"Средняя", 
																																																			"Высокая", 
																																																			"Максимальная" ], "Высокая"],
											  "Total War: Shogun 2 охватывает период феодальной Японии 16 века. Сколько кланов (фракций) участвуют в борьбе за власть?" : [["3", 
											  																																 "4", 
																																											 "5", 
																																											 "9" ], "9"],
											  "В серии Total War присутствуют игры, использующие сеттинг настольной игры. Название сеттинга?" : [["Warhammer 40,000", 
																																				  "Spartan", 
																																				  "Warhammer Fantasy", 
																																				  "Ничего из перечисленного" ], "Warhammer Fantasy "],
											  "Как минимум одна игра из серии Total War распространялась по модели free-to-play. Название игры?" : [["Total War Battles: Kingdom", 
											  																										   "Total War: Attila", 
																																					   "Total War Saga: Troy", 
																																					   "Total War: Arena" ], "Total War: Arena"],

												"Какой вид левиафанов является самым большим и мало известным на планете 4546B в Subnautica?" : [["Левиафан Анктониус", 
																																				  "Морской Император", 
																																				  "Левиафан Гаргантюа", 
																																				  "Пустотный оптический левиафан"], "Пустотный оптический левиафан"],
												"Какой способностью обладает биомеханическая форма жизни по имени страж в Subnautica?" : [["Силовое поле", "Пси-излучение", "Телепорт", "Электрический шок" ], "Телепорт"],
												
												"Как называются два вида подводных транспортных средства, которые мы можем использовать в Subnautica?" : [["ROM12A, VEH-A", 
																																						   "Спринтер, Аврора", 
																																						   "Geo-Max, Sparkle", 
																																						   "Мотылёк, Циклоп"], "Мотылёк, Циклоп"],

												"На какую реальную болезнь похоже Хараа охватившая целую планету в Subnautica?" : [["Крапивница", "Грипп", "Сифилис", "Туберкулез"], "Грипп"],

												"С каким левиафаном (в возрасте ребенка) можно подружиться исключительно в Return of the Ancients в Subnautica?" : [["Морской император", "Призрачный левиафан", 
																																									 "Левиафан Рипер", "Левиафан Гаргантюа"], "Левиафан Гаргантюа"],
																																									 
												"В какой момент главный герой попадает под влияние вируса Хараа в Subnautica?" : [["Во время инъекции на базе инопланетян", 
																																   "После укуса зараженных крабо-подобных существ", 
																																   "После укуса сталкера (рыба охотник)", 
																																   "После погружения в воду"], "После погружения в воду"],

												"Что будет если уплыть за предел мертвой зоны в Subnautica?" : [["Вас убьет призрачный Левиафан", 
																												 "Вы умрете от вируса Хараа", 
																												 "Вы попадете на остров", 
																												 "Вас вернет в спасательную шлюпку"], "Вас убьет призрачный Левиафан"],

												"Самое сильное оружие, которое вы можете создать в Subnautica?" : [["Стазис винтовка", 
																													"Пропульсионная пушка", 
																													"Шокерный-гарпун", 
																													"Термоклинок"], "Термоклинок"],

												"Что первое видит главный герой, когда поднимается на верх спасательной шлюпки в Subnautica?" : [["Летучий скат", 
																																				  "Попугай", 
																																				  "Чайка", 
																																				  "Одноглазый-летун"], "Летучий скат"],

												"Кто такие Баккаи в LOL?" : [["Палачи Ноксуса", 
																			 "Те, кто пережил неудачный ритуал Вознесения", 
																			 "Демасийская гвардия элитных солдат", 
																			 "Легендарные войны освобождения " ], "Те, кто пережил неудачный ритуал Вознесения"],
												"Назовите правильный вариант с названиями умений Зеда" : [["Презрение к слабости/теневой клон/смертельное лезвие/бросок сюрикена",
													   													   "Теневой разрез/клеймо смерти/живая тень/бросок сюрекена", 
																										   "Сюрикен/рассечение/теневой клон/смертельная подготовка", 
																										   "Ближний бой/тень/решимость судьбы/сюрикен" ], "Теневой разрез/клеймо смерти/живая тень/бросок сюрекена"],

												
												"Кем был Ургот до предательтва?" : [["Коммандиром элитного отряда Ноксуса",
																					"Даником Гутовским", 
																					"Верховным палачом Ноксуса", 
																					"Правой рукой Сиона" ], " Верховным палачом Ноксуса"],

												"У кого из этих чемпионов нету легендарного образа?" : [["Фиддлстикс",
																										"Зед", 
																										"Триндамир", 
																										"Вуконг" ], "Вуконг"],
												
												"Какой предмет в League of Legends можно найти в магазине по альтернативному запросу «tons of damage»?" : [["«Самый Лучший Меч»",
																																							"«Грань Бесконечности»", 
																																							"«Тройственный союз»", 
																																							"«Кровопийца»" ], "«Тройственный союз»"],

												"Именно этот кровожадный полководец, ранее носивший имя Сахн-Азал, воздвиг бастион, который стал основой Ноксуса" : [["Дариус",
																																									  "Мордекайзер", 
																																									  "Свейн", 
																																									  "Клед"], "Мордекайзер"],

												"Кто оставил шрам на лице Катарины, попытавшись её убить?" : [["Ноктюрн",
																												"Гарен", 
																												"Зед", 
																												"Талон" ], "Талон"],

												"Сколько скинов имеет чемпион Люкс?" : [["15",
																						"20", 
																						"18", 
																						"21" ], "18"],

												"Как называется ульта (R) Ёне?" : [["Решение судьбы",
																					"Последний вздох", 
																					"Путь охотника", 
																					"Рассечение духа" ], "Решение судьбы"],

												"Назовите прозвище Фиддлстикса" : [["Кошмар во плоти",
																					"Страховин", 
																					"Древний ужас", 
																					"Тотем страха" ], "Древний ужас"],


												"Какая профессия у Геральта из Ривии?" : [["бард", 
																							"ведьмак", 
																							"алхимик", 
																							"крупье" ], "ведьмак"],

												"К какой школе ведьмаков принадлежал Геральт?" : [["Школа Волка", 
																									"Школа Кошки", 
																									"Школа Грифона", 
																									"Школа для Даунов" ], "Школа Волка"],

												"Как называются мистические существа во вселенной Ведьмака?" : [["эльфы", 
																												"гномы", 
																												"вампиры", 
																												"ведьмаки" ], "вампиры"],

												"На каком основном языке говорят в Северных королевствах?" : [["Древняя речь", 
																												"Всеобщая речь", 
																												"Нильфгаардская", 
																												"Гномья" ], "Всеобщая речь"],

												"Кто приемная дочь Геральта и могущественная волшебница?" : [["Цири", 
																											"Йеннифэр", 
																											"Трисс", 
																											"Мама" ], "Цири"],

												"На каком континенте находится вселенная Ведьмака?" : [["Тамриэль", 
																										"Азерот", 
																										"Вестерос", 
																										"Континент" ], "Континент"],


												"Как называется карточная игра, широко распространенная во вселенной Ведьмака?" : [["Гвинт", 
																																	"Лаки 7", 
																																	"Блэк Джек", 
																																	"Хартстоун" ], "Гвинт"],


												"Кто такой император Нильфгаарда, могущественной южной империи?" : [["Эмгыр вар Эмрейс", 
																													"Радовид V", 
																													"Король Фольтест", 
																													"Кариньш" ], "Эмгыр вар Эмрейс"],


												"Как зовут волшебницу, воспитавшую Цири и являющуюся любовным увлечением Геральта?" : [["Йеннифэр", 
																																		"Трисс", 
																																		"Фрингилья", 
																																		"Божена" ], "Йеннифэр"],


												" Что за существо такое Леший в Ведьмаке?" : [["Элементаль", 
																								"Вампир", 
																								"Оборотень", 
																								"Лесной дух" ], "Лесной дух"],

												"В каком году вышел ремастер Diablo 2?" : [["2021", 
																							"2020", 
																							"2023", 
																							"Ещё не вышел" ], "2021"],

												"Кто главный антагонист Diablo 4?" : [["Мефисто", 
																						"Диабло", 
																						"Лилит", 
																						"Инарий" ], "Лилит"],

												"Какая была проблема в первое время после запуска Diablo 4?" : [["Не было проблем", 
																												"Огромные очереди на вход в игру", 
																												"Невозможность создания одного из классов персонажей", 
																												"Частые вылеты игры" ], "Огромные очереди на вход в игру"],

												"Сколько актов в сюжетной линии Diablo 4? (Без учёта пролога и эпилога)" : [["4 акта", 
													   "5 актов", 
													   "6 актов", 
													   "7 актов" ], "6 актов"],

												"Сколько актов в сюжетной линии Diablo 3?" : [["7 актов", 
													   "4 акта", 
													   "5 актов", 
													   "6 актов" ], "4 акта"],

												"Кто создал Санктуарий (мир серии игр Diablo)?" : [["Бог", 
													   "Люцифер", 
													   "Инарий и Лилит", 
													   "Диабло, Мефисто и Баал" ], "Инарий и Лилит"],


												"Настоящее имя Диабло?" : [["Аль-Диабалос, Повелитель Ужаса", 
																			"Эль-Диабол, Повелитель Страха", 
																			"Диаболос, Повелитель Кошмаров", 
																			"Эль-Дебил" ], "Аль-Диабалос, Повелитель Ужаса"],

												"Кем является Лилит для Мефисто?" : [["Служанка", 
																						"Дочь", 
																						"Жена", 
																						"Мать" ], "Дочь"],

												"Что такое Изначальное Зло в серии игр Diablo?" : [["Трое самых могущественных демонов", 
																									"Сатана", 
																									"Ангелы и Демоны", 
																									"Люди" ], "Трое самых могущественных демонов"],

												"Что такое Меньшее Зло (Младшее Воплощение Зла) в Diablo?" : [["Ведьмы", 
																												"Признаки", 
																												"Сильные демоны, но слабее, чем Изначальное Зло*", 
																												"Слабые демоны, которые сотрудничают с людьми" ], "Сильные демоны, но слабее, чем Изначальное Зло*"],

												#"" : [["", 
												#	   "", 
												#	   "", 
												#	   "" ], ""],




											  
					   	  					  }


					   		}


		# Buttons
		self.proceed_button = Button(self.root,
									 width=self.button_width,
									 height=self.button_height,
									 image=self.init_img,
									 command=self.proceed_to_quiz,
									 bd=0)
	def proceed_to_quiz(self):
		"""
		Hides widgets, shows the players (their characters/names)
		"""
		mixer.music.load(r"audio\\click.mp3")
		mixer.music.play()

		self.canvas.delete("dialogue")
		self.canvas.delete("mundo")
		self.canvas.delete("text")
		self.proceed_button.place_forget()

		self.root.update()

		time.sleep(1)
		self.show_rest()

	
	def show_rest(self):
		# ---------- Displaying players ----------
		pl_entries = []
		for player in self.players:
			self.canvas.create_image((self.player_x,
									  self.player_y),
									  anchor="nw",
									  image=player.character,
									  tag=player.name.get())

			self.canvas.create_text((self.pl_name_x, self.pl_name_y),
									text=player.name.get(),
									fill="white",
									font="Fixedsys 16 bold",
									tag=player.name.get() + "text")


			mixer.music.load(r"audio\appearance.mp3")
			mixer.music.play()
			self.root.update()
			self.player_x += self.moving_constant_x
			self.pl_name_x += self.moving_constant_x
			time.sleep(0.5)

		def generate_audiotext(audio, test_string, wait=False):
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
																   font="Fixedsys 17 bold")
				self.canvas.after(delay, update_text)
				self.root.update()
				delay += delta


		def wrapper():
			time.sleep(12) 
			for player in self.players:
				self.canvas.delete(player.name.get())
				self.canvas.delete(player.name.get() + "text")

				time.sleep(0.2)

			self.canvas.delete("mundo")

			time.sleep(0.2)

			self.canvas.delete("dialogue")
			self.canvas.delete("text")

			time.sleep(1)
			
			StandardQuestions(self.players, 
							  self.root, 
							  self.canvas, 
							  self.pictures_path,
							  self.questions)

		# ---------- Displaying rest ----------

		self.mundo = PhotoImage(file=self.pictures_path + "mundo_mid.png")
		self.dialog = PhotoImage(file=self.pictures_path + "dialog_mid.png")

		self.canvas.create_image((1200, 400), anchor="nw", image=self.mundo, tag="mundo")
		self.root.update()
		mixer.music.load(r"audio\blop.mp3")
		mixer.music.play()

		time.sleep(0.5)

		self.canvas.create_image((250, 400), anchor="nw", image=self.dialog, tag="dialogue")
		self.root.update()
		mixer.music.load(r"audio\blop.mp3")
		mixer.music.play()

		canvas_text = self.canvas.create_text((290, 450), anchor="nw", tag="text")

		
		txt = "Ну нихуя себе сейчас заруба будет! Помните\n" + \
			  "пачаны - главное, чтобы с Боженкой все\n" + \
			  "хорошо было! А так похуй нахуй. Было\n" + \
			  "и было."

		t1 = threading.Thread(target=wrapper)

		generate_audiotext(r"audio\dr_5.mp3", txt, wait=1)
		t1.start()


		




		