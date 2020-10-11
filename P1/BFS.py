from collections import deque
from time import time
def co(l1):
    l2 = l1[:]
    return list(l2)
def readFile(name):
    f = open(name, 'r')
    result = []
    ma = list(map(int, f.readline().split(',')))
    result.append(ma)
    head = list(map(int, f.readline().split(',')))
    result.append(head)
    t = int(f.readline())
    k = 0
    points = {}
    for i in range(t):
        a = list(map(int, f.readline().split(',')))
        points[tuple(a[:2])] = a[2]
        k += a[2]
    result.append(k)
    result.append(points)
    f.close()
    return result

def checkedState(snake, t_point, points):
    s = list()
    for it in snake:
        s.append(tuple(it))
    s = tuple(s)
    p = list()
    for y, x in points:
        p.append((y, x, points[(y, x)]))
    return (s, t_point, tuple(p))

def createState(snake, t_point, points, direct, mokh, path):

    head_y = (snake[-1][0]+direct[0]+mokh[0])%mokh[0] 
    head_x = (snake[-1][1]+direct[1]+mokh[1])%mokh[1]


    if((head_y, head_x) in points.keys()):
        if points[(head_y, head_x)] > 0:
            points[(head_y, head_x)] -= 1
            snake.append([head_y, head_x])
            t_point -= 1
    else:
        for i in range(len(snake)-1):
            snake[i] = snake[i+1]
        snake[-1] = [head_y, head_x]
    path.append(direct)
    return [snake, t_point, points, path]     

def is_possible(snake, direction, mokh):
    head_y = (snake[-1][0]+direction[0])%mokh[0]
    head_x = (snake[-1][1]+direction[1])%mokh[1]
    if [head_y, head_x] in snake and [head_y, head_x] != snake[0]:
        return False
    if len(snake)>1:
        if [head_y, head_x] == snake[-2]:
            return False
    return True 

def newState(now_state, q, direction, mokh,checked):
    if is_possible(now_state[0][:], direction, mokh):
        l1 = now_state[0][:]
        l2 = now_state[2].copy()
        l3 = now_state[3][:]
        new_state = createState(l1, now_state[1], l2,direction, mokh, l3)
        if checkedState(new_state[0], new_state[1], new_state[2]) in checked:
            return False 
        q.append(new_state)
        if new_state[1] == 0:
            print(new_state[3][1:])
            return True
    return False
    
def BFS():    
    addr = input()
    init = readFile(addr)
    mokh = init[0]
    snake = [init[1]]
    t_point = init[2]
    points = init[3]
    q = []
    checked = set()
    q.append(createState(snake, t_point, points, [0, 0], mokh,[]))
    k = 0
    while(len(q)):
        now_state = q[k]
        k += 1
        checked.add(checkedState(now_state[0], now_state[1], now_state[2]))
        if now_state[1] == 0:
            print(now_state[3][1:])
            return True
        if newState(now_state, q, [0, 1], mokh, checked):
            return True
        if newState(now_state, q, [0, -1], mokh, checked):
            return True
        if newState(now_state, q, [1, 0], mokh, checked):
            return True
        if newState(now_state, q, [-1, 0], mokh, checked):
            return True
st = time()
BFS()
print(time() - st)
