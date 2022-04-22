import os
from typing import Any
from napari_plugin_engine import napari_hook_implementation
import time
import numpy as np

from napari import Viewer
from napari.layers import Image, Shapes
from magicgui import magicgui


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

# logo = os.path.join(__file__, 'logo/logo_small.png')



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
        custom_model=dict(widget_type='FileEdit', label='select 2D image: ',
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
            custom_model,
            flag_label,
            zssr_flag_X4,
            zssr_flag_SR,
            zssr_flag_REAL
    ) -> None:
        # Import when users activate plugin
        #if not hasattr(widget, 'cellpose_layers'):
        #    widget.cellpose_layers = []
       ## print(widget.zssr_flag_REAL.value)
        #image = image_layer.data
        ## put channels last
        #widget.n_channels = 0
        #widget.channel_axis = None
        #if image_layer.ndim == 4 and not image_layer.rgb:
        #    chan = np.nonzero([a == 'c' for a in viewer.dims.axis_labels])[0]
        #    if len(chan) > 0:
        #        chan = chan[0]
        #        widget.channel_axis = chan
        #        widget.n_channels = image.shape[chan]
        #elif image_layer.ndim == 3 and not image_layer.rgb:
        #    image = image[:, :, :, np.newaxis]
        #elif image_layer.rgb:
        #    widget.channel_axis = -1
        zssr_run_path = "C:\\Users\\dorle\\PycharmProjects\\final-project-ZSSR-2.0\\ZSSR\KernelGAN-master\\train.py "
        command = "python " + zssr_run_path +"--input-dir "
        if custom_model: #if path given - run ZSSR with chosen flags
            command += str(custom_model) + " "
            if zssr_flag_SR:
                command +="--SR "
            if zssr_flag_REAL:
                command +="--real "
            if zssr_flag_X4:
                command +="--x4"
            print(command)
            #os.system(command)



    return widget


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return widget_wrapper, {'name': 'cellpose'}
