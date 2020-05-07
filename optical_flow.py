import numpy as np
import cv2

termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
feature_params = dict(maxCorners=200, qualityLevel=0.01, minDistance=7, blockSize=7)
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=termination)

class App:
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = cv2.VideoCapture(video_src)
        self.frame_idx = 0
        self.blackscreen = False
        self.width = int(self.cam.get(3))
        self.height = int(self.cam.get(4))

    def run(self):
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("[INFO] NOT FIND")
                break

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            vis = frame.copy()

            if self.blackscreen:
                vis = np.zeros((self.height, self.width, 3), np.uint8)

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0 - p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue

                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]

                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0, -1))

                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            self.frame_idx += 1
            self.prev_gray = frame_gray
            resize_img = cv2.resize(vis, dsize=(656, 368), interpolation=cv2.INTER_AREA)
            cv2.imshow('frame', resize_img)
            k = cv2.waitKey(30) & 0xFF
            if k == 27:
                break
            if k == ord('b'):
                self.blackscreen = not self.blackscreen
        self.cam.release()

video_src = '/home/ubuntu/kang_test/Realtime-Action-Recognition/data_test/falldown3.mp4'
# video_src = '/home/ubuntu/kang_test/cam1.avi'
App(video_src).run()
cv2.destroyAllWindows()

#
# import cv2
# import numpy as np
# cap = cv2.VideoCapture("/home/ubuntu/kang_test/cam1.avi")
#
# ret, frame1 = cap.read()
# prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
# hsv = np.zeros_like(frame1)
# hsv[...,1] = 255
#
# while(1):
#     ret, frame2 = cap.read()
#     next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
#
#     flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
#
#     mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
#     hsv[...,0] = ang*180/np.pi/2
#     hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
#     rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
#
#     cv2.imshow('frame2',rgb)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#     elif k == ord('s'):
#         cv2.imwrite('opticalfb.png',frame2)
#         cv2.imwrite('opticalhsv.png',rgb)
#     prvs = next
#
# cap.release()
# cv2.destroyAllWindows()