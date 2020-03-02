import cv2
import numpy as np

img = cv2.imread("bangla.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"Finding threshold"
th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

"Finding rectangle or bounding box"
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx,cy), (w,h), ang = ret

if w>h:
    w,h = h,w
    ang += 90

"Rotating image for alignment of box"
M = cv2.getRotationMatrix2D((cx,cy), 0, 1.0)
rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))
output = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))
BUFFER = 1
"""
def buffer_size(hist):
    size_buffer = []
    concurrent_minima = 0
    minimas = sorted(hist)
    i = 0
    minima = np.median(minimas)
    while i < len(hist):
        while i < len(hist) and hist[i] <= minima:
            concurrent_minima+=1
            i+=1
        if concurrent_minima != 0:
            size_buffer.append(concurrent_minima)
            concurrent_minima = 0
        i += 1
    return (int(np.median(size_buffer)), minima)
def bounds(hist, dim_init, dim_size):
    size_buf,threshold = buffer_size(hist)
    bound_limits = [0]
    for y in range(dim_init, dim_size-size_buf):
        if(hist[y]>threshold and (max([hist[val] for val in range(y+1, y+size_buf+1)], default=0)<=threshold)):
            bound_limits.append(y+BUFFER)
        elif(hist[y]<=threshold and (min([hist[val] for val in range(y+1, y+size_buf+1)], default=0)>threshold)):
            bound_limits.append(y-BUFFER)
    bound_limits = list(set(bound_limits))
    bound_limits.sort()
    return (threshold, size_buf, bound_limits)
"""
def words_seperator(lower, upper, cnt_lines):
    hist2 = cv2.reduce(rotated[upper:lower, :],0, cv2.REDUCE_AVG).reshape(-1)
    left = 0
    right = len(hist2)-1
    while hist2[left] <= min(hist2):
        left+=1
    while hist2[right] <= min(hist2):
        right-=1
    x = left
    prev_x = left
    cnt_words = 1
    while x < right:
        while x < len(hist2) and hist2[x] <= min(hist2):
            x += 1
        prev_x = x
        while x < len(hist2) and hist2[x] > min(hist2):
            x += 1
        if x - prev_x > 5:
            cv2.line(output, (prev_x,lower),(prev_x, upper), (255,0,0))
            cv2.line(output, (x,lower),(x, upper), (255,0,0))
            hist3 = cv2.reduce(rotated[upper-BUFFER:lower+BUFFER, prev_x-BUFFER:x+BUFFER],1, cv2.REDUCE_AVG).reshape(-1)
            letter_upper = 0
            letter_lower = len(hist3)-1
            while hist3[letter_upper] <= min(hist3):
                letter_upper+=1
            while hist3[letter_lower] <= min(hist3):
                letter_lower-=1
            cv2.imwrite("word/words_"+str(cnt_lines)+str(cnt_words)+".png", output2[upper+letter_upper-BUFFER:upper+letter_lower+BUFFER, prev_x-BUFFER:x+BUFFER])
            cnt_words += 1


def lines_seperator():
    hist2 = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)
    upper = 0
    lower = len(hist2)-1
    while hist2[upper] <= min(hist2):
        upper+=1
    while hist2[lower] <= min(hist2):
        lower-=1
    x = upper
    prev_x = upper
    cnt_lines = 1
    while x < lower:
        while x < len(hist2) and hist2[x] <= min(hist2):
            x += 1
        prev_x = x
        while x < len(hist2) and hist2[x] > min(hist2):
            x += 1
        if x - prev_x > 0:
            cv2.line(output, (0, x),(WIDTH, x), (0,255,0))
            cv2.line(output, (0, prev_x),(WIDTH, prev_x), (0,255,0))
            cv2.imwrite("line/lines_"+str(cnt_lines)+".png", output2[prev_x-BUFFER:x+BUFFER, :])
            words_seperator(x, prev_x, cnt_lines)
            cnt_lines += 1

"Drawing lines or seperation of lines"
hist = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)

HEIGHT, WIDTH = img.shape[:2]

output2 =cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
output = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)

lines_seperator()

"""for vals in line_bounds:
    cv2.line(output, (0,vals),(WIDTH, vals), (0,255,0))
"Generation of letters and saving of words in words directory"
prev_y = line_bounds[0]
cnt_lines = 1
cnt_letters = 1
for y in line_bounds[1:]:
    if (y - prev_y) > line_buffer:
        hist2 = cv2.reduce(rotated[prev_y:y, :], 0, cv2.REDUCE_AVG).reshape(-1)
        emp = max(hist2)
        if emp > 5:
            cv2.imwrite("line/lines_"+str(cnt_lines)+".png", output2[prev_y-BUFFER:y+BUFFER, :])
            words_seperator(y, prev_y, cnt_lines)
            cnt_lines += 1
    prev_y = y"""
import matplotlib.pyplot as plt

plt.imshow(output)
plt.show()

cv2.imwrite("result.png", output)