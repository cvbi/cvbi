import scipy
import numpy as np
import scipy.ndimage
from scipy.fftpack import fft2, fftshift
from skimage.transform import resize

def get_image_angles(im, window_size = 13, window_overlap = 0.05, order_param_width = 2):


    # variables for analysis
    window_radius = int(np.floor(window_size/2))
    window_spacing = int(np.ceil(window_size*window_overlap))


    def gaussian_filter(shape, sigma):
        m,n = [(ss-1.)/2. for ss in shape]
        y,x = np.ogrid[-m:m+1,-n:n+1]
        h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
        h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h

    # create gaussian filter to remove edge effects on windows

    gauss_filter = gaussian_filter((window_size, window_size), window_size/4)

    # create a mask to apply during moment calculation
    r = 0.75 * window_radius  # arbitrary choice. Just needs to go to zero at the edges
    x, y = np.mgrid[-window_radius:window_radius+1, -window_radius:window_radius+1]
    # mask = x**2 + y**2 <= r**2
    mask = x**2 + y**2 <= r**2 + r + 1
    mask = mask.astype(float)

    # create coordinate grids for moment calculation
    y, x = np.mgrid[1:window_size+1, 1:window_size+1]

    # find coordinates of windows in image
    sz = im.shape
    grid_row = np.arange(window_radius+1, sz[0]-window_radius, window_spacing, dtype=int)
    grid_col = np.arange(window_radius+1, sz[1]-window_radius, window_spacing, dtype=int)
    number_rows = len(grid_row)
    number_cols = len(grid_col)

    angle_matrix = np.zeros((number_rows, number_cols))

    for i in grid_row:
        for j in grid_col:

            # store the local window of interest
            window = im[i-window_radius-1:i+window_radius, j-window_radius-1:j+window_radius]

            # take the fourier transform of the window and mask it
            window_fft = fftshift(fft2(window*gauss_filter))
            window_fft = np.real(np.sqrt(window_fft*np.conj(window_fft)))
            window_fft_masked = window_fft*mask

            # Calculate the various image moments
            M00 = np.sum(window_fft_masked)
            M10 = np.sum(window_fft_masked*x)
            M01 = np.sum(window_fft_masked*y)
            M11 = np.sum(window_fft_masked*x*y)
            M20 = np.sum(window_fft_masked*x*x)
            M02 = np.sum(window_fft_masked*y*y)

            # The Center of Mass
            xave = M10/M00
            yave = M01/M00

            # Calculate the central moments
            mu20 = M20/M00 - xave**2
            mu02 = M02/M00 - yave**2
            mu11 = M11/M00 - xave*yave

            # angle of axis of the least second moment
            theta = 0.5 * np.arctan(2 * mu11 / (mu20-mu02+1e-12))

            # Convert angle to proper orientation for my frame of reference
            if 0 < theta < (np.pi / 4):
                theta = np.pi/2 - theta
            if (-1 * np.pi / 4) < theta < 0:
                theta = -1 * theta

            # find points to do line scans to determine the maximum and minimum orientations
            x2 = xave - 1 + r * np.cos(theta)
            y2 = yave - 1 - r * np.sin(theta)

            x3 = xave - 1 - r * np.sin(theta)
            y3 = yave - 1 - r * np.cos(theta)

            # create points to interpolate along for linescans
            xline1, yline1 = np.linspace(xave-1, x2, r), np.linspace(yave-1, y2, r)
            xline2, yline2 = np.linspace(xave-1, x3, r), np.linspace(yave-1, y3, r)

            # Interpolate along those linescans
            line1 = scipy.ndimage.map_coordinates(np.transpose(np.log(window_fft)), np.vstack((xline1, yline1)))
            line2 = scipy.ndimage.map_coordinates(np.transpose(np.log(window_fft)), np.vstack((xline2, yline2)))

            # Determine which line is the maximum direction and correct theta
            if np.sum(line1) > np.sum(line2):
                maxline = line1
                minline = line2
                if x2 < xave:
                    theta = theta + np.pi/2
            else:
                maxline = line2
                minline = line1
                if x3 < xave:
                    theta = theta + np.pi/2

            # Store the theta value in a matrix
            angle_matrix[int(i/window_spacing - 1), int(j/window_spacing - 1)] = theta

    # order parameter matrix calculations
    order_matrix = np.zeros(angle_matrix.shape)
    for i in np.arange(order_param_width, order_matrix.shape[0]-order_param_width+1):
        for j in np.arange(order_param_width, order_matrix.shape[1]-order_param_width+1):
            # Create a matrix of the points of interest
            temp_matrix = angle_matrix[i-order_param_width:i+order_param_width+1, j-order_param_width:j+order_param_width+1]

            # Create a matrix of the same size filled with the central vector
            temp_angle_matrix = np.ones(temp_matrix.shape) * angle_matrix[i, j]

            # Calculate the order parameter as the square of the cosine between vectors
            compare_matrix = np.cos(temp_matrix-temp_angle_matrix) ** 2

            # Store the order parameters as the mean value of cos**2
            order_matrix[i, j] = np.mean(compare_matrix)

    # For plotting the figure with the vector directions overlaid
    X, Y = np.meshgrid(grid_col, grid_row)
    U = np.floor(window_radius/2.) * np.sin(angle_matrix)
    V = -1 * np.floor(window_radius/2.) * np.cos(angle_matrix)

    angle_out = resize(angle_matrix, im.shape)
    return(angle_out,X,Y,U,V)
