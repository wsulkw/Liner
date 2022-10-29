import math
import random

import pygame

from maths import touching, change_direction

pygame.font.init()

W, H = 1920, 1080

WIN = pygame.display.set_mode((W, H))

GRAY = (30, 30, 30)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

points = [[], []]

draw = True
go = False
end = False

f = pygame.font.SysFont('calibre', 100)
hs_f = pygame.font.SysFont('calibre', 50)

score = 0


class Circle:
    def __init__(self):
        self.x = W // 2
        self.y = H // 2
        self.initialAngle = random.random() * 6.28
        self.dy = math.sin(self.initialAngle)
        self.dx = math.cos(self.initialAngle)
        self.vel = 2
        self.r = 10

    def update(self):
        self.x += self.dx * self.vel
        self.y += self.dy * self.vel
        pygame.draw.circle(WIN, GRAY, (self.x, self.y), self.r)

    def bounds_check(self):
        if not (0 + self.r <= self.x <= W - self.r) or not (self.r <= self.y <= H - self.r):
            return True

        return False


p = Circle()


def get_hs():
    with open('hs.txt', 'r+') as file:
        num = file.read()

        if score > int(num):
            file.close()

            with open('hs.txt', 'w') as file:
                file.truncate(0)
                file.write(str(score))
            num = score

        file.close()

    return num


def end_sequence():
    WIN.fill(LIGHT_GRAY)

    score_txt = f.render(f"{score}", True, GRAY)
    score_txt_rect = score_txt.get_rect(center=(W // 2, H // 2 - 300))
    WIN.blit(score_txt, score_txt_rect)

    highscore_txt = hs_f.render(f"{get_hs()}", True, GRAY)
    highscore_txt_rect = highscore_txt.get_rect(center=(W // 2, H // 2 - 200))
    WIN.blit(highscore_txt, highscore_txt_rect)

    restart_rect = pygame.Rect(W // 2 - 100, H // 2 - 50, 200, 100)
    pygame.draw.rect(WIN, GRAY, restart_rect)

    restart_txt = hs_f.render("restart", True, LIGHT_GRAY)
    restart_txt_rect = restart_txt.get_rect(center=(W // 2, H // 2))
    WIN.blit(restart_txt, restart_txt_rect)
    pygame.display.update()


def redraw():
    global draw, points, run, score, go, end

    WIN.fill(LIGHT_GRAY)

    if p.bounds_check():
        draw = False
        end = True

    touch, index = touching((p.x, p.y), points, p.r)
    if touch:
        p.vel += 0.03

        score += 1

        v = change_direction(points[index][0], points[index][1], [p.dx, p.dy])
        p.dx = v[0]
        p.dy = v[1]

        del points[index]
        points.append([])

        draw = True

    mpos = pygame.mouse.get_pos()
    if len(points[1]) == 2:
        draw = False
        pygame.draw.line(WIN, BLACK, points[0][0], points[0][1], 2)
        pygame.draw.line(WIN, BLACK, points[1][0], points[1][1], 2)
    elif len(points[1]) == 1:
        pygame.draw.line(WIN, BLACK, points[0][0], points[0][1], 2)
        pygame.draw.line(WIN, BLACK, points[1][0], mpos, 2)
    elif len(points[0]) == 2:
        pygame.draw.line(WIN, BLACK, points[0][0], points[0][1], 2)
    elif len(points[0]) == 1:
        pygame.draw.line(WIN, BLACK, points[0][0], mpos, 2)

    scoretext = f.render(f"{score}", False, GRAY)
    WIN.blit(scoretext, (0, 0))

    if go:
        p.update()
    else:
        pygame.draw.circle(WIN, GRAY, [W // 2, H // 2], p.r)

    pygame.display.update()


run = True
clock = pygame.time.Clock()
while run:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = list(pygame.mouse.get_pos())
                if draw:
                    go = True
                    if len(points[0]) != 2:
                        if pos not in points[0]:
                            points[0].append(pos)
                    else:
                        if pos not in points[1]:
                            points[1].append(pos)
                else:
                    if W // 2 - 100 <= pos[0] <= W // 2 + 100:
                        if H // 2 - 50 <= pos[1] <= H // 2 + 50:
                            end = False
                            draw = True
                            go = False
                            p = Circle()
                            points = [[], []]
                            score = 0

    if not end:
        redraw()
    else:
        end_sequence()

pygame.quit()
