import pygame
import csv
import sys

# ====================
# Settings
# ====================
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (15, 15, 15)
POINT_COLOR = (0, 220, 255)
POINT_RADIUS = 2

SCALE = 6        # scale lidar units → pixels
OFFSET_X = 40    # shift drawing right
OFFSET_Y = 40    # shift drawing down

# ====================
# Load LiDAR point cloud
# ====================
points = []

with open("lidar_apartment_2d_pointcloud.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        x = float(row["x"])
        y = float(row["y"])
        points.append((x, y))

# ====================
# Pygame setup
# ====================
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
            running = False

    screen.fill(BACKGROUND_COLOR)

    for x, y in points:
        px = int(x * SCALE + OFFSET_X)
        py = int(y * SCALE + OFFSET_Y)
        pygame.draw.circle(screen, POINT_COLOR, (px, py), POINT_RADIUS)

    pygame.display.flip()

pygame.quit()
sys.exit()
