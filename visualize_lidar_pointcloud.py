import pygame
import csv
import sys
import math

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
MAX_DIST = 10    # lidar units
CAMERA_SPEED = 10

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
        if event.type == pygame.MOUSEWHEEL:
            SCALE = max(1, SCALE + event.y)
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            speed = CAMERA_SPEED * 3 if keys[pygame.K_LSHIFT] else CAMERA_SPEED

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                OFFSET_X += speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                OFFSET_X -= speed
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                OFFSET_Y += speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                OFFSET_Y -= speed

    screen.fill(BACKGROUND_COLOR)

    for x, y in points:
        px = int(x * SCALE + OFFSET_X)
        py = int(y * SCALE + OFFSET_Y)
        pygame.draw.circle(screen, POINT_COLOR, (px, py), POINT_RADIUS)



    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        dist = math.hypot(x2 - x1, y2 - y1)
        if dist < MAX_DIST:
            p1 = (int(x1 * SCALE + OFFSET_X), int(y1 * SCALE + OFFSET_Y))
            p2 = (int(x2 * SCALE + OFFSET_X), int(y2 * SCALE + OFFSET_Y))
            pygame.draw.line(screen, (255, 0, 255), p1, p2, 1)
    # points.sort(
    #     key=lambda p: math.atan2(p[1] - LIDAR_Y, p[0] - LIDAR_X)
    # )
    pygame.display.flip()

pygame.quit()
sys.exit()
