from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

#To create Paddles and there movement
#Note: Paddles are considered as players
class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.2

#For the movement of ball
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Latest position = Current velocity + Current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

#Main class to create the game
class PongGame(Widget):
    #Initializing ball and player to object
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    #Moving the ball in random direction
    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    #Function to update and display the events
    def update(self,dt):
        self.ball.move()

        # bounce of top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1
        # bounce of left and increase the score
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score += 1
        # bounce of right and increase the score
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.player2.score += 1
        #calling the bounce ball for the ball to hit and bounce of the paddle 
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
    # Creating movement by touch or mouse click    
    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y

#To display the game on the window
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        #Setting the interval or FPS
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

#main to run the PongApp class
if __name__=="__main__":
    PongApp().run()
