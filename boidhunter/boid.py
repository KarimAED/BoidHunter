import numpy as np

from actor import Actor


class Boid(Actor):

    def __init__(self, pos, vel, frame, label,
                 pref_dist=20, vision_range=50,
                 size=5, color="red", max_v=20, frame_size=np.array([1000, 800]), show=False):
        super().__init__(pos, vel, frame, label,
                         pref_dist, vision_range,
                         size, color, max_v, frame_size, show)

    def find_neighbours(self, other_boids, hunters):
        distances = [boid.pos-self.pos for boid in other_boids
                     if np.linalg.norm(boid.pos-self.pos) < self.vision_range]
        boids = [boid for boid in other_boids if np.linalg.norm(boid.pos-self.pos) < self.vision_range]

        self.neighbours = np.array([distances, boids])

        return [hunter.pos - self.pos for hunter in hunters if np.linalg.norm(hunter.pos-self.pos) < self.vision_range]

    def accelerate(self, other_boids, hunters):
        nb_hunters = self.find_neighbours(other_boids, hunters)
        if len(self.neighbours[0]) == 0:
            return
        avg_pos_dist = np.mean(self.neighbours[0], axis=0)
        avg_vel = np.mean([b.vel for b in self.neighbours[1]], axis=0)
        self.vel += (0.1*avg_pos_dist*np.linalg.norm(avg_pos_dist)/self.pref_dist).astype(int)
        self.vel += (0.5*(avg_vel-self.vel)).astype(int)
        for dist in self.neighbours[0]:
            if np.linalg.norm(dist) < self.pref_dist:
                self.vel -= (0.1*dist*self.pref_dist/np.linalg.norm(dist)).astype(int)

        for dist in nb_hunters:
            if np.linalg.norm(dist) < self.size*5:
                self.dead = True
            self.vel -= (100*dist/np.linalg.norm(dist)).astype(int)

        if np.linalg.norm(self.vel) > self.max_v:
            vel = self.vel * self.max_v / np.linalg.norm(self.vel)
            self.vel = vel.astype(int)
