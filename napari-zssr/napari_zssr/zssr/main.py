import napari
from napari.utils.notifications import show_info
from napari_zssr.zssr.utils import show_message


def show_hello_message_from_main():
    show_info('Hello, world!')


def start_zssr():
    """
    this function is the main flow of zssr proccess.
    :return:
    """
    viewer = napari.viewer.current_viewer()
    if len(viewer.layers) == 0:
        show_message("error: can't start zssr proccess "
                     "please load png image!")
        return
    visible_layers = [layer for layer in viewer.layers if layer.visible]
    print(visible_layers)
