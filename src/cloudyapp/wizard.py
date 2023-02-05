import os
from PyQt5 import QtWidgets

from cloudykit.system import System
from cloudykit.utils.core import restartApplication
from cloudykit.utils.files import writeJson


class LocaleWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self._parent = parent
        self._locales = System.config.LOCALES
        self._curLocale = System.config.DEFAULT_LOCALE
        self._localesRev = {v: k for (k, v) in self._locales.items()}
        self._curLocaleRev = self._locales.get(self._curLocale)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet("QComboBox{font-size: 12pt;}")
        self.comboBox.insertItem(0, self._locales.pop(self._curLocale))
        self.comboBox.addItems([self._locales.get(i) for (i, _) in self._locales.items()])
        self.comboBox.currentIndexChanged.connect(self.getResult)

        self.localeLabel = QtWidgets.QLabel(System.registry.locales("shared", "Select locale"))
        self.localeLabel.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.localeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        newLocale = self._localesRev.get(self.comboBox.currentText())
        writeJson(
            file=str(System.user_root / System.config.USER_CONFIG_FOLDER / "locales.json"),
            data={"locale": newLocale},
            create=True
        )

        if self._curLocale != newLocale:
            restartApplication()

        return newLocale


class ThemeWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setStyleSheet("QComboBox{font-size: 12pt;}")
        self.comboBox.addItems(System.registry.assets.themes)
        self.comboBox.currentIndexChanged.connect(self.getResult)

        self._curTheme = System.registry.configs.get(
            "user", "assets.theme", default=System.registry.assets.theme
        )

        themeLabel = QtWidgets.QLabel(System.registry.locales("shared", "Select theme"))
        themeLabel.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(themeLabel)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)

    def getResult(self):
        newTheme = self.comboBox.currentText()
        writeJson(
            file=str(System.user_root / System.config.USER_CONFIG_FOLDER / "assets.json"),
            data={"theme": newTheme},
            create=True
        )

        if self._curTheme != newTheme:
            restartApplication()

        return self.comboBox.currentText()


class FfmpegWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._parent = parent
        ffmpegPath = System.registry.configs.get("ffmpeg.ffmpeg_path")

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setDisabled(True)
        self.lineEdit.setStyleSheet("QLineEdit{font-size: 15pt;}")

        self.lineEditButton = QtWidgets.QToolButton()
        self.lineEditButton.setStyleSheet("""
            QPushButton{
            font-size: 15pt;
                width: 300px;
                border-radius: 50px;
            }
        """)
        self.lineEditButton.setText(">")
        self.lineEditButton.clicked.connect(self.selectFfmpegPath)

        localeLabel = QtWidgets.QLabel("Setup ffmpeg")
        localeLabel.setStyleSheet("QLabel{font-size: 25pt; padding-bottom: 20px;}")

        ffmpegHBox = QtWidgets.QHBoxLayout()
        ffmpegHBox.addWidget(self.lineEditButton)
        ffmpegHBox.addWidget(self.lineEdit)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(localeLabel)
        layout.addLayout(ffmpegHBox)
        self.setLayout(layout)

        parent.button(QtWidgets.QWizard.NextButton).clicked.connect(self.checkFfmpegPath)

    def checkFfmpegPath(self):
        pass

    def selectFfmpegPath(self):
        fileDialog = QtWidgets.QFileDialog().getOpenFileName(
            self._parent,
            directory=os.path.expanduser("~")
        )
        if fileDialog:
            print(fileDialog)

    def getResult(self):
        return self.lineEdit.text()


class FinishWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent) -> None:
        super().__init__(parent)


class SetupWizard(QtWidgets.QWizard):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        if not System.user_root.exists():
            System.user_root.mkdir()
            (System.user_root / System.config.USER_CONFIG_FOLDER).mkdir()
            (System.user_root / System.config.USER_PLUGINS_FOLDER).mkdir()

        self.setWindowTitle("Setup wizard")
        self.resize(640, 380)
        self.setOptions(
            QtWidgets.QWizard.NoBackButtonOnLastPage
            | QtWidgets.QWizard.NoCancelButtonOnLastPage
        )

        self.pages = (
            LocaleWizardPage(self),
            ThemeWizardPage(self),
            FfmpegWizardPage(self),
            FinishWizardPage(self)
        )

        for page in self.pages:
            self.addPage(page)

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.onFinish)

    def onFinish(self):
        for page in self.pages:
            if hasattr(page, "getResult"):
                page.getResult()

        restartApplication()
