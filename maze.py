import pygame
import sys


if __name__ == '__main__':
    print('Введите высоту и ширину поля:')
    n, m = map(int, input().split())
    board = [[[1,1,1,1,0] for j in range(m)] for i in range(n)] # Клетка содержит пять полей: стена сверху, справа, снизу, слева, состояние клетки.
    for i in range(n):
        board[i][0][3] = 0
        board[i][-1][1] = 0
    for j in range(m):
        board[0][j][0] = 0
        board[-1][j][2] = 0
    print('Введите кординаты стен в следуюшем формате:'
          '\n<координаты клетки отсчитывая с левого нижнего угла, отсчёт с 1> '
          '<положение стены: 1 - сверху; 2 - справа; 3 - снизу; 4 - слева>'
          '\n ...'
          '\nПустая строка - конец ввода.')
    wall = input()
    while wall != '':
        x, y, command = map(int, wall.split())
        if command == 1:
            board[-y][x - 1][0] = 0
            board[(-y - 1) % n][x - 1][2] = 0
        elif command == 2:
            board[-y][x - 1][1] = 0
            board[-y][x % m][3] = 0
        elif command == 3:
            board[-y][x - 1][2] = 0
            board[(-y + 1) % n][x - 1][0] = 0
        elif command == 4:
            board[-y][x - 1][3] = 0
            board[-y][(x - 2) % m][1] = 0
        wall = input()

    size = 800
    if n > m:
        scale = size / n
        height = size
        width = scale * m
    else:
        scale = size / m
        width = size
        height = scale * n
    fps = 30
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    start_read = False
    end_read = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                y, x = pygame.mouse.get_pos()
                y = y // int(scale)
                x = x // int(scale)
                if not start_read:
                    start = (x, y)
                    start_read = True
                    explored = {start[:]: [0, 0, 0]}
                    found = {}
                elif not end_read:
                    end = (x, y)
                    end_read = True
                else:
                    start = (x, y)
                    start_read = True
                    explored = {start[:]: [0, 0, 0]}
                    found = {}
                    end_read = False
                    for j in range(n):
                        for i in range(m):
                            board[j][i][-1] = 0
        screen.fill((255, 255, 255))
        for i in range(n):
            for j in range(m):
                elem = board[i][j][-1]
                if elem == 1:
                    pygame.draw.rect(screen, (200, 200, 200),
                                     (j * scale, i * scale, scale, scale))
                elif elem == 2:
                    pygame.draw.rect(screen, (255, 255, 155),
                                     (j * scale, i * scale, scale, scale))
        if end_read:
            if end not in found.keys():
                y, x = start
                pygame.draw.circle(screen, (0, 0, 0),
                                   ((x + 0.5) * scale, (y + 0.5) * scale),
                                   scale * 0.5)
                optimal_way = min(explored.values())
                for coordinates in explored.keys():
                    if explored[coordinates] == optimal_way:
                        optimal_cords = coordinates
                        break
                point = board[optimal_cords[0]][optimal_cords[1]]
                if point[0]:
                    res_cords = (optimal_cords[0] - 1, optimal_cords[1])
                    y, x = res_cords
                    board[y][x][-1] = 1
                    if res_cords not in found.keys():
                        res_way = [optimal_way[0], optimal_way[1] + 1,
                                   optimal_cords]
                        if optimal_cords[0] <= end[0]:
                            res_way[0] += 1
                        else:
                            res_way[0] -= 1
                        explored[res_cords] = min(explored.get(res_cords, res_way),
                                                  res_way)
                if point[1]:
                    res_cords = (optimal_cords[0], optimal_cords[1] + 1)
                    y, x = res_cords
                    board[y][x][-1] = 1
                    if res_cords not in found.keys():
                        res_way = [optimal_way[0], optimal_way[1] + 1,
                                   optimal_cords]
                        if optimal_cords[1] >= end[1]:
                            res_way[0] += 1
                        else:
                            res_way[0] -= 1
                        explored[res_cords] = min(explored.get(res_cords, res_way),
                                                  res_way)
                if point[2]:
                    res_cords = (optimal_cords[0] + 1, optimal_cords[1])
                    y, x = res_cords
                    board[y][x][-1] = 1
                    if res_cords not in found.keys():
                        res_way = [optimal_way[0], optimal_way[1] + 1,
                                   optimal_cords]
                        if optimal_cords[0] >= end[0]:
                            res_way[0] += 1
                        else:
                            res_way[0] -= 1
                        explored[res_cords] = min(explored.get(res_cords, res_way),
                                                  res_way)
                if point[3]:
                    res_cords = (optimal_cords[0], optimal_cords[1] - 1)
                    y, x = res_cords
                    board[y][x][-1] = 1
                    if res_cords not in found.keys():
                        res_way = [optimal_way[0], optimal_way[1] + 1,
                                   optimal_cords]
                        if optimal_cords[1] <= end[1]:
                            res_way[0] += 1
                        else:
                            res_way[0] -= 1
                        explored[res_cords] = min(explored.get(res_cords, res_way),
                                                  res_way)
                found[optimal_cords] = optimal_way

                explored.pop(optimal_cords)
            else:
                y, x = end
                pygame.draw.circle(screen, (0, 0, 0),
                                   ((x + 0.5) * scale, (y + 0.5) * scale),
                                   scale * 0.5)
                previous = end
                while previous != start:
                    y, x = previous
                    board[y][x][-1] = 2
                    previous = found[previous][2]
                x, y = start
                board[x][y][-1] = 2
        elif start_read:
            y, x = start
            pygame.draw.circle(screen, (0, 0, 0),  ((x + 0.5) * scale, (y + 0.5) * scale), scale * 0.5)

        for i in range(n + 1):
            pygame.draw.line(screen, (0, 0, 0), (0, i * scale),
                             (m * scale, i * scale), 3)
        for i in range(m + 1):
            pygame.draw.line(screen, (0, 0, 0), (i * scale, 0),
                         (i * scale, n * scale), 3)

        for j in range(n):
            for i in range(m):
                elem = board[j][i]
                if not elem[0]:
                    pygame.draw.line(screen, (0, 0, 0), (i * scale, j * scale),
                                     ((i + 1) * scale, j * scale), 10)
                if not elem[1]:
                    pygame.draw.line(screen, (0, 0, 0), ((i + 1) * scale, j * scale),
                                     ((i + 1) * scale, (j + 1) * scale), 10)
                if not elem[2]:
                    pygame.draw.line(screen, (0, 0, 0), (i * scale, (j + 1) * scale),
                                     ((i + 1) * scale, (j + 1) * scale), 10)
                if not elem[3]:
                    pygame.draw.line(screen, (0, 0, 0), (i * scale, j * scale),
                                     (i * scale, (j + 1) * scale), 10)
        pygame.display.flip()
        clock.tick(fps)