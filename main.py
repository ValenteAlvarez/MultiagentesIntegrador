# Model design
import agentpy as ap
import numpy as np

# Visualization
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import IPython

class Ball(ap.Agent):
	def setup(self):
		self.trajectories = [list(), list()]
		self.velocityX = self.model.random.uniform(-1,1)
		self.velocityY = self.model.random.uniform(-1,1)

	def advance(self):
		currX, currY = self.model.space.positions[self]

		if currX <= 0 or currX >= 50:
			self.bounce('x')
		if currY <= 0 or currY >= 50:
			self.bounce('y')

		newPosition = [currX + self.velocityX, currY + self.velocityY]
		self.model.space.move_to(self, newPosition)
		self.logTrajectory(newPosition[0], newPosition[1])
	
	def bounce(self, bounceAxis):
		if bounceAxis == 'x':
			self.velocityX = -self.velocityX
		elif bounceAxis == 'y':
			self.velocityY = -self.velocityY

	def logTrajectory(self, x, y):
		self.trajectories[0].append(round(float(x), 3))
		self.trajectories[1].append(round(float(y), 3))

class BouncingBallsModel(ap.Model):
	def setup(self):
		self.space = ap.Space(self, shape=[50, 50])
		self.agents = ap.AgentList(self, self.p.agents, Ball)
		self.space.add_agents(self.agents, random=True)

	def step(self):
		for ball in self.agents:
			ball.advance()


# Parameters
parameters = {'agents': 10, 'steps': 200}
model = BouncingBallsModel(parameters)
model.setup()

fig, ax = plt.subplots()
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
scat = ax.scatter([], [], s=100)



def update(frame):
	model.step()
	xs, ys = zip(*[model.space.positions[a] for a in model.agents])
	scat.set_offsets(list(zip(xs, ys)))
	return scat

ani = FuncAnimation(fig, update, frames=parameters['steps'], interval=50, repeat=False)
plt.show()

import json

# JSON Log
allTrajectories = []

for index, ball in enumerate(model.agents):
	agentData = {
		"id": index,
		"x": ball.trajectories[0],
		"y": ball.trajectories[1]
	}
	allTrajectories.append(agentData)

dataToSave = { "data": allTrajectories }

with open("./all_trajectories.json", "w") as f:
    json.dump(dataToSave, f, indent=2)