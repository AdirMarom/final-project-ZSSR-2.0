import warnings
from pathlib import Path
from typing import Optional, List, Callable, Sequence, Union
import napari
from napari import viewer
from skimage import data
from napari.types import PathOrPaths, ReaderFunction, LayerData
from napari.utils.notifications import show_info
from napari_plugin_engine import napari_hook_implementation

# example_plugin.some_module
PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]


def _ensure_str_or_seq_str(path):
    if isinstance(path, Path) or (
            isinstance(path, (list, tuple)) and any([isinstance(p, Path) for p in path])
    ):
        warnings.warn(
            "Npe2 receive a `Path` or a list of `Path`s, instead of `str`,"
            " this will  become an error in the future and is likely a"
            " napari bug. Please fill and issue.",
            UserWarning,
            stacklevel=3,
        )


ReaderFunction = Callable[[PathOrPaths], List[LayerData]]


def get_reader(path: PathOrPaths) -> Optional[ReaderFunction]:
    # If we recognize the format, we return the actual reader function
    if isinstance(path, str) and path.endswith(".png"):
        return xyz_file_reader
    # otherwise we return None.
    return None


def xyz_file_reader(path: PathOrPaths) -> List[LayerData]:
    viewer = napari.viewer.current_viewer()
    viewer.add_image(data.astronaut(), name='astronaut')
    viewer.add_image(data.moon(), name='moon')
    viewer.add_image(data.camera(), name='camera')
    print(viewer.layers)
    layer_attributes = {"name": "etc..."}
    return [(data, layer_attributes)]


def show_message(massage: str):
    try:
        show_info(massage)
    except Exception as e:
        print(str(e))
