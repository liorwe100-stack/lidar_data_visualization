from math import floor
import heapq
import math

class Grid_map:
    def __init__(self, width, height, max_dist):
        self.max_dist = max_dist
        self.width = width
        self.height = height
        self.grid = [[0] * height for _ in range(width)]

        #0- represents that there is nothing
    # def visualize_grid(self):
    #     for y, row in enumerate(self.grid):
    #         line = ""
    #         for x, cell in enumerate(row):
    #             elif cell == 1:
    #                 line += "█ "
    #             else:
    #                 line += ". "
    def receive_occupied_points(self,point_list: list[tuple]):
        grid = self.grid
        for x,y in point_list:
            grid[floor(x)][floor(y)] = 1
        for i in range(len(point_list) - 1):
            for j in range (i + 1, len(point_list)):
                x1,y1 = point_list[i]
                x2,y2 = point_list[j]
                rx1, ry1,rx2,ry2= round(x1), round(y1), round(x2), round(y2) #r - rounded...
                fx1,fy1,fx2,fy2 = floor(x1),floor(y1),floor(x2),floor(y2) #f - floored
                dist = math.hypot(x2 - x1, y2 - y1)
                if dist < self.max_dist:
                    if x1 != x2:  # if there is a straight line (prevents division by 0)
                        slope = round((y1 - y2) / (x1 - x2), 2)
                        # bresenham algorithm could be used
                        for x in range(min(rx1,rx2), max(rx1, rx2)):
                            y = round(slope * (x - x1) + y1)
                            self.grid[fx1][fy1] = 1
                        for y in range(min(ry1, ry2), max(ry1, ry2)):
                            x = round((y - y1 + x1 * slope) / slope)
                            self.grid[fx1][fy1] = 1
                        print(f"slope: {slope}")
                    else:
                        for y in range(min(ry1, ry2), max(ry1, ry2)):
                            self.grid[fx1][fy1] = 1
                        print("slope is on the y axis")
                    if x1 >= x2 and y1 >= y2:
                        self.grid[fx1][fy1] = 1

            # print(f"{x},{y}: {grid[floor(x)][floor(y)]}")
        self.grid = grid

    def line_of_sight(self, p1, p2):
        grid = self.grid
        x0, y0 = p1
        x1, y1 = p2

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x1 > x0 else -1
        sy = 1 if y1 > y0 else -1

        err = dx - dy

        while True:
            if grid[x0][y0] == 1:
                return False

            if (x0, y0) == (x1, y1):
                return True

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def smooth_path(self, path):
        grid = self.grid
        if len(path) <= 2:
            return path

        new_path = [path[0]]
        i = 0

        while i < len(path) - 1:

            j = len(path) - 1

            while j > i + 1:
                if self.line_of_sight(path[i], path[j]):
                    break
                j -= 1

            new_path.append(path[j])
            i = j

        return new_path

    import heapq

    def astar(self, start, goal):
        grid = self.grid
        if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
            print("Start or goal blocked")
        rows = len(grid)
        cols = len(grid[0])

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:

            current = heapq.heappop(open_set)[1]
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]

                path.append(start)
                path.reverse()
                return path

            for dx, dy in neighbors:

                nx = current[0] + dx
                ny = current[1] + dy

                if not (0 <= nx < rows and 0 <= ny < cols):
                    continue

                if grid[nx][ny] == 1:
                    continue

                neighbor = (nx, ny)

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    f = tentative_g + heuristic(neighbor, goal)

                    heapq.heappush(open_set, (f, neighbor))

        return None