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
        Applies subtle differences with 'Feathered Edges' to hide the square shape.
        """
        # 1. Capture the original patch
        patch = cv_img[y:y+h, x:x+w].copy()
        diff_type = random.randint(0, 3)

        # 2. Create the modified version of the patch
        if diff_type == 0:
            # Color Tint - Reduced to 15% for subtlety
            tint = np.full_like(patch, [random.randint(0, 255) for _ in range(3)])
            modified_patch = cv2.addWeighted(patch, 0.85, tint, 0.15, 0)

        elif diff_type == 1:
            # Brightness Shift (+/- 25)
            temp = patch.astype(np.int16)
            shift = random.choice([-25, 25])
            modified_patch = np.clip(temp + shift, 0, 255).astype(np.uint8)

        elif diff_type == 2:
            # Gaussian Blur (11x11 is a good balance)
            modified_patch = cv2.GaussianBlur(patch, (11, 11), 0)

        else:
            # Hue Rotation (18 degrees)
            patch_hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV).astype(np.int16)
            patch_hsv[:, :, 0] = (patch_hsv[:, :, 0] + 18) % 180
            modified_patch = cv2.cvtColor(patch_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

        # 3.Create a soft-edged mask
        # This makes the square transition 'fade' into the image
        mask = np.zeros((h, w), dtype=np.float32)
        # Draw a white rectangle slightly inside the patch
        cv2.rectangle(mask, (3, 3), (w-3, h-3), 1.0, -1)
        # Blur the mask to create the 'feathered' effect
        mask = cv2.GaussianBlur(mask, (15, 15), 0)

        # 4. Blend the modified patch back into the image using the mask
        for c in range(3): # Loop through Blue, Green, Red channels
            cv_img[y:y+h, x:x+w, c] = (mask * modified_patch[:, :, c] + 
                                      (1 - mask) * cv_img[y:y+h, x:x+w, c])

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
