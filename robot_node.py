import csv
class Robot_node:
    def __init__(self,robot_pos: tuple,offset_x,offset_y,scale):
        self.robot_pos = robot_pos
        self.x = self.robot_pos[0]
        self.y = self.robot_pos[1]
        self.new_x = (self.x + offset_x) / scale
        self.new_y = (self.y + offset_y) / scale
        self.new_robot_pos = (self.new_x, self.new_y)
        with open("robot_locations.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.new_robot_pos)
