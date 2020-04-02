import cv2
import numpy as np
import sys
import os

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

def asciify(frame):
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = frame // 25
	frame = frame.tolist()
	text = [[ASCII_CHARS[px] for px in line[::10]] for line in frame[::10]]
	return text


if __name__ == '__main__':

	video = cv2.VideoCapture(sys.argv[1])

	width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = video.get(cv2.CAP_PROP_FPS)

	name, ext = os.path.splitext(sys.argv[1])

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	writer = cv2.VideoWriter('asciified-'+name+'.mp4', fourcc, fps, (width, height))

	print('Writing W*H {}x{}, FPS {}'.format(width, height, fps))


	while(video.isOpened()):
		ret, frame = video.read()

		if ret:
			text = asciify(frame)
			out = np.zeros((height, width, 3), np.uint8)
			for i in range(len(text)):
				for j in range(len(text[i])):
					cv2.putText(img=out,
						text=''.join(text[i][j]),
						org=(j*10, i*10),
						fontFace=1,
						fontScale=0.6,
						color=(255, 255, 255))

			writer.write(out)

			## TO CHECK RESULTS
			
			##cv2.imshow('test', out)

		else:
			break

	print('done')

	writer.release()
	video.release()
	cv2.waitKey(0)
	cv2.destroyAllWindows()