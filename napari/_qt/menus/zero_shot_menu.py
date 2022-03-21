from typing import TYPE_CHECKING
from itertools import chain
from typing import TYPE_CHECKING

from qtpy.QtCore import QSize
from qtpy.QtWidgets import QAction

from ...settings import get_settings
from ...utils.history import get_save_history, update_save_history
from ...utils.misc import running_as_bundled_app
from ...utils.translations import trans
from ..dialogs.preferences_dialog import PreferencesDialog
from ..dialogs.screenshot_dialog import ScreenshotDialog
from ._util import NapariMenu, populate_menu
from ...utils.translations import trans
from ..dialogs.qt_about import QtAbout
from ._util import NapariMenu, populate_menu

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
