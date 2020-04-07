from map import Map, Bot
import time
import random

def second(s):
    if s == 1:
        unit_s = 'second'
    else:
        unit_s = 'seconds'
    return s, unit_s

def minute(m):
    m_m = m // 1
    m_s = (m % 1) * 60
    if m_m == 1:
        unit_m = 'minute'
    else:
        unit_m = 'minutes'
        
    m_s, unit_s = second(m_s)


    return m_m, unit_m, m_s, unit_s

def hour(h):
    h_h = h // 1
    h_m = (h % 1) * 60
    if h_h == 1:
        unit_h = 'hour'
    else:
        unit_h = 'hours'

    h_m, unit_m, h_s, unit_s = minute(h_m)

    return h_h, unit_h, h_m, unit_m, h_s, unit_s

def print_time(s, i):
    seconds = s / i
    minutes = seconds / 60
    hours = minutes / 60

    if seconds < 60:
        s, unit_s = second(seconds)
        return f'{s:.0f} {unit_s}'

    elif seconds >= 60 and minutes < 60:
        m_m, unit_m, m_s, unit_s = minute(minutes)
        return f'{m_m:.0f} {unit_m}, {m_s:.0f} {unit_s}'

    elif minutes >= 60:
        h_h, unit_h, h_m, unit_m, h_s, unit_s = hour(hours)
        return f'{h_h:.0f} {unit_h}, {h_m:.0f} {unit_m}, {h_s:.0f} {unit_s}'


def make_my_random_room(m, x):
    i = 0
    while i <= x:
        i += 1
        m.make_rectangle(random.randint(0, m.width), random.randint(0,m.height), random.randint(0, 5), random.randint(0, 5))


def make_my_empty_room(m): #38, 20
    m.make_rectangle(0, 1, 1, 1)
    m.make_rectangle(0, 14, 1, 1)
    m.make_rectangle(0, 15, 14, 5)
    m.make_rectangle(0, 0, 14, 1)
    m.make_rectangle(14, 0, 1, 2)
    m.make_rectangle(23, 0, 2, 1)
    m.make_rectangle(37, 0, 1, 1)
    m.make_rectangle(24, 15, 14, 5)
    m.make_rectangle(14, 14, 1, 2)
    m.make_rectangle(23, 15, 1, 1)

def make_my_furnished_room(m): #38, 20
    m.make_rectangle(0, 1, 1, 1)
    m.make_rectangle(0, 14, 1, 1)
    m.make_rectangle(0, 15, 14, 5)
    m.make_rectangle(0, 0, 14, 1)
    m.make_rectangle(14, 0, 1, 2)
    m.make_rectangle(23, 0, 2, 1)
    m.make_rectangle(37, 0, 1, 1)
    m.make_rectangle(24, 15, 14, 5)
    m.make_rectangle(14, 14, 1, 2)
    m.make_rectangle(23, 15, 1, 1)
    m.make_rectangle(22, 16, 2, 4)
    m.make_rectangle(14, 2, 2, 1)
    m.make_rectangle(15, 0, 1, 2)
    m.make_rectangle(25, 0, 3, 2)
    m.make_rectangle(27, 14, 8, 1)
    m.make_rectangle(1, 14, 5, 1)
    m.make_rectangle(6, 13, 5, 2)
    m.make_rectangle(0, 2, 3, 12)
    m.make_rectangle(1, 1, 11, 3)
    m.make_rectangle(4, 5, 2, 2)
    m.make_rectangle(13, 4, 3, 3)


def make_my_big_empty_room(m): #190, 101
    m.make_rectangle(0, 4, 3, 3)
    m.make_rectangle(0, 70, 3, 3)
    m.make_rectangle(0, 73, 67, 20)
    m.make_rectangle(0, 0, 68, 3)
    m.make_rectangle(68, 0, 5, 7)
    m.make_rectangle(125, 0, 8, 3)
    m.make_rectangle(187, 0, 3, 3)
    m.make_rectangle(120, 76, 70, 25)
    m.make_rectangle(68, 68, 5, 3)
    m.make_rectangle(117, 76, 3, 5)

def scan(m, t, d=1):
    for i in range(4):
        b = t.copy()
        b.dir = i
        dis = 0
        while 0 <= b.x < m.width and 0 <= b.y < m.height:
            n = b.next()
            v = m.get(n)
            if v == 0:
                t.dir = b.dir
                return dis
            elif v == -1:
                break
            elif d > 1:
                new_dir = b.dir
                new_dis = scan(m, b, d-1)
                if new_dis is not None:
                    for i in range(dis):
                        t.dir = new_dir
                        t.fwd()
                        m.set(t.pos(), 1)
                    t.dir = b.dir
                    return new_dis
            dis += 1
            b.fwd()
    return None

def main():
    m = Map(38, 20)
    make_my_empty_room(m)
    b = Bot(random.randint(0, m.width), random.randint(0, m.height), random.randint(0,4), m)
    #b = Bot(37, 1, 3, m)
    v = m.get(b.pos())
    if v == -1:
        error = 1
        return 0, error, 0
    else:
        while True:
            m.set(b.pos(), 1)
            for i in range(4):
                n = b.next(b.dir, 1)
                v = m.get(n)
                if v != 0:
                    b.left()
                else:
                    break
            else:
                for l in range(1,3):
                    dis = scan(m, b, l)
                    if dis is not None:
                        for i in range(dis):
                            b.fwd()
                            m.set(b.pos(), 1)
                        break
                else:
                    break
            b.left()
            n = b.next()
            v = m.get(n)
            if v != 0:
                b.right()
            b.fwd()
            #m.print(p=b.pos())
            #time.sleep(0.01)
            error = 0
        return m.score(), error, b.time_passed()

if True:
    t = 0
    iteration = 0
    sum = 0
    r = 0
    sum_error = 0
    max = 1000 
    while iteration < max:
        #print(iteration)
        score, error, ti = main()

        if error == 0:
            sum += score[0]
            r += score[1]
            t += ti
        else:
            sum_error += 1

        iteration += 1

    avg_score = sum / (max-sum_error)
    avg_redun = ((r / (max-sum_error))-1)*100
    
    print(f'\nAverage Time: {print_time(t, max-sum_error)}.\n')
    print(f'{avg_score:.2f}% Covered\n{avg_redun:.2f}% Repeated')
else:
    sum = 0
    r = 0
    score, error, ti = main()
    if error == 0:
        sum += score[0]
        r += score[1]
        avg_score = sum 
        avg_redun = (r-1)*100
        
        print(f'Time: {print_time(ti, 1)}.\n')
        print(f'{avg_score:.2f}% Covered\n{avg_redun:.2f}% Repeated')
    else:
        print('ERROR: Bot spawned in wall.')