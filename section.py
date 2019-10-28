from math import cos, sin, sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def get_circle_points(r, z):
    n = 360
    pi_2 = 2 * np.pi
    return np.array([(r * cos(t * pi_2 / n), r * sin(t * pi_2 / n), z) for t in range(n)])


def get_intersection(r, z, plane):
    a, b, c = plane
    s_len = a * a + b * b
    x0 = a * c / s_len
    y0 = b * c / s_len
    d = r * r - c * c / s_len
    if d < -1e-9:
        return []
    elif abs(d) < 1e-9:
        return np.array([(x0, y0, z)])
    else:
        delta = sqrt(d / s_len)
        x1 = x0 + b * delta
        x2 = x0 - b * delta
        y1 = y0 - a * delta
        y2 = y0 + a * delta
        return np.array([(x1, y1, z), (x2, y2, z)])


def find_section_by_zero_plane(obj):
    res = []
    for p in obj[obj[:1] == 0]:
        res.extend(get_circle_points(p[0], p[1]))
    return res


def find_section_by_nonzero_plane(obj, plane):
    res = []
    for i, p in enumerate(obj):
        res.extend(get_intersection(p[0], p[1], plane))
    return res


def find_section_by_plane(obj, plane):
    """
    Function for find section of some rotation figure by plane
    :param obj: ndarray of points in format (radius, z)
    :param plane: array_like object with three digits - a, b and c for plane `ax + by = c`
    :return: ndarray of points which represents section
    """

    if plane[0] == 0 and plane[1] == 0:
        if plane[2] == 0:
            res = find_section_by_zero_plane(obj)
        else:
            raise ValueError("Incorrect plane")
    else:
        res = find_section_by_nonzero_plane(obj, plane)
    return np.array(res)


def draw_plot(sections, azim=None):
    """
    Function for drawing sections of some rotation figure or figures by plane or planes
    This function draws a plot
    :param sections: array_like object with sections (ndarray) of some rotation figure or figures by plane or planes
    :param azim: stores the azimuth angle in the x,y plane (in degrees)
    """

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for section in sections:
        if len(section) == 0:
            continue
        elif len(section) == 1:
            ax.scatter(section[:, 0], section[:, 1], section[:, 2])
        else:
            section = np.concatenate((section, [section[0]]))
            ax.plot(section[:, 0], section[:, 1], zs=section[:, 2])
    ax.view_init(azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def draw_points(sections, azim=None):
    """
    Function for drawing sections of some rotation figure or figures by plane or planes
    This function draws a points without lines between it
    :param sections: array_like object with sections (ndarray) of some rotation figure or figures by plane or planes
    :param azim: stores the azimuth angle in the x,y plane (in degrees)
    """

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for section in sections:
        if len(section) == 0:
            continue
        else:
            ax.scatter(section[:, 0], section[:, 1], section[:, 2])
    ax.view_init(azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
