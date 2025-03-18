import cv2 as cv
import numpy as np

video = cv.VideoCapture(0)

if not video.isOpened():
    exit()

fps = video.get(cv.CAP_PROP_FPS)
wait_msec = int(1000 / fps)

fourcc = cv.VideoWriter_fourcc(*'XVID') 
frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH)) * 2
frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

def concat_fft(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    dft = cv.dft(np.float32(gray), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude = cv.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
    magnitude = np.log1p(magnitude)

    magnitude = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)
    magnitude = np.uint8(magnitude)

    magnitude = cv.cvtColor(magnitude, cv.COLOR_GRAY2BGR)

    return np.hstack((img, magnitude))

runnable = True

while runnable:
    while runnable:
        runnable, img = video.read()
        if not runnable:
            break

        img = concat_fft(img)
        cv.imshow('Video Player', img)

        key = cv.waitKey(wait_msec)
        if key == 27:
            runnable = False
            break
        elif key == ord(' '):
            break

    video_writer = cv.VideoWriter('name.avi', fourcc, fps, (frame_width, frame_height))
    while runnable:
        runnable, img = video.read()
        if not runnable:
            break

        img = concat_fft(img)
        video_writer.write(img)
        
        img[:frame_height//20, :frame_width//20, :] = (0, 0, 255)
        cv.imshow('Video Player', img)

        key = cv.waitKey(wait_msec)
        if key == 27:
            runnable = False
            break
        elif key == ord(' '):
            break
    video_writer.release()

video.release()
cv.destroyAllWindows()
