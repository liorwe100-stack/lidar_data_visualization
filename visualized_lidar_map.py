from operator import truediv
from sys import float_repr_style

import pygame
import csv
import sys
import math
import robot_node
import os
# ====================
# Settings
# ====================
# class visualized_lidar_map:
class Visualized_lidar_map:
    def __init__(self):
        self.window_width = 900
        self.window_height = 600
        self.background_color = (15, 15, 15)
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
    def run_map(self):
        # ====================
        # Pygame setup
        # ====================
        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("2D LiDAR Point Cloud – Apartment Scan")
        clock = pygame.time.Clock()

        # ====================
        # Main loop
        # ====================
        running = True
        b_pressed = False
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #left click
                    if b_pressed:
                        robot_node.Robot_node(event.pos,self.offset_x,self.offset_y,self.scale)
                        b_pressed = not b_pressed
                if event.type == pygame.MOUSEWHEEL:
                    self.scale = max(1, self.scale + event.y)
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    speed = self.camera_speed * 3 if keys[pygame.K_LSHIFT] else self.camera_speed
                    if keys[pygame.K_b]:
                        b_pressed = not b_pressed
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        self.offset_x += speed
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        self.offset_x -= speed
                    if keys[pygame.K_w] or keys[pygame.K_UP]:
                        self.offset_y += speed
                    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                        self.offset_y -= speed

            screen.fill(self.background_color)
            if self.check_for_updates("robot_locations.csv"):
                self.load_robot_points()
            for x, y in self.robot_points:
                px = int(x * self.scale + self.offset_x)
                py = int(y * self.scale + self.offset_y)
                pygame.draw.circle(screen, self.point_color, (px, py), self.point_radius + 10)
            if self.check_for_updates("lidar_apartment_2d_pointcloud.csv"):
                self.load_lidar_points()
            for x, y in self.lidar_points:
                px = int(x * self.scale + self.offset_x)
                py = int(y * self.scale + self.offset_y)
                pygame.draw.circle(screen, self.point_color, (px, py), self.point_radius)

            for i in range(len(self.lidar_points) - 1):
                for j in range (i + 1, len(self.lidar_points)):
                    x1, y1 = self.lidar_points[i]
                    x2, y2 = self.lidar_points[j]
                    dist = math.hypot(x2 - x1, y2 - y1)
                    if dist < self.max_dist:
                        p1 = (int(x1 * self.scale + self.offset_x), int(y1 * self.scale + self.offset_y))
                        p2 = (int(x2 * self.scale + self.offset_x), int(y2 * self.scale + self.offset_y))
                        pygame.draw.line(screen, (255,0,255), p1, p2, 1)
            # lidar_points.sort(
            #     key=lambda p: math.atan2(p[1] - LIDAR_Y, p[0] - LIDAR_X)
            # )
            pygame.display.flip()
if __name__ == "__main__":
    lidar_map = Visualized_lidar_map()
    lidar_map.run_map()
