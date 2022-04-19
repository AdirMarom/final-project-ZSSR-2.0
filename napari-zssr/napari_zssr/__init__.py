from napari.utils.notifications import show_info

#def show_hello_message():
#    show_info('Hello, world!')

#try:
#    from ._version import version as __version__
#except ImportError:
#    __version__ = "unknown"

from .zssr.call import napari_experimental_provide_dock_widget
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
