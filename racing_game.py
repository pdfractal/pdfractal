import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Simple cube vertices and edges to represent the car/obstacles
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,7), (7,6), (6,4),
    (0,4), (1,5), (2,7), (3,6)
)

def draw_cube(color=(1,0,0)):
    glBegin(GL_LINES)
    glColor3fv(color)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

class Obstacle:
    def __init__(self, z):
        self.x = 0
        self.y = 0
        self.z = z
        self.speed = 0.5
    def update(self):
        self.z += self.speed
        if self.z > 1:
            self.z = -50
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        draw_cube((0,1,0))
        glPopMatrix()

class Car:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.z = 0
    def move(self, dx):
        self.x += dx
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        draw_cube((1,0,0))
        glPopMatrix()

def draw_road():
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)
    glVertex3f(-5, -1.5, -50)
    glVertex3f(5, -1.5, -50)
    glVertex3f(5, -1.5, 1)
    glVertex3f(-5, -1.5, 1)
    glEnd()

    # center line
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(1, 1, 0)
    for z in range(-50, 1, 5):
        glVertex3f(0, -1.49, z)
        glVertex3f(0, -1.49, z+2)
    glEnd()

def init_gl(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    init_gl(*display)

    car = Car()
    obstacles = [Obstacle(z) for z in range(-10, -50, -10)]

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            car.move(-0.1)
        if keys[K_RIGHT]:
            car.move(0.1)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,0,2, 0,0,-10, 0,1,0)

        draw_road()
        car.draw()
        for ob in obstacles:
            ob.update()
            ob.draw()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
