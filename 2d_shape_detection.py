import numpy as np
import cv2
from scipy.spatial import distance


def find_contours_and_corners(image):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    kernel = np.ones((4, 4), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    corners = cv2.goodFeaturesToTrack(image, 100, 0.01, 10)
    corners = np.int0(corners)
    for corner in corners:
        corner.ravel()
    return contours, corners


def count_corners(corners, x, y, w, h):
    result = 0
    for corner in corners:
        a, b = corner.ravel()
        if a in range(x, x + w + 1) and b in range(y, y + h + 1):
            result += 1
    return result


def template_processing(template_dir):
    template = cv2.imread(template_dir)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    blur_gray_template = cv2.GaussianBlur(gray_template, (3, 3), 0)  # remove Gaussian noise
    contours, corners = find_contours_and_corners(blur_gray_template)
    contours = np.squeeze(contours[1])
    contours_complex_list = []
    for contour in contours:
        contours_complex_list.append(complex(contour[0], contour[1]))
    # Fourier Transform
    contours_FFT = np.fft.fft(contours_complex_list, norm="ortho")
    f = abs(contours_FFT[1])
    after_trim = [i / f for i in contours_FFT[:trim_size]]  # scale invariance
    after_trim = [abs(i) for i in after_trim]  # rotation invariance
    after_trim = after_trim[1:]  # translation invariance
    return after_trim


trim_size = 100  # about 30% of the original contour length of templates
after_trim_C = template_processing('origin_c.jpg')
after_trim_2 = template_processing('origin_2.jpg')

img = cv2.imread('a4.bmp')
img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_gray_img = cv2.GaussianBlur(gray_img, (3, 3), 0)
contours_img, corners_img = find_contours_and_corners(blur_gray_img)
print("%d objects are found." % len(contours_img))

for contour_img in contours_img:
    if len(contour_img) > trim_size:
        contour_img = np.squeeze(contour_img)
        contour_img_complex = []
        for con_img in contour_img:
            contour_img_complex.append(complex(con_img[0], con_img[1]))
        contour_img_FFT = np.fft.fft(contour_img_complex)
        f_img = abs(contour_img_FFT[1])
        if f_img != 0:
            norm = [i / f_img for i in contour_img_FFT]  # divided by the first element, scale invariance
            norm = [abs(i) for i in norm]  # rotation invariance
            norm_len = len(norm)
            if norm_len >= trim_size:  # trim
                norm = norm[:trim_size]
            else:  # if length of template is larger than length of target, cut after_trim
                after_trim_C = after_trim_C[:norm_len]
                after_trim_2 = after_trim_2[:norm_len]
            norm = norm[1:]  # translation invariance

            # Calculate Euclidean distance
            distance_C = distance.euclidean(after_trim_C, norm)
            distance_2 = distance.euclidean(after_trim_2, norm)

            if distance_C < 0.3:
                x, y, w, h = cv2.boundingRect(contour_img)
                corner_C_number = count_corners(corners_img, x, y, w, h)
                if corner_C_number == 0:
                    cv2.drawContours(img, [np.array(contour_img)], 0, (0, 0, 255), 5)  # marked in red
            if distance_2 < 0.15:
                x, y, w, h = cv2.boundingRect(contour_img)
                corner_2_number = count_corners(corners_img, x, y, w, h)
                if 1 <= corner_2_number <= 2:
                    cv2.drawContours(img, [np.array(contour_img)], 0, (0, 255, 0), 5)  # marked in green

cv2.imwrite('a4_result.jpg', img)
print("Finish!")