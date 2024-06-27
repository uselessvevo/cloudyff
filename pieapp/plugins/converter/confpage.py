from __feature__ import snake_case

from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QFormLayout

from pieapp.api.gloader import Global
from pieapp.api.registries.models import Scope
from pieapp.api.models.plugins import SysPlugin
from pieapp.api.plugins.confpage import ConfigPage
from pieapp.api.registries.locales.helpers import translate
from pieapp.api.registries.themes.mixins import ThemeAccessorMixin
from pieapp.api.registries.configs.mixins import ConfigAccessorMixin


class ConverterConfigPage(
    ConfigPage,
    ConfigAccessorMixin,
    ThemeAccessorMixin
):
    name = SysPlugin.Converter

    def get_icon(self) -> "QIcon":
        return self.get_svg_icon("icons/app.svg", scope=self.name)

    def get_title(self) -> str:
        return translate("Converter")

    def get_page_widget(self) -> QWidget:
        return self._main_widget

    def init(self) -> None:
        self._main_widget = QWidget()
        main_form_layout = QFormLayout()

        self._ffmpeg_line_edit_action = QAction()
        self._ffmpeg_line_edit_action.set_icon(self.get_svg_icon("icons/folder.svg"))
        self._ffmpeg_line_edit_action.triggered.connect(self._ffmpeg_button_connect)

        self._ffmpeg_root = self.get_config("ffmpeg.root", Scope.User, Global.USER_ROOT / "ffmpeg")
        self._ffmpeg_line_edit = QLineEdit()
        self._ffmpeg_line_edit.set_object_name("PreferencesLineEdit")
        self._ffmpeg_line_edit.insert(self._ffmpeg_root)
        self._ffmpeg_line_edit.add_action(
            self._ffmpeg_line_edit_action,
            QLineEdit.ActionPosition.TrailingPosition
        )

        main_form_layout.add_row(translate("Converter binaries path"), self._ffmpeg_line_edit)
        self._main_widget.set_layout(main_form_layout)

    def _ffmpeg_button_connect(self) -> None:
        ffmpeg_directory = QFileDialog.get_existing_directory(
            parent=self._main_widget,
            caption=translate("Select ffmpeg directory"),
            dir=self._ffmpeg_root
        )
        directory_path = QDir.to_native_separators(ffmpeg_directory)

        if directory_path:
            self.update_config("ffmpeg.root", Scope.User, directory_path)
            directory_path_obj = Path(directory_path)
            binaries = list(map(Path, ("ffmpeg.exe", "ffprobe.exe", "ffplay.exe")))
            for binary in binaries:
                if not (directory_path_obj / binary).exists():
                    raise FileNotFoundError(
                        f"Binary file \"{binary.stem!s}\" not found. "
                        f"Please, download ffmpeg bundle from https://ffmpeg.org/download.html"
                    )

                self.update_config(f"ffmpeg.{binary.stem!s}", Scope.User, str(directory_path_obj / binary))

            self._ffmpeg_path = directory_path
            self._ffmpeg_line_edit.set_text(directory_path)
            self.set_modified(True)

    def accept(self) -> None:
        self.save_config()
        self.set_modified(False)

    def cancel(self) -> None:
        self.restore_config(Scope.User)
