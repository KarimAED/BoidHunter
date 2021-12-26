import numpy as np


class Actor:

    def __init__(self, pos, vel, frame, label,
                 pref_dist=20, vision_range=50,
                 size=5, color="red", max_v=20, frame_size=np.array([1000, 800]), show=False):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.pref_dist = pref_dist
        self.vision_range = vision_range
        self.neighbours = []
        self.frame = frame
        self.label = label
        self.size = size
        self.color = color
        self.max_v = max_v
        self.frame_size = frame_size
        self.dead = False
        self.show = show

    def move(self):
        self.pos += self.vel

        for i in range(len(self.pos)):
            if self.pos[i] < 0:
                self.pos[i] += self.frame_size[i]
            elif self.pos[i] > self.frame_size[i]:
                self.pos[i] -= self.frame_size[i]

    def draw(self):
        self.frame.create_oval(self.pos[0]-self.size,
                               self.pos[1]-self.size,
                               self.pos[0]+self.size,
                               self.pos[1]+self.size,
                               fill=self.color,
                               tags=self.label)

    def update(self):
        if self.dead:
            return -1
        self.move()
        if self.show:
            self.draw()
