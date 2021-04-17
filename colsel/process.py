import numpy as np
from numba import njit


@njit
def colour_slicing(image_numpy, colour_point, radius, beautify, cube, width_p, height_p, positions): #*args and **kwargs do not work with numba
    
    gray_points = np.copy(image_numpy)

    if positions is None:
        start_width = 0
        start_height = 0
        if width_p > gray_points.shape[1]:
            width = gray_points.shape[1]
        else:
            width = width_p
        if height_p > gray_points.shape[0]:
            height = gray_points.shape[0]
        else:
            height = height_p
    else:
        width = int(width_p/2)
        height = int(height_p/2)
        y, x = positions
        start_width = max(0, x - width)
        start_height = max(0, y - height)
        width = min(image_numpy.shape[1], x + width)
        height = min(image_numpy.shape[0], y + height)
    
    if beautify:
        #gray_points[start_height:height, start_width:width,] = np.mean(image_numpy, axis=2)[start_height:height, start_width:width, None] #numba do not support axis for mean 
        #so use whay below
        #numba
        temp = np.sum(image_numpy, axis=2)[start_height:height, start_width:width,] / 3
        for i in range(3):
            gray_points[start_height:height, start_width:width, i] = temp
        #numba
    else:
        gray_points[start_height:height, start_width:width, ] = np.array([0.5, 0.5, 0.5])
  
    if cube:
        coordinates_x_y = np.where(
            (np.absolute(image_numpy - colour_point)) > radius/2
        )[0:2]
    else:
        coordinates_x_y = np.where(
            np.sum(np.power(image_numpy - colour_point, 2), axis=2) > np.power(radius, 2)
        )

    #image_numpy[coordinates_x_y] = gray_points[coordinates_x_y] # numba again do not support such indexis #if not kwargs["beautify"] else gray_points[coordinates_x_y]
    #so use what below
    #numba
    x_coor = coordinates_x_y[0]
    y_coor = coordinates_x_y[1]
    for i in range(x_coor.shape[0]):
        image_numpy[x_coor[i]][y_coor[i]] = gray_points[x_coor[i]][y_coor[i]]
    #numba
    
    return image_numpy