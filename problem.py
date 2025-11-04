import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

class Problem:
    def __init__(self):
        self.X = []
        self.Y = []
        self.Z = []

    def generate_initial_state(self):
        rx = random.randint(0, len(self.X)-1)
        ry = random.randint(0, len(self.Y)-1)
        return (rx, ry)


    def get_evaluation(self,state):
        x, y = state
        return self.Z[y][x]
    
    def get_successor(self, state):
        x, y = state
        possible_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1,y+1), (x+1,y-1), (x-1,y+1), (x-1,y-1)]  
        valid_moves = []
        for move in possible_moves:
            if self.is_valid(move):  
                valid_moves.append(move)
        if valid_moves:
            return valid_moves  
        return None  
    
    def is_valid(self, state):
        x, y = state
        return (x >= 0 and x < len(self.X) and y >= 0 and y < len(self.Y))
    
    def load_state_space(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        h, w = img.shape
        self.X = np.arange(w)
        self.Y = np.arange(h)
        self.Z = img


    def show(self):
        X, Y = np.meshgrid(self.X,self.Y)
        fig = plt.figure(figsize=(8,6))
        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, self.Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        return ax
    
    def draw_path(self,path):
        ax = self.show()
        x, y, z = zip(*path)
        ax.plot(x, y, z, 'r-', zorder=3, linewidth=0.5)
        plt.show()
