import locale
import os.path
from pathlib import Path

from piekit.structs.etypes import EList
from piekit.structs.etypes import EDict
from piekit.structs.configs import ManagerConfig, PathConfig

# Base paths
BASE_DIR: Path = Path(__file__).parent.parent.parent
APP_ROOT: Path = BASE_DIR / os.getenv("PIEADUIO_ROOT", "pieapp")
USER_ROOT: Path = os.getenv("USER_ROOT", Path.home() / ".crabs")
SYSTEM_ROOT: Path = BASE_DIR / "piekit"

PIEAPP_ENTRYPOINT = os.getenv("PIEAPP_ENTRYPOINT", "app.main.main")

# Plugins configuration
# Built-in plugins folder
PLUGINS_FOLDER: str = os.getenv("PLUGINS_FOLDER", "plugins")

# User/site plugins folder
USER_PLUGINS_FOLDER: str = os.getenv("USER_PLUGINS_FOLDER", "plugins")

# Components folder
COMPONENTS_FOLDER: str = os.getenv("COMPONENTS_FOLDER", "components")

# Containers folder
CONTAINERS_FOLDER: str = os.getenv("CONTAINERS_FOLDER", "containers")

# Assets
ASSETS_EXCLUDED_FORMATS: EList = []
ASSETS_FOLDER: str = os.getenv("ASSETS_FOLDER", "assets")
THEMES_FOLDER: str = os.getenv("THEMES_FOLDER", "themes")


# Configurations
CONFIGS_FOLDER = os.getenv("CONFIGS_FOLDER", "configs")
USER_CONFIG_FOLDER: str = os.getenv("USER_CONFIGS_FOLDER", "configs")
USER_FOLDER_FILES: EList = ["locales.json", "assets.json"]

# Templates
TEMPLATE_FOLDER: str = "templates"

# Locales
LOCALES: EDict = {
    "en-US": "English",
    "ru-RU": "Русский"
}

# Setup default locale
system_locale = locale.getdefaultlocale()[0].replace("_", "-")
default_locale = system_locale if system_locale in LOCALES else "en-US"

DEFAULT_LOCALE: str = os.getenv("DEFAULT_LOCALE", default_locale)
LOCALES_FOLDER: str = os.getenv("LOCALES_FOLDER", "locales")


# Managers startup configuration
# TODO: Replace `mount` attribute with Qt signal name (str) and emit it via `QMetaObject` -> `invokeMethod`
MANAGERS: EList = [
    ManagerConfig(
        import_string="piekit.managers.configs.manager.ConfigManager",
        mount=True,
        args=(
            PathConfig(APP_ROOT / USER_CONFIG_FOLDER, section="shared"),
            PathConfig(USER_ROOT / USER_CONFIG_FOLDER, section="user")
        )
    ),
    ManagerConfig(
        import_string="piekit.managers.locales.manager.LocaleManager",
        mount=True,
        args=(PathConfig(APP_ROOT / LOCALES_FOLDER, section="shared"),)
    ),
    ManagerConfig(
        import_string="piekit.managers.assets.manager.AssetsManager",
        mount=True,
        args=(PathConfig(APP_ROOT / ASSETS_FOLDER, pattern="*", section="shared"),)
    ),
    ManagerConfig(
        import_string="piekit.managers.plugins.manager.PluginManager",
        mount=False
    )
]