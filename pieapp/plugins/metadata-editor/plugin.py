from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from __feature__ import snake_case

from typing import Union

from pieapp.structs.plugins import Plugin
from piekit.plugins.plugins import PiePlugin
from piekit.plugins.utils import get_plugin
from piekit.managers.assets.mixins import AssetsAccessorMixin
from piekit.managers.locales.mixins import LocalesAccessorMixin
from piekit.managers.plugins.decorators import on_plugin_event


class MetadataEditor(
    PiePlugin, LocalesAccessorMixin, AssetsAccessorMixin
):
    name = Plugin.MetadataEditor
    requires = [Plugin.Converter]

    @on_plugin_event(target=Plugin.Converter, event="converter_table_ready")
    def on_converter_table_ready(self) -> None:
        self._converter = get_plugin(Plugin.Converter)
        self._converter.add_side_menu_item(
            name="edit",
            text=self.get_translation("Edit"),
            icon=self.get_svg_icon("refresh.svg"),
            callback=self._edit_toolbutton_connect
        )

    def _edit_toolbutton_connect(self) -> None:
        pass


def main(parent: "QMainWindow", plugin_path: "Path") -> Union[PiePlugin, None]:
    return MetadataEditor(parent, plugin_path)