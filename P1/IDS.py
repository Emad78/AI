from time import time
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

def checkedState(snake, t_point, points, depth):
    s = list()
    for it in snake:
        s.append(tuple(it))
    s = tuple(s)
    p = list()
    for y, x in points:
        p.append((y, x, points[(y, x)]))
    return (s, t_point, tuple(p), depth)

def createState(snake, t_point, points, direct, mokh, path, depth):
    
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
    path.append(direct[2])
    return [snake, t_point, points, path, depth]     

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
#    global states
#    states += 1
    if is_possible(now_state[0][:], direction, mokh):
        new_state = createState(now_state[0].copy(), now_state[1], now_state[2].copy(),direction, mokh, now_state[3].copy(), now_state[4]+1)
        if checkedState(new_state[0], new_state[1], new_state[2], len(new_state[3]) - 1) in checked:
            return False 
        q.append(new_state)
        if new_state[1] == 0:
            print(new_state[3][1:])
            return True
    return False


def IDS():    
    addr = input()
    init = readFile(addr)
    global st
    st = time()
    mokh = init[0]
    snake = [init[1]]
    t_point = init[2]
    points = init[3]
    q = []
    depth = 0
 #   global uniqe
 #   global states
 #   un = set()
    while(True):
        checked = set()
        q.append(createState(snake, t_point, points, [0, 0,''], mokh,[], 0))
        while len(q) != 0:
  #          states += 1
            now_state = q.pop()
 #           un.add(checkedState(now_state[0], now_state[1], now_state[2], len(now_state[3]) - 1))
 #           uniqe = len(un)
            checked.add(checkedState(now_state[0], now_state[1], now_state[2], len(now_state[3]) - 1))
            if now_state[1] == 0:
                print(now_state[3][1:])
                return True
            if now_state[4]+1 <= depth :
                if newState(now_state, q, [0, 1,'R'], mokh, checked):
                    return True
                if newState(now_state, q, [0, -1,'L'], mokh, checked):
                    return True
                if newState(now_state, q, [1, 0, 'D'], mokh, checked):
                    return True
                if newState(now_state, q, [-1, 0, 'U'], mokh, checked):
                    return True
        depth += 1
st = 0
#states = 0
#uniqe = 0
IDS()
#print("states: ", states)
#print("Uniqe: ", uniqe)
print(time() - st)

