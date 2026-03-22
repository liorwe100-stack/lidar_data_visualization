from operator import truediv
from sys import float_repr_style

import pygame
import csv
import sys
import math
from math import floor
import robot_node
import os
import grid_map
import astar
# ====================
# Settings
# ====================
# class visualized_lidar_map:
class Visualized_lidar_map:
    def __init__(self):
        self.window_width = 900
        self.window_height = 600
        self.background_color = (15, 15, 15)
        self.screen = None
        self.point_color = (0, 220, 255)
        self.point_radius = 2

        self.scale = 6        # scale lidar units → pixels
        self.offset_x = 40    # shift drawing right
        self.offset_y = 40    # shift drawing down
        self.max_dist = 1.4     # lidar units
        self.camera_speed = 30
        self.lidar_points = []
        self.load_lidar_points()
        self.robot_points = []
        self.load_robot_points()
        self.last_modified_time = {"robot_locations.csv": None, "lidar_apartment_2d_pointcloud.csv": None}
        self.grid = grid_map.Grid_map(self.window_width,self.window_height,self.max_dist)
        self.grid.receive_occupied_points(self.lidar_points)
        self.key_toggle = {"b": False, "p": False, "p1": False}
        self.key_toggle_offlist = {"b":"p,p1","p": "b"}  #write like this: {"a": "b,c,d",...} for each key that when turned on others need to turn off
        self.startgoal_points = {"start": (100,100), "goal": (100,100)} #example point presented here (just so there is no yellow error)
        # self.path = self.grid.astar((50,50), (400,400))
        # if self.path:
        #     self.path = self.grid.smooth_path(self.path)

    def check_for_updates(self, file_name: str):
        current_modified_time = os.path.getmtime(file_name)
        if self.last_modified_time[file_name] is None:
            self.last_modified_time[file_name] = current_modified_time
            return False
        if self.last_modified_time[file_name] != current_modified_time:
            self.last_modified_time[file_name] = current_modified_time
            print("file have been changed")
            return True
        else:
            return False
    def load_lidar_points(self):
        lidar_points = []
        with open("lidar_apartment_2d_pointcloud.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                lidar_points.append((x, y))
        self.lidar_points = lidar_points
    def load_robot_points(self):
        robot_points = []
        with open("robot_locations.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                robot_points.append((x, y))
        self.robot_points = robot_points
    # def draw_points(self,point_list):
    def toggle_key(self, key, onoff=None):
        if onoff is None:
            self.key_toggle[key] = not self.key_toggle[key]
        else:
            self.key_toggle[key] = onoff
    def toggle_other_keys(self,key, onoff=False): #enter the key that is being toggled
        key_list = self.key_toggle_offlist[key].split(",")
        for x in key_list:
            self.toggle_key(x,onoff)
    def unscale_point(self,point: tuple):
        x = int((point[0] - self.offset_x) / self.scale)
        y = int((point[1] - self.offset_y) / self.scale)
        return (x,y)
    def find_path(self):
        start = self.startgoal_points["start"]
        start = self.unscale_point(start)
        goal = self.startgoal_points["goal"]
        goal = self.unscale_point(goal)
        path = astar.astar_path(self.grid.grid,start,goal)
        if path is not None:
            for i in path:                      #need to fix problem if the path is a straight line on the x axis ("TypeError: 'NoneType' object is not iterable")
                self.grid.grid[i[0] * self.grid.grid_scale][i[1] * self.grid.grid_scale] = 1
                print(i[0],i[1])
            print("finished")

    def run_map(self):
        # ====================
        # Pygame setup
        # ====================
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("2D LiDAR Point Cloud – Apartment Scan")
        clock = pygame.time.Clock()

        # ====================
        # Main loop
        # ====================
        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #left click
                    if self.key_toggle["b"]:
                        robot_node.Robot_node(event.pos,self.offset_x,self.offset_y,self.scale)
                        self.toggle_key("b")
                    if self.key_toggle["p"]:
                        self.startgoal_points["start"] = event.pos
                        self.toggle_key("p") #turn back off the p_key toggle
                        self.toggle_key("p1", True)
                        print("p1 Toggled on:", self.key_toggle["p1"])
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #right click
                    if self.key_toggle["p1"]: #if a start pos was already established
                        self.startgoal_points["goal"] = event.pos
                        self.find_path()
                        self.toggle_key("p1")
                if event.type == pygame.MOUSEWHEEL:
                    self.scale = max(1, self.scale + event.y)
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    speed = self.camera_speed * 3 if keys[pygame.K_LSHIFT] else self.camera_speed
                    if keys[pygame.K_p]:
                        self.toggle_key("p")
                        print("p toggled on")
                        self.toggle_other_keys("p")
                    if keys[pygame.K_b]:
                        self.toggle_key("b")
                        self.toggle_other_keys("b")
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        self.offset_x += speed
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        self.offset_x -= speed
                    if keys[pygame.K_w] or keys[pygame.K_UP]:
                        self.offset_y += speed
                    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                        self.offset_y -= speed

            self.screen.fill(self.background_color)
            if self.check_for_updates("robot_locations.csv"):
                self.load_robot_points()
            for x, y in self.robot_points:
                px = int(x * self.scale + self.offset_x)
                py = int(y * self.scale + self.offset_y)
                pygame.draw.circle(self.screen, self.point_color, (px, py), self.point_radius + 10)
            if self.check_for_updates("lidar_apartment_2d_pointcloud.csv"):
                self.load_lidar_points()
            for x, y in self.lidar_points:
                px = int(x * self.scale + self.offset_x)
                py = int(y * self.scale + self.offset_y)
                pygame.draw.circle(self.screen, self.point_color, (px, py), self.point_radius)
            # for i in range(len(self.path) - 1):
            #     x1,y1 = self.path[i]
            #     x2,y2 = self.path[i + 1]
            #     p1 = (int(x1 * self.scale + self.offset_x), int(y1 * self.scale + self.offset_y))
            #     p2 = (int(x2 * self.scale + self.offset_x), int(y2 * self.scale + self.offset_y))
            #     pygame.draw.line(self.screen, (255, 0, 255), p1, p2, 1)
            for i in range(len(self.lidar_points) - 1):
                for j in range (i + 1, len(self.lidar_points)):
                    x1, y1 = self.lidar_points[i]
                    x2, y2 = self.lidar_points[j]
                    dist = math.hypot(x2 - x1, y2 - y1)
                    if dist < self.max_dist:
                        p1 = (int(x1 * self.scale + self.offset_x), int(y1 * self.scale + self.offset_y))
                        p2 = (int(x2 * self.scale + self.offset_x), int(y2 * self.scale + self.offset_y))
                        pygame.draw.line(self.screen, (255,0,255), p1, p2, 1)
            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    if self.grid.grid[x][y] == 1:
                        px = int(x / self.grid.grid_scale * self.scale + self.offset_x)
                        py = int(y / self.grid.grid_scale * self.scale + self.offset_y)
                        pygame.draw.circle(self.screen,(0,0,255), (px,py), 1)
            # lidar_points.sort(
            #     key=lambda p: math.atan2(p[1] - LIDAR_Y, p[0] - LIDAR_X)
            # )
            pygame.display.flip()
if __name__ == "__main__":
    lidar_map = Visualized_lidar_map()
    lidar_map.run_map()
