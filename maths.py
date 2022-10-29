import math

#Collision detection function
def touching(c, points, rad):
    for i in points:
        if len(i) != 2:
            continue

        px = i[1][0] - i[0][0]
        py = i[1][1] - i[0][1]

        norm = px * px + py * py

        u = ((c[0] - i[0][0]) * px + (c[1] - i[0][1]) * py) / float(norm)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0

        x = i[0][0] + u * px
        y = i[0][1] + u * py

        dx = x - c[0]
        dy = y - c[1]

        dist = (dx * dx + dy * dy) ** .5
        if rad >= dist:
            return True, points.index(i)

    return False, None

#change of coordinates to accomodate pygame
def coords(W, H, pos):
    return [pos[0] + W // 2, pos[1] + H // 2]

#calculating dot product between two vectors
def dot_product(vect1, vect2):
    return (vect1[0] * vect2[0]) + (vect1[1] * vect2[1])

#producing a normalized vector from two points
def normalize(pos1, pos2):
    dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    line = [(pos2[0] - pos1[0]) / dist, (pos2[1] - pos1[1]) / dist]

    return [-line[1], line[0]]

#using dot product for projection
def projection(normal, dp):
    normal[0] *= dp
    normal[1] *= dp
    return normal

#calculating the new vector using a projection
def new_vect(proj, vect):
    vect[0] -= 2 * proj[0]
    vect[1] -= 2 * proj[1]
    return vect

#combining all functions above to calculate the new directional vector
def change_direction(pos1, pos2, v):
    n = normalize(pos1, pos2)
    dp = dot_product(n, v)
    proje = projection(n, dp)
    return new_vect(proje, v)
