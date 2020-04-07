# coding: utf-8

import json
import os
import os.path
import supervisely_lib as sly

import numpy as np
from numpy import random
import skimage as ski
from skimage import io

AXIS = 'axis'
SIZE = 'size'
MODE = 'mode'
OVERLAP = 'overlap'
NUMBER_SAMPLE = 'n_sample'

DEFAULT_AXIS = [0]
DEFAULT_SIZE = [256, 256]
DEFAULT_MODE = 'sliding_window'
DEFAULT_OVERLAP = 10
DEFAULT_N_SAMPLE = 100

# Do NOT use directly for video extension validation. Use is_valid_ext() /  has_valid_ext() below instead.
ALLOWED_CT_EXTENSION = ['.tiff']

def is_valid_ext(ext: str) -> bool:
    return ext.lower() in ALLOWED_CT_EXTENSION

def has_valid_ext(path: str) -> bool:
    return is_valid_ext(os.path.splitext(path)[1])

def sliding_window(im, size, overlap, axes):
    shape = list(im.shape)

    ls_im = []

    for axis in axes:
        t_shape = shape.copy()
        t_shape.pop(axis)
        for i in range(shape[axis]):
            sub_im = np.take(im, i, axis)

            for j in range(0, t_shape[0], size[0] - overlap):
                for k in range(0, t_shape[1], size[1] - overlap):
                    ss_im = sub_im[j:j+size[0], k:k+size[1]]
                    ls_im.append(ss_im)
    
    return ls_im

def random_sampling(im, size, number, axes, seed = None):
    if(seed is not None):
        random.seed(seed)
    
    ls_im = []

    shape = list(im.shape)

    for _ in number:
        axis = random.choice(axes)
        t_shape = shape.copy()
        t_shape.pop(axis)

        i = random.randint(0, im.shape[axis])
        j = random.randint(0, t_shape[0] - size[0])
        k = random.randint(0, t_shape[1] - size[1])

        sub_im = np.take(im, i, axis)[j:j+size[0], k:k+size[1]]
        ls_im.append(sub_im)
    
    return ls_im

def convert_ct_im():
    task_settings = json.load(open(sly.TaskPaths.TASK_CONFIG_PATH, 'r'))

    convert_options = task_settings['options']

    mode = convert_options.get(MODE)
    if mode is not None:
        mode = str(mode)
    else:
        sly.logger.warning('axis parameter not found. set to default: {}'.format(DEFAULT_MODE))
        mode = DEFAULT_MODE

    axis = set(convert_options.get(AXIS, DEFAULT_AXIS))
    size = set(convert_options.get(SIZE, DEFAULT_SIZE))

    paths = sly.fs.list_files(sly.TaskPaths.DATA_DIR)
    tiff_paths = []
    for path in paths:
        if has_valid_ext(path):
            tiff_paths.append(path)
        else:
            sly.logger.warning("CT file '{}' has unsupported extension. Skipped. Supported extensions: {}"
                               .format(path, ALLOWED_CT_EXTENSION))

    if len(tiff_paths) == 0:
        raise RuntimeError("Image not found!")

    project_dir = os.path.join(sly.TaskPaths.RESULTS_DIR, task_settings['res_names']['project'])
    project = sly.Project(directory=project_dir, mode=sly.OpenMode.CREATE)
    for im_path in tiff_paths:
        try:
            video_relpath = os.path.relpath(im_path, sly.TaskPaths.DATA_DIR)
            ds_name = video_relpath.replace('/', '__')
            ds = project.create_dataset(ds_name=ds_name)

            raw_image = io.imread(im_path) 

            if(mode == 'sliding_window'):
                overlap = convert_options.get(OVERLAP, DEFAULT_OVERLAP)
                ls_im = sliding_window(raw_image, size, overlap, axis)
            elif(mode == 'random'):
                number_sample = convert_options.get(NUMBER_SAMPLE, DEFAULT_N_SAMPLE)
                ls_im = random_sampling(raw_image, size, number_sample, axis)
            else:
                raise RuntimeError("mode not implemented")

            progress = sly.Progress('Import image: {}'.format(ds_name), len(ls_im))
            for frame_id, image in enumerate(ls_im):
                img_name = "frame_{:05d}".format(frame_id)
                ds.add_item_np(img_name + '.png', image)
                progress.iter_done_report()

        except Exception as e:
            exc_str = str(e)
            sly.logger.warn('Input tiff skipped due to error: {}'.format(exc_str), exc_info=True, extra={
                'exc_str': exc_str,
                'video_file': im_path,
            })


def main():
    convert_ct_im()
    sly.report_import_finished()


if __name__ == '__main__':
    sly.main_wrapper('VIDEO_ONLY_IMPORT', main)