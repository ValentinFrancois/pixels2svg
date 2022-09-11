import os

from examples.base import (BRAIN_OVERLAY_PNG_PATH, BRAIN_PNG_PATH, IMAGES_DIR,
                           SWORD_PNG_PATH)

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = os.path.join(TEST_DIR, 'fixtures')

IMAGE_CONSTANTS = (IMAGES_DIR,
                   BRAIN_OVERLAY_PNG_PATH,
                   BRAIN_PNG_PATH,
                   SWORD_PNG_PATH)
