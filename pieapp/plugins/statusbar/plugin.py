from __feature__ import snake_case

from typing import Union

from PySide6.QtWidgets import QStatusBar, QWidget

from pieapp.structs.plugins import Plugin
from piekit.plugins.plugins import PiePlugin
from piekit.managers.themes.mixins import ThemeAccessorMixin
from piekit.managers.configs.mixins import ConfigAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin


class StatusBar(
    PiePlugin,
    ConfigAccessorMixin, LocalesAccessorMixin, ThemeAccessorMixin,
):
    name = Plugin.StatusBar

    def show_message(self, message: str) -> None:
        self.status_bar.show_message(message)

    def init(self) -> None:
        self.status_bar = QStatusBar(self._parent)
        self.status_bar.insert_permanent_widget(0, QWidget())
        self._parent.set_status_bar(self.status_bar)
        self._parent.sig_plugin_ready.connect(lambda _: self.show_message(self.translate("Plugins are ready")))

    showMessage = show_message


def main(parent: "QMainWindow", plugin_path: "Path"):
    return StatusBar(parent, plugin_path)