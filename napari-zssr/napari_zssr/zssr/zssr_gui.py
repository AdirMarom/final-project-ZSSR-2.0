import os
from os import listdir
from typing import Any
from napari_plugin_engine import napari_hook_implementation
import time
from threading import Thread
from multiprocessing.pool import ThreadPool
import concurrent.futures
import numpy as np
import napari
from napari import Viewer
from napari.layers import Image, Shapes
from magicgui import magicgui
import PIL
from matplotlib import image
from napari.utils.notifications import show_info
from .conf import *


def read_logging(log_file, logwindow):
    with open(log_file, 'r') as thefile:
        # thefile.seek(0,2) # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.01)  # Sleep briefly
                continue
            else:
                logwindow.cursor.movePosition(logwindow.cursor.End)
                logwindow.cursor.insertText(line)
                yield line


def watch_file(filename, time_limit, check_interval):
    now = time.time()
    last_time = now + time_limit
    while time.time() <= last_time:
        if os.path.exists(filename):
            return True
        else:
            # Wait for check interval seconds, then check again.
            time.sleep(check_interval)

    return False


def create_new_file(command, pic_name):
    pic_name = pic_name.replace(".png", "")
    sbatch_file_path = CURRENT_FOLER_PATH + os.sep + 'sbatch_gpu1.example'
    with open(sbatch_file_path, "r") as old_file:
        with open(pic_name, "w") as newfile:
            for line in old_file:
                newfile.write(line)
            newfile.write("\n")
            newfile.write(command)
    return pic_name


def widget_wrapper():
    from napari.qt.threading import thread_worker
    @magicgui(
        call_button='run "Zero-Shot" Super-Resolution ',
        layout='vertical',
        label_line_2=dict(widget_type='Label', label='            Zero Shot Super Resolution for microscopic images'),
        label_line_3=dict(widget_type='Label', label='            Ben Gurion University of the Negev'),
        model_type=dict(widget_type='ComboBox', label='model type', choices=['zssr', ''],
                        value='zssr',
                        tooltip='there is a <em>cyto</em> model, a new <em>cyto2</em> model from user submissions, and a <em>nuclei</em> model'),
        file_dir=dict(widget_type='FileEdit', label='select 2D image: ',
                      tooltip='specify file path to it here', mode='d'),
        flag_label=dict(widget_type='Label', label='              Set ZSSR configurations '),
        zssr_flag_X4=dict(widget_type='CheckBox', text=' Estimate the X4 kernel'),
        zssr_flag_SR=dict(widget_type='CheckBox', text='Perform ZSSR using the estimated kernel'),
        zssr_flag_REAL=dict(widget_type='CheckBox', text='Real-image configuration (effects only the ZSSR)'),
    )
    def widget(  # label_logo,
            label_line_2,
            label_line_3,
            viewer: Viewer,
            image_layer: Image,
            model_type,
            file_dir,
            flag_label,
            zssr_flag_X4,
            zssr_flag_SR,
            zssr_flag_REAL
    ) -> None:

        zssr_run_path = ZSSR_RUN_PATH
        command = "python " + zssr_run_path + " --input-dir "
        if file_dir != ".":  # if path given - run ZSSR with chosen flags
            command += str(file_dir) + " "
            if zssr_flag_SR:
                command += "--SR "
            if zssr_flag_REAL:
                command += "--real "
            if zssr_flag_X4:
                command += "--X4 "
            output_path = ZSSR_RESULTS_PATH
            command += "--output-dir " + output_path
            show_info('ZSSR is started, please wait...')
            pic_name = listdir(file_dir)[0]
            if IN_CSE_LABS:
                new_file_to_run = create_new_file(command, pic_name)
                print("new file to run is: ")
                print(str(new_file_to_run))
                run_status = os.system("sbatch " + str(new_file_to_run))
            else:
                run_status = os.system(command)
            print("pic name is: ")
            tmp_pic_name = pic_name.replace(".png", "")
            print(str(tmp_pic_name))
            path_to_check_if_exists = output_path + os.sep + str(tmp_pic_name) + "/ZSSR_" + pic_name
            print("the path you are checking is:" + str(path_to_check_if_exists))
            print('run status is: ' + str(run_status))
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(watch_file, path_to_check_if_exists, 3600, 60)
                return_value = future.result()
                if return_value:
                    print("The path exists")
                    viewer = napari.viewer.current_viewer()
                    viewer.open(path_to_check_if_exists)

    return widget


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return widget_wrapper, {'name': 'cellpose'}
