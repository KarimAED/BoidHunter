import numpy as np


from actor import Actor


class Hunter(Actor):

    def __init__(self, pos, vel, frame, label,
                 pref_dist=20, vision_range=50,
                 size=10, color="blue", max_v=22, frame_size=np.array([1000, 800]), show=False):
        super().__init__(pos, vel, frame, label,
                         pref_dist, vision_range,
                         size, color, max_v, frame_size, show)

    def accelerate(self, boids, other_hunters):
        nb_boids = [boid.pos - self.pos for boid in boids if np.linalg.norm(boid.pos-self.pos) < self.vision_range]
        dist = [np.linalg.norm(b) for b in nb_boids]

        self.vel += np.random.randint(-2, 2, 2)

        hunter_dist = [h.pos - self.pos for h in other_hunters]

        for h_di in hunter_dist:
            d = np.linalg.norm(h_di)
            if d == 0:
                d = 1e-3
            self.vel -= (10*h_di/d).astype(int)

        if dist:
            near_boid = nb_boids[np.argmin(dist)]

            self.vel += (0.2*near_boid).astype(int)

        if np.linalg.norm(self.vel) > self.max_v:
            vel = self.vel * self.max_v / np.linalg.norm(self.vel)
            self.vel = vel.astype(int)
