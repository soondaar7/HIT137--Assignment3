# logic/image_processor.py

import cv2
import numpy as np
import random
from PIL import Image


class ImageProcessor:
    """
    Handles cloning an image and applying 5 hidden differences.
    Each difference is a rectangular region with a subtle visual change.
    """

    DIFFERENCE_SIZE = 40  # Each difference patch is 40x40 pixels
    NUM_DIFFERENCES = 5  # Total number of differences to hide
    MIN_GAP = 50  # Minimum pixel gap between difference centres

    def __init__(self):
        ######### List of (x, y, w, h) tuples (canvas coords) ##########
        self.difference_coords = []

    ########## PUBLIC API  (called by the Integrator / main.py) ##########

    def create_modified_image(self, pil_image: Image.Image):
        """
        Takes a PIL Image (already resized to 350x350 by the GUI),
        applies 5 non-overlapping subtle differences, and returns:
          - modified PIL Image  (to display on the right canvas)
          - list of (x, y, w, h) tuples  (for Student C's click detection)
        """
        ####### PIL → OpenCV (BGR) #######
        cv_image = self._pil_to_cv(pil_image)
        modified = cv_image.copy()

        self.difference_coords = []
        attempts = 0

        while len(self.difference_coords) < self.NUM_DIFFERENCES and attempts < 1000:
            attempts += 1
            x, y = self._random_position(cv_image.shape)
            w = h = self.DIFFERENCE_SIZE

            if not self._overlaps(x, y, w, h):
                self._apply_difference(modified, x, y, w, h)
                self.difference_coords.append((x, y, w, h))

        ###### OpenCV → PIL #####
        modified_pil = self._cv_to_pil(modified)
        return modified_pil, self.difference_coords

    def get_difference_coords(self):
        """Returns the list of difference rectangles from the last call."""
        return self.difference_coords

    def _random_position(self, shape):
        """Pick a random top-left (x, y) so the patch fits within the image."""
        h_img, w_img = shape[:2]
        x = random.randint(10, w_img - self.DIFFERENCE_SIZE - 10)
        y = random.randint(10, h_img - self.DIFFERENCE_SIZE - 10)
        return x, y

    def _overlaps(self, x, y, w, h):
        """Return True if this rectangle is too close to an existing difference."""
        for (ex, ey, ew, eh) in self.difference_coords:
            if (abs(x - ex) < w + self.MIN_GAP and
                    abs(y - ey) < h + self.MIN_GAP):
                return True
        return False

    def _apply_difference(self, cv_img, x, y, w, h):
        """
        Randomly pick one of 4 subtle difference types and apply in-place.
        Types: subtle colour tint, brightness shift, blur patch, hue rotation.
        All changes are noticeable upon careful inspection but not glaringly obvious.
        """
        diff_type = random.randint(0, 3)

        if diff_type == 0:
            # Subtle colour tint — blend a random colour at 25% opacity
            patch = cv_img[y:y+h, x:x+w].astype(np.float32)
            tint = np.full_like(patch, [random.randint(0, 255)
                                for _ in range(3)], dtype=np.float32)
            blended = cv2.addWeighted(patch, 0.75, tint, 0.25, 0)
            cv_img[y:y+h, x:x+w] = blended.astype(np.uint8)

        elif diff_type == 1:
            ######### Subtle brightness shift (±30 — noticeable but not glaring) #########
            patch = cv_img[y:y+h, x:x+w].astype(np.int16)
            shift = random.choice([-30, 30])
            patch = np.clip(patch + shift, 0, 255).astype(np.uint8)
            cv_img[y:y+h, x:x+w] = patch

        elif diff_type == 2:
            ######### Moderate gaussian blur #########
            blurred = cv2.GaussianBlur(cv_img[y:y+h, x:x+w], (11, 11), 0)
            cv_img[y:y+h, x:x+w] = blurred

        else:
            ######### Subtle hue rotation (+30 degrees in HSV space) #########
            patch_bgr = cv_img[y:y+h, x:x+w].copy()
            patch_hsv = cv2.cvtColor(
                patch_bgr, cv2.COLOR_BGR2HSV).astype(np.int16)
            patch_hsv[:, :, 0] = (patch_hsv[:, :, 0] + 30) % 180
            patch_hsv = patch_hsv.astype(np.uint8)
            cv_img[y:y+h, x:x+w] = cv2.cvtColor(patch_hsv, cv2.COLOR_HSV2BGR)

    @staticmethod
    def _pil_to_cv(pil_image: Image.Image):
        """Convert PIL RGB image to OpenCV BGR numpy array."""
        rgb = np.array(pil_image.convert("RGB"))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    @staticmethod
    def _cv_to_pil(cv_img) -> Image.Image:
        """Convert OpenCV BGR array to PIL RGB image."""
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)
