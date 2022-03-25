from typing import TYPE_CHECKING

from ...utils.translations import trans
from ._util import NapariMenu, populate_menu

##

from .. import qt_viewer
##
if TYPE_CHECKING:
    from ..qt_main_window import Window

try:
    from napari_error_reporter import ask_opt_in
except ImportError:
    ask_opt_in = None


class zeroShotMenu(NapariMenu):
    def __init__(self, window: 'Window'):
        super().__init__(trans._('&zeroShotMenu'), window._qt_window)
        ACTIONS = [
            {
                'text': trans._('Open File(s)...'),
                'slot': window._qt_viewer._open_files_dialog,
                'shortcut': 'Ctrl+O',
            },
            {
                'text': trans._('Save Selected Layer(s)...'),
                'slot': lambda: window._qt_viewer._save_layers_dialog(
                    selected=True
                ),
                'shortcut': 'Ctrl+S',
            },
            {
                'text': trans._('Save All Layers...'),
                'slot': lambda: window._qt_viewer._save_layers_dialog(
                    selected=False
                ),
                'shortcut': 'Ctrl+Shift+S',
            }

        ]
        if ask_opt_in is not None:
            ACTIONS.append(
                {
                    'text': trans._('Bug reporting opt in/out...'),
                    'slot': lambda: ask_opt_in(force=True),
                }
            )

        populate_menu(self, ACTIONS)
