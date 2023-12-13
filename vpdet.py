import cv2 as cv
import numpy as np
from PIL import Image

''' RYENG NOTES
VPDET: CREATE CLASS VPDET
GIVEN: LINE_THRESH, PP, SEED, FOCAL_LEN 

METHOD:
1) DETECT LINES, STORE IN ARRAY
2) SET PP AS CENTER OF IMG
3) FIND VP CANDIDATES
4) MAP TO SPHERE
5) CLUSTER

DIVE: 
1) Line detect
    a) use opencv's lsd detector
    b) store the following info:
        i) point1, point2 (from lsd)
            note: also the cross product??
        j) dx, dy
        k) orientation (arctan2)
            normalize the orientations:
                [-pi, pi] -> [0, pi]

    note: line is given by <m,b>  (i think)

2) Set pp as img center (idky since it's given)
3) Find vp candidates:
    a) given pair of lines
    b) 

    src: https://imois.in/posts/line-intersections-with-cross-products/
         
'''

class vpdet():
    def __init__(self, img: Image.Image,  line_threshold : float, focal_len : float, principal_point : np.ndarray):
        # preprocess img
        self.img_pil = img # save raw img
        if (self.img_pil.mode != "L"): 
            self.img_pil_gs = self.img.convert('L') # save a grayscale copy
        self.img = np.array(self.img_pil_gs) # working copy

        # define other variables
        self.line_threshold = line_threshold # decides the lines chosen
        self.focal_len = focal_len 
        self.principal_point = principal_point
        self.lines = None 
        self.vps = np.array([[],[],[]]) # 3 vps per image

    def line_detection(self):
        lsd = cv.createLineSegmentDetector(0)
        lines_lsd = lsd.detect(self.img)[:,0]
        dx = lines_lsd[:,2] - lines_lsd[:,0]
        dy = lines_lsd[:,3] - lines_lsd[:,1]
        mag = np.sqrt(dx ** 2 + dy ** 2)
        lines = []
        for i in range(len(mag)):
            if mag < self.line_threshold:
                lines.append(lines_lsd[i])
        return lines

    def find_candidates(self):
        deg2rad = np.pi / 180
        line_amt = self.lines.shape[0]
        p1 = np.column_stack((self.lines[:, :2], np.ones(line_amt)))
        p2 = np.column_stack((self.lines[:, 2:], np.ones(line_amt)))
        cp = np.cross(p1,p2)
        dx = p1[:, 0] - p2[:, 0]
        dy = p1[:, 1] - p2[:, 1]
        mag = np.sqrt(dx ** 2 + dy ** 2)
        orientation = np.arctan2(dy, dx)
        candidates = np.zeros((105 * 360, 3, 3))
        for i in range(105):
            random1, random2 = np.random.permutation(line_amt)[:2]
            _vp1 = np.cross(cp[random1], cp[random2])

            vp1 = np.zeros(3)
            vp1[:2] = _vp1[:2] / _vp1[2] - self.principal_point
            vp1[2] = self.focal_len

            vp1 /= np.sqrt(np.sum(np.square(vp1)))
            lat = np.arange(360) * deg2rad
            long = np.arctan(-vp1[2] / (vp1[0] * np.sin(lat) + vp1[1] * np.cos(lat)))
            
            vp2 = np.column_stack([np.sin(long) * np.sin(lat), np.sin(long) * np.cos(lat), np.cos(long)])
            vp2 /= np.sqrt(np.sum(np.square(vp2), axis=1, keepdims=True))
            vp2[vp2[:, 2] < 0, :] *= -1.0

            vp3 = np.cross(vp1, vp2)
            vp3 /= np.sqrt(np.sum(np.square(vp3), axis=1, keepdims=True))
            vp3[vp3[:, 2] < 0, :] *= -1.0

            # add candidates
        
        return candidates
            
    def sphere_coords(self):
        
        return 1
    
    def get_best(self):


    def main(self, path):
        self.img = cv.imread(path)
        self.line_detection()
        candidates = self.find_candidates()
        sphere = self.sphere_coords()
        best = self.get_best()
        return best