import cv2
import numpy as np
from utils import eprint, create_directory_if_not_exists, file_exists, absolute_path, basename, get_env, boolean
from time import time
from math import trunc, pi, atan
from subprocess import Popen, PIPE

_DEBUG = boolean(get_env('DEBUG', 'False'))
_EXIFTOOL = get_env('EXIFTOOL', 'd:\\dev\\strawberry-perl\\perl\\site\\bin\\exiftool.bat')


# Module function: stitch multiple images into single panorama view and upload it servers.
def process_images(images: [np.ndarray], hfov: float) -> (bool, str):
    # stitch image
    succeeded, pano = stitch_images(images)
    if not succeeded:
        return (False, None)
    if pano is None:
        eprint('[{}]: Stitched image is null'.format(basename(__file__)))
        return (False, None)

    # save image to local storage
    result_dir = 'results'
    create_directory_if_not_exists(result_dir)
    result_filename = '{}/pano-{}.jpg'.format(result_dir, trunc(time()))
    cv2.imwrite(result_filename, pano)

    # add gpano metadata to image
    if not update_gpano_metadata(result_filename, hfov):
        eprint('[{}]: Fail to update GPano metadata of result image file'.format(basename(__file__)))
        return (False, None)

    # upload image
    if not upload_image_to_facebook(result_filename):
        eprint('[{}]: Fail to upload result image'.format(basename(__file__)))
        return (False, result_filename)

    return (True, result_filename)


# Sub function: stitch multiple images into single panorama view
def stitch_images(images: [np.ndarray]) -> (bool, np.ndarray):
    assert len(images) > 1

    stitcher = cv2.createStitcher(False)
    retval, pano = stitcher.stitch(images)
    if retval != cv2.STITCHER_OK:
        eprint('[{}]: Can not stitch images'.format(basename(__file__)))
        return (False, None)
    return (True, pano)


# Sub function: compute and add/update GPano metadata to image file
def update_gpano_metadata(filename: str, hfov: float) -> bool:
    absolute_filename = absolute_path(filename)
    assert file_exists(absolute_filename)

    image: np.ndarray = cv2.imread(absolute_filename)
    (full_pano_width, full_pano_height,
     cropped_area_left, cropped_area_top,
     cropped_area_width, cropped_area_height) = compute_gpano_cylindrical_metadata(image, hfov)

    proc = Popen([_EXIFTOOL,
                  '-overwrite_original',
                  '-FullPanoWidthPixels={}'.format(full_pano_width),
                  '-FullPanoHeightPixels={}'.format(full_pano_height),
                  '-CroppedAreaLeftPixels={}'.format(cropped_area_left),
                  '-CroppedAreaTopPixels={}'.format(cropped_area_top),
                  '-CroppedAreaImageWidthPixels={}'.format(cropped_area_width),
                  '-CroppedAreaImageHeightPixels={}'.format(cropped_area_height),
                  '-ProjectionType=cylindrical',
                  absolute_filename], stdout=PIPE, stderr=PIPE)

    if _DEBUG:
        print('[{}]: Update metadata command: {}'.format(basename(__file__), ' '.join(proc.args)))

    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        return True
    eprint('[{}]: Update GPano metadata failed'.format(basename(__file__)))
    eprint(stderr.decode('utf-8'))
    return False


# Sub function: compute GPano metadata for cylindrical projection using image size and horizontal field of view
# return (FullPanoWidthPixels, FullPanoHeightPixels, CroppedAreaLeftPixels, CroppedAreaTopPixels, CroppedAreaImageWidthPixels, CroppedAreaImageHeightPixels)
def compute_gpano_cylindrical_metadata(image: np.ndarray, hfov: float) -> (int, int, int, int, int, int):
    assert hfov > 0 and hfov <= 360

    image_width = image.shape[1]
    image_height = image.shape[0]
    assert image_width > 0 and image_height > 0

    theta = (hfov * pi) / 180  # camera angle, projection angle in sphere center (in radian)
    l = image_width  # max x (right most, left most is 0) in mapped coordinates (image coordinates)
    r = l / theta  # radius of sphere
    y = image_height / 2  # max y (top most, center is 0, bottom most is -y) of mapped coordinates
    fi = atan(y / r)  # latitude of mapped y in sphere
    L = (l * 2 * pi) / theta  # width of sphere surface unrolled to a rectangle 2:1 (full pano)
    H = L / 2  # height of sphere unrolled to a rectangle 2:1 (full pano)
    Y = (fi * H) / pi  # mapped y in rectangle 2:1 unrolled from sphere
    h = Y * 2  # height of mapped coordinates rectangle 2:1 unrolled from sphere

    full_pano_width = int(round(L))
    full_pano_height = int(round(H))
    cropped_area_width = int(round(l))
    cropped_area_height = int(round(h))
    cropped_area_left = int(round((full_pano_width - cropped_area_width) / 2))  # center panorama in 360 horizontal view
    cropped_area_top = 0  # cylindrical panorama get no effect of cropped top pixels, it is always displayed in the center

    return (full_pano_width, full_pano_height,
            cropped_area_left, cropped_area_top,
            cropped_area_width, cropped_area_height)


# Sub function: upload processed image to servers
def upload_image_to_facebook(filename: str) -> bool:
    eprint(
        '[{}]: Can not upload image to Facebook at that time because Facebook is current blocking this feature'.format(
            basename(__file__)))
    eprint(
        '[{}]: Please manually upload using result image at "{}"'.format(basename(__file__), absolute_path(filename)))
    return True
