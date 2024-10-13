#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Installing tkinter and PIL
1) pip install tk
2) pip install pillow
"""

import argparse
from tkinter import *
from PIL import Image, ImageTk
import random as random

class draw_gate_packing(Tk):
    """
    Source: https://stackoverflow.com/questions/54637795/how-to-make-a-tkinter-canvas-rectangle-transparent
    """
    def __init__(self, input_f, output_f, grid_dimensions):   
        self.scale = 0
        self.shift = 0
        super(draw_gate_packing, self).__init__()
        self.images = []
        self.title("Gate Placement Visualization")
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set the canvas size based on the screen size
        canvas_width = int(screen_width * 0.9)
        canvas_height = int(screen_height * 0.9)
        
        # Initialize canvas before using it
        self.canvas1 = Canvas(self, width=canvas_width, height=canvas_height, bg="white")
        self.canvas1.pack()

        row_size, column_size = grid_dimensions
        grid_size_x = canvas_width // column_size
        grid_size_y = canvas_height // row_size
        grid_size = min(grid_size_x, grid_size_y)
        self.scale = grid_size

        # Draw the grid on the canvas
        self.draw_grid(canvas_width, canvas_height, grid_size)
        
        for g, sz in output_f.items():
            print(g, sz)
            if g == 'bounding_box':
                self.shift = self.scale * (sz[1])
                self.create_rectangle(0, 0, self.scale * sz[0], self.scale * sz[1], outline='black', width=5)
            else:
                print(g)
                de = random.randint(0, 255)
                re = random.randint(0, 255)
                we = random.randint(0, 255)
                color = (de, re, we)
                x1 = self.scale * sz[0]
                y1 = self.shift - self.scale * input_f[g][1] - self.scale * sz[1]
                x2 = self.scale * sz[0] + self.scale * input_f[g][0]
                y2 = self.shift - self.scale * sz[1]
                print(x1, y1, x2, y2)
                self.create_rectangle(x1, y1, x2, y2, outline='black', fill=color, width=1, alpha=0.5)
                self.canvas1.create_text(x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, font=("Arial", grid_size), text=g)

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = fill + (alpha,)
            image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas1.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas1.create_rectangle(x1, y1, x2, y2, **kwargs)

    def draw_grid(self, width, height, grid_size):
        """Draws the grid lines on the canvas."""
        for i in range(0, width, grid_size):
            self.canvas1.create_line([(i, 0), (i, height)], tag="grid_line", fill="lightgray")
        for i in range(0, height, grid_size):
            self.canvas1.create_line([(0, i), (width, i)], tag="grid_line", fill="lightgray")



def visualize_gates(coordinates_file, dimensions_file, grid_dimensions):
    """Visualizes gates and their grid cell coverage."""
    # Read the dimensions file
    gate_dimensions = {}
    with open(dimensions_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            gate_info = line.split()
            if len(gate_info) != 3:
                print(f"Skipping line in dimensions file: {line.strip()}")
                continue
            name = gate_info[0]
            width = int(gate_info[1])
            height = int(gate_info[2])
            gate_dimensions[name] = (width, height)

    # Read the coordinates file
    gates = {}
    with open(coordinates_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            gate_info = line.split()
            if len(gate_info) != 3:
                print(f"Skipping line in coordinates file: {line.strip()}")
                continue
            name = gate_info[0]
            x = int(gate_info[1])
            y = int(gate_info[2])
            # if name in gate_dimensions:
            gates[name] = (x, y)

    # Draw gates and grid cells covered by the gates
    print(grid_dimensions)
    root = draw_gate_packing(gate_dimensions, gates, tuple(grid_dimensions))

    root.mainloop()

   
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize gate placement on a grid.")
    parser.add_argument(
        "coordinates_file", type=str, help="File containing gate coordinates."
    )
    parser.add_argument(
        "dimensions_file", type=str, help="File containing gate dimensions."
    )
    parser.add_argument(
        "grid_dimensions",
        type=int,
        nargs=2,
        help="Grid dimensions as row_size column_size.",
    )

    args = parser.parse_args()

    visualize_gates(args.coordinates_file, args.dimensions_file, args.grid_dimensions)
