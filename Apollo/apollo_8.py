from turtle import Shape, Screen, Turtle, Vec2D as Vec

G = 8
NUM_LOOPS = 4100 
Ro_X = 0
Ro_Y = -85
Vo_X = 485
Vo_Y = 0

class GravSyst():

    def _init_(self):
        self.bodies = []
        self.t = 0
        self.dt = 0.001

    def sim_loop(self):
        for _ in range(NUM_LOOPS):
            self.t += self.dt
            for body in self.bodies:
                body.step()

class Planet(Turtle):
    #Celestial body(earth) that orbits and projects grav field
    def __init__(self, mass, start_loc, vel, gravsys, shape):
        super().__init__(shape=shape)
        self.gravsys = gravsys
        self.penup()
        self.mass = mass
        self.setpos(start_loc)
        self.vel = vel
        gravsys.bodies.append(self)
        #self.resizemode("user")
        #self.pendown() (Draws path behind object)
        #Defines class to create object for the earth, the moon and the Apollo 8
    def accel(self):
        #Calculates combine force and returns vector components
        a = Vec(0, 0)
        for body in self.gravsys.bodies:
            if body != self:
                r = body.pos() - self.pos()
                a += (G* body.mass / abs(r)**3) * r
        return a #returns acelleration because a is represented by a = Gm/r^2 (Uni Gravitation) (r is unit vector)
    def step(self):
        #Calculates Position, and velocity as well as orientation
        dt = self.gravsys.dt
        a = self.accel
        self.vel = self.vel + dt * a
        self.setpos(self.pos() + dt * self.vel)
        if self.gravsys.bodies.index(self) == 2: #second index is the spacecraft selects it
            rotate_factor = 0.0006
            self.setheading((self.heading - rotate_factor * self.xcor()))
            if self.xcor() < -20:
                self.shape('arrow')
                self.shape(0.5)
                self.setheading(105) #alligns, in degrees towards earth
    def main():
        screen = Screen()
        screen.setup(width=1.0, height=1.0) #Fullscreens 
        screen.bgcolor('black')
        screen.title("Apollo 8 Return Simulation")
        gravsys = GravSyst()
        #Sizes and scales both the earth and the moon
        image_earth = 'earth_100x100.gif'
        screen.register_shape(image_earth)
        earth = Planet(1000000, (0, -25), Vec(0, -2.5), gravsys, image_earth)

        image_moon = 'moon_27x27.gif'
        screen.register_shape(image_moon)
        moon = Planet(32000, (344, 42), Vec(-27, 147), gravsys, image_moon)

        csm = Shape('compound')
        cm = ((0, 30), (0, -30), (30, 0))
        csm.addcomponent(cm, 'white', 'white')
        sm = ((-60, 30), (0, 30), (0, -30), (-60, -30))
        csm.addcomponent(sm, 'white', 'black')
        nozzle = ((-55, 0), (-90, 20), (-90, -20))
        csm.addcomponent(nozzle, 'white', 'white')

        ship = Planet(1, (Ro_X, Ro_Y), Vec(Vo_X, Vo_Y), gravsys, 'csm')
        ship.shapesize(0.2)
        ship.color('white')
        ship.getscreen().tracer(1, 0)
        ship.setheading(90)

        gravsys.sim_loop()

    if __name__ == '__main__':
        main()




