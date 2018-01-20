import math
import random

def inRectangle(point,width,height):
    return point[0]>=0 and point[0]<width and point[1]>=0 and point[1]<height

def generateNeighboringPoints(point, mindist):
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)

    #generate radius in (mindist, 2*mindist) and angle in (0,2 * pi)
    radius = mindist * (r1*4 + 1);
    angle = 2 * math.pi * r2;

    newX = point[0] + radius * math.cos(angle)
    newY = point[1] + radius * math.sin(angle)
    return (newX, newY);

def inNeighbourhood(grid, point, mindist, cellSize, width, height, grey_value):
    x=int(point[0]/cellSize)
    y=int(point[1]/cellSize)
    gridPoint = grid[x][y]

    for i in range(-4,5):
        for j in range(-4,5):
            if inRectangle((x+i,y+j),int(width/cellSize)+1,int(height/cellSize)+1) and (grid[x+i][y+j] != (-1,-1)):
                dis = math.sqrt(math.pow((grid[x+i][y+j][0]-point[0]),2) + math.pow((grid[x+i][y+j][1]-point[1]),2))
                if dis< mindist*(1+2*(grey_value/255.0)): return True
    print("$$",math.sqrt(math.pow((grid[x][y][0]-point[0]),2) + math.pow((grid[x][y][1]-point[1]),2)))
    return False

def poisson(width, height, min_dist, new_points_count, grey):
    cellSize = min_dist/math.sqrt(2);

    grid = [[(-1,-1)]*(int(height/cellSize)+1) for _ in range(int(width/cellSize)+1)]

    rdsample = []
    samplePoints = []
    pointInit = (random.uniform(0,width), random.uniform(0,height))

    rdsample.append(pointInit)
    samplePoints.append(pointInit)
    
    grid[int(pointInit[0]/cellSize)][int(pointInit[1]/cellSize)] = pointInit

    iter = 0
    while len(rdsample) > 0:
        pointNow = rdsample.pop(random.randint(0,len(rdsample)-1))
        for i in range(new_points_count):
            newPoint = generateNeighboringPoints(pointNow, min_dist)
            if (inRectangle(newPoint,width,height) and not inNeighbourhood(grid, newPoint, min_dist,cellSize,width,height, grey[int(newPoint[1])][int(newPoint[0])][0]+grey[int(pointNow[1])][int(pointNow[0])][0])):
                rdsample.append(newPoint);
                samplePoints.append(newPoint);
                print('#',grid[int(newPoint[0]/cellSize)][int(newPoint[1]/cellSize)])
                print(math.sqrt(math.pow(grid[int(newPoint[0]/cellSize)][int(newPoint[1]/cellSize)][0]-newPoint[0],2)+ math.pow((grid[int(newPoint[0]/cellSize)][int(newPoint[1]/cellSize)][1]-newPoint[1]),2)))
                grid[int(newPoint[0]/cellSize)][int(newPoint[1]/cellSize)] = newPoint
                print(newPoint)

    print("hehe")
    return samplePoints
#poisson(1080, 680, 10, 20)

