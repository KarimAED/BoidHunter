import tkinter as tk
import numpy as np

from boid import Boid
from hunter import Hunter

boids = np.array([])
hunters = np.array([])
iter = 0

master = tk.Tk()
frame_params = {
    "master": master,
    "width": 1000,
    "height": 800
}
frame = tk.Canvas(**frame_params)


def add_boid(x, y):
    global boids, frame, frame_params
    b = Boid(np.array([x, y]),
             np.random.randint(-20, 20, 2),
             frame=frame, label=len(boids),
             pref_dist=50, vision_range=100,
             frame_size=np.array([frame_params["width"], frame_params["height"]]), show=True)
    boids = np.append(boids, [b])


def add_hunter(x, y):
    global hunters, frame, frame_params
    h = Hunter(np.array([x, y]),
               np.random.randint(-20, 20, 2),
               frame=frame, label="h_" + str(len(hunters)),
               pref_dist=50, vision_range=300,
               frame_size=np.array([frame_params["width"], frame_params["height"]]), show=True)
    hunters = np.append(hunters, [h])


def it():
    global boids, hunters, frame, master, iter, frame_params
    iter += 1
    frame.delete("all")
    frame.create_text(100, 10, text=f"Iterations: {iter}")
    frame.create_text(frame_params["width"] / 2, 10, text=f"Prey: {len(boids)}")
    frame.create_text(frame_params["width"] - 100, 10, text=f"Predators: {len(hunters)}")
    boid_cp = boids.copy()
    for i in range(len(boids)):
        other_boids = boid_cp[np.arange(len(boids)) != i]
        boids[i].accelerate(other_boids, hunters)

    hunter_cp = hunters.copy()
    for i in range(len(hunters)):
        other_hunters = hunter_cp[np.arange(len(hunters)) != i]
        hunters[i].accelerate(boid_cp, other_hunters)

    mask = []
    for i in range(len(boids)):
        u = boids[i].update()
        if u == -1:
            mask.append(False)
        else:
            mask.append(True)

    boids = boids[mask]

    for hunter in hunters:
        hunter.update()

    if len(boids) < 10:
        return
    master.after(1, it)


def main():
    add_ev_boid = lambda e: add_boid(e.x, e.y)
    add_ev_hunter = lambda e: add_hunter(e.x, e.y)

    frame.pack()
    frame.bind("<Button-1>", add_ev_boid)
    frame.bind("<Button-3>", add_ev_hunter)

    for i in range(5):
        for j in range(10):
            add_boid(200+50*i, 100+50*j)

    add_hunter(500, 225)
    add_hunter(100, 225)

    it()

    master.mainloop()


if __name__ == "__main__":
    main()
