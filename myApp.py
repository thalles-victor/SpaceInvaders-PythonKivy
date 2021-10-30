from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.widget import Widget
import random as rd

class Manager(ScreenManager):
	pass
class Game(Screen):
	fps=1/60
	up= BooleanProperty(False)
	down= BooleanProperty(False)
	isShoot= BooleanProperty(False)
	flag_height=0
	flag_shoot=0
	listShoot=[]
	listComet=[]
	time_addComet=0
	def on_pre_enter(self, *args):
		Clock.schedule_interval(self.tick, self.fps)
	def tick(self, *args):
		self.playerUp()
		self.playerDown()
			
		
		self.flag_shoot=0
		self.shoot()
		self.animationShoot()
		
	
		self.time_addComet+=1
		if self.time_addComet>=(1/self.fps)*1/2:
			self.time_addComet=0
			self.add_Comet()
		self.anim_Comet()
		self.ColisionComet_With_Player()
		self.ColisionBullet_With_Comet()
	def ColisionBullet_With_Comet(self, *args):
		for comet in self.listComet:
			for shoot in self.listShoot:
				
				if Colision().checkColider(comet, shoot):
					try:
						self.removeObj(comet, self.listComet)
						self.removeObj(shoot, self.listShoot)
					except:
						continue
				

	def removeObj(self, obj, lista):
		self.remove_widget(obj)
		lista.remove(obj)
	def ColisionComet_With_Player(self, *args):
		for comet in self.listComet:
			if Colision().checkColider(comet, self.ids.player):
				myApp().stop()
			
	def anim_Comet(self, *args):
		for comet in self.listComet:
			comet.x-=5
			if comet.x<=-comet.width:
				self.remove_widget(comet)
	def add_Comet(self, *args):
		comet= Comet(pos=(self.width, rd.randrange(0, self.height)))
		self.add_widget(comet)
		self.listComet.append(comet)
		
	def animationShoot(self, *args):
		for shoot in self.listShoot:
			shoot.x+=10
			if shoot.x>self.width:
				self.removeObj(shoot, self.listShoot)
	def playerUp(self):
		if self.up and self.ids.player.y+self.ids.player.height <=self.height:
			self.ids.player.y+=15
	def playerDown(self):
		if self.down and self.ids.player.y >= 0:
			self.ids.player.y-=15
			
	def shoot(self, *args):
		if self.isShoot and len(self.listShoot)<=25:
			shoot=Bullet(y=self.ids.player.height/2+self.ids.player.y, x=self.ids.player.width+self.ids.player.x, size=(10, 5))
			self.add_widget(shoot)
			self.listShoot.append(shoot)
			
class Colision:
	def checkColider(self, obj1, obj2):
		return self.colider(obj1, obj2)
		
	def colider(self, obj1, obj2):
		if obj1.x + obj1.width > obj2.x and	 obj1.x<obj2.x and obj1.y + obj1.height >obj2.y and obj1.y <obj2.y:
			return True
		return False
			
class Menu(Screen):
	pass
class GameOver(Screen):
	pass
class Comet(Widget):
	life = NumericProperty(10)
class Bullet(Image):
	pass	
class Player(Image):
	pass
class Conf(Screen):
	pass
class myApp(App):
	def build(self):
		return Manager()
		
myApp().run()