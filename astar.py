from astar_node import Node
import heapq
#this is A* algorithm on a 2d grid created by liorwe100 on GitHub
#for the function you need to give it a 2d list as the grid
#a tuple of x and y coordinates for the start and end goal
#it returns a list of Nodes that represents the best path it has found
def astar(grid,start,end):
    start_node = Node(start)
    end_node = Node(end)
    start_node.setH(end_node)

    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    tosearch = []
    heapq.heappush(tosearch, start_node)

    tosearch_dict = {start: start_node}
    processed = set()
    while len(tosearch) > 0:
        current = heapq.heappop(tosearch)
        if current.pos in processed:
            continue
        processed.add(current.pos)

        if current == end_node:
            path = []
            while current != start_node:
                path.append(current)
                current = current.parent
            return path

        for  dx,dy in neighbors:
            nx = current.pos[0] + dx
            ny = current.pos[1] + dy
            if not(0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue
            if grid[nx][ny] != 0:
                continue
            if (nx,ny) in processed:
                continue
            neighbor_node = Node((nx,ny),current.g + (14 if 0 not in (dx,dy) else 10), current)
            found_node = None
            insearch = False
            if (nx,ny) in tosearch_dict:
                found_node = tosearch_dict[(nx,ny)]
                if found_node.g > neighbor_node.g:
                    found_node.setG(neighbor_node.g)
                    found_node.setParent(current)
                    heapq.heappush(tosearch,found_node)
            else:
                neighbor_node.setH(end_node)
                heapq.heappush(tosearch, neighbor_node)
                tosearch_dict[(nx,ny)] = neighbor_node

def astar_path(grid, start,end):
    sx,sy = start
    ex,ey = end
    if grid[sx][sy] != 0 or grid[ex][ey] != 0:
        print("start or end values are on a obstacle")
        return None
    path = astar(grid, start, end)
    path_set = []
    for node in path:
        path_set.append(node.pos)
    return path_set



