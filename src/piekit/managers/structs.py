"""
Default managers
"""
import typing
import dataclasses as dt
from pathlib import Path


class SysManagers:
    # ConfigManager
    Configs = "configs"
    
    # LocaleManager
    Locales = "locales"
    
    # AssetsManager
    Assets = "assets"

    # ShortcutsManager
    Shortcuts = "shortcuts"

    # PluginManager
    Plugins = "plugins"
    
    # MenuManager
    Menus = "menus"

    # ToolButtonManager
    ToolButton = "toolbuttons"

    # ToolBarManager
    ToolBars = "toolbar"
    

class Sections:
    # User/site access section
    User = "user"
    
    # Shared/root access section
    Shared = "shared"


class WorkbenchItems:
    OpenFiles = "openFiles"
    Clear = "clear"
    Convert = "convert"
    Settings = "settings"
    Spacer = "spacer"
    Exit = "exit"


@dt.dataclass(frozen=True, eq=False)
class ManagerConfig:
    import_string: typing.Optional[str]
    mount: bool = dt.field(default=False)
    args: tuple = dt.field(default_factory=tuple)
    kwargs: dict = dt.field(default_factory=dict)


AllPlugins = "__ALL__"
DirectoryType = type("DirectoryType", (), {})