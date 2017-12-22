# -*- coding: utf-8 -*-
#
# This file is part of NINJA-IDE (http://ninja-ide.org).
#
# NINJA-IDE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# NINJA-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NINJA-IDE; If not, see <http://www.gnu.org/licenses/>.

# import sys

from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import (
    QIcon,
    QPixmap
)
from PyQt5.QtCore import (
    Qt,
    # QTextCodec,
    QCoreApplication,
    # QTranslator,
    # QLibraryInfo,
    # QLocale
)

from ninja_ide import resources
# from ninja_ide.core import settings
# from ninja_ide.core import ipc
# from ninja_ide.core.file_handling import file_manager
from ninja_ide.tools import json_manager
from ninja_ide.tools.logger import NinjaLogger
from ninja_ide.gui import ninja_style
logger = NinjaLogger(__name__)

resources.load_shortcuts()
# Register Components:
# lint:disable
import ninja_ide.gui.main_panel.main_container  # noqa
import ninja_ide.gui.tools_dock.errors_tree  # noqa
import ninja_ide.gui.tools_dock.tools_dock  # noqa
import ninja_ide.gui.central_widget  # noqa
import ninja_ide.gui.status_bar  # noqa
import ninja_ide.gui.menus.menubar  # noqa
# from ninja_ide.tools.completion import completion_daemon
# Syntax
from ninja_ide.gui.syntax_registry import syntax_registry  # noqa
# Explorer Container
import ninja_ide.gui.explorer.explorer_container  # noqa
from ninja_ide.gui.explorer.tabs import tree_projects_widget  # noqa
from ninja_ide.gui.explorer.tabs import tree_symbols_widget  # noqa
# from ninja_ide.gui.explorer.tabs import web_inspector
# Checkers
# from ninja_ide.gui.editor.checkers import errors_checker
from ninja_ide.gui.editor.checkers import pep8_checker  # noqa
# from ninja_ide.gui.editor.checkers import migration_2to3
# Preferences
from ninja_ide.gui.dialogs.preferences import preferences_general  # noqa
from ninja_ide.gui.dialogs.preferences import preferences_execution  # noqa
# from ninja_ide.gui.dialogs.preferences import preferences_shortcuts
from ninja_ide.gui.dialogs.preferences import preferences_interface  # noqa
from ninja_ide.gui.dialogs.preferences import preferences_editor_general  # noqa
from ninja_ide.gui.dialogs.preferences import preferences_editor_display  # noqa
# from ninja_ide.gui.dialogs.preferences import preferences_editor_completion
# from ninja_ide.gui.dialogs.preferences import preferences_plugins
# from ninja_ide.gui.dialogs.preferences import preferences_theme
import ninja_ide.gui.editor.extensions  # noqa
# Templates
from ninja_ide.core.template_registry import ntemplate_registry  # noqa
from ninja_ide.core.template_registry import (
    bundled_project_types
)
###########################################################################
# Start Virtual Env that supports encapsulation of plugins
###########################################################################
# from ninja_ide.core.encapsulated_env import nenvironment

from ninja_ide.gui import ide
# lint:enable


def start_ide(app, filenames, projects_path, extra_plugins, linenos):
    """Load all the settings necessary before loading the UI, and start IDE."""

    QCoreApplication.setOrganizationName('NINJA-IDE')
    QCoreApplication.setOrganizationDomain('NINJA-IDE')
    QCoreApplication.setApplicationName('NINJA-IDE')
    app.setWindowIcon(QIcon(":img/icon"))
    # Check if there is another session of ninja-ide opened
    # and in that case send the filenames and projects to that session
    # running = ipc.is_running()
    # start_server = not running[0]
    # if running[0] and (filenames or projects_path):
    #     sended = ipc.send_data(running[1], filenames, projects_path, linenos)
    #    running[1].close()
    #    if sended:
    #        sys.exit()
    # else:
    #    running[1].close()

    # Create and display the splash screen
    splash_pix = QPixmap(":img/splash")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Set the codec for strings (QString)
    # QTextCodec.setCodecForCStrings(QTextCodec.codecForName('utf-8'))

    # FIXME: handle this
    qsettings = ide.IDE.ninja_settings()
    data_qsettings = ide.IDE.data_settings()
    # Translator
    # language = QLocale.system().name()
    # lang = qsettings.value('preferences/interface/language',
    #                       defaultValue=language, type='QString') + '.qm'
    # lang_path = file_manager.create_path(resources.LANGS, lang)
    # if file_manager.file_exists(lang_path):
    #    settings.LANGUAGE = lang_path
    # translator = QTranslator()
    # if settings.LANGUAGE:
    #    translator.load(settings.LANGUAGE)
    #    app.installTranslator(translator)

    #    qtTranslator = QTranslator()
    #    qtTranslator.load(
    #        "qt_" + language,
    #        QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    #    app.installTranslator(qtTranslator)

    # Loading Syntax
    splash.showMessage("Loading Syntax", Qt.AlignRight | Qt.AlignTop, Qt.black)
    json_manager.load_syntax()

    # Read Settings
    splash.showMessage("Loading Settings", Qt.AlignRight | Qt.AlignTop,
                       Qt.black)

    # FIXME: handle this
    # Set Stylesheet
    # style_applied = False
    # if settings.NINJA_SKIN not in ('Default'):
    #    file_name = ("%s.qss" % settings.NINJA_SKIN)
    #    qss_file = file_manager.create_path(resources.NINJA_THEME_DOWNLOAD,
    #                                        file_name)
    #    if file_manager.file_exists(qss_file):
    #        with open(qss_file) as fileaccess:
    #            qss = fileaccess.read()
    #            app.setStyleSheet(qss)
    #            style_applied = True
    # if not style_applied:
    #    if settings.NINJA_SKIN == 'Default':
    #        with open(resources.NINJA_THEME) as fileaccess:
    #            qss = fileaccess.read()
    #    app.setStyleSheet(qss)

    # FIXME: handle this
    # Loading Schemes
    splash.showMessage("Loading Schemes...",
                       Qt.AlignRight | Qt.AlignTop, Qt.black)
    all_schemes = json_manager.load_editor_schemes()
    scheme = qsettings.value("preferences/editor/scheme", "")
    resources.COLOR_SCHEME = all_schemes['Ninja Dark']
    # if scheme:
    #    color_scheme = all_schemes[scheme]
    #    resources.CUSTOM_SCHEME = color_scheme

    # print(all_schemes)
    # scheme = qsettings.value('preferences/editor/scheme', "default",
    #                         type='QString')
    # if scheme != 'default':
    #    scheme = file_manager.create_path(resources.EDITOR_SKINS,
    #                                      scheme + '.color')
    #    if file_manager.file_exists(scheme):
    #        resources.CUSTOM_SCHEME = json_manager.parse(open(scheme))

    # Loading Shortcuts
    # resources.load_shortcuts()
    # Loading GUI
    splash.showMessage("Loading GUI", Qt.AlignRight | Qt.AlignTop, Qt.black)
    # ninjaide = ide.IDE(start_server)
    ninjaide = ide.IDE()

    # Style
    app.setStyle(ninja_style.NinjaStyle())

    # Showing GUI
    ninjaide.show()
    # OSX workaround for ninja window not in front
    try:
        ninjaide.raise_()
    except:
        pass  # I really dont mind if this fails in any form
    # FIXME: handle this
    # Loading Session Files
    splash.showMessage("Loading Files and Projects",
                       Qt.AlignRight | Qt.AlignTop, Qt.black)

    # First check if we need to load last session files
    files = data_qsettings.value(
        'last_session/opened_files', [])
    projects = data_qsettings.value(
        'last_session/projects', [])
    current_file = data_qsettings.value('last_session/current_file', '')
    if files is None:
        files = []
    if projects is None:
        projects = []
    ninjaide.load_session_files_projects(
        files, projects, current_file, []
    )
    # projects = data_qsettings.value('last_session/projects', [])
    # files = []
    # projects = []
    # if projects is None:
    #    projects = []
    # if files is None:
    #    files = []
    # current_file = ''
    # recent_files = []
    # ninjaide.load_session_files_projects(files, projects,
    #                                     current_file, recent_files)

    # if qsettings.value('preferences/general/loadFiles', True, type=bool):
    #    # Files in Main Tab
    #    files = data_qsettings.value('lastSession/openedFiles', [])
    #    tempFiles = []
    #    if files:
    #        for file_ in files:
    #            fileData = tuple(file_)
    #            if fileData:
    #                tempFiles.append(fileData)
    #    files = tempFiles

    #    # Recent Files
    #    recent_files = data_qsettings.value('lastSession/recentFiles', [])
    #    # Current File
    #    current_file = data_qsettings.value(
    #        'lastSession/currentFile', '', type='QString')
    #    # Projects
    #    projects = data_qsettings.value('lastSession/projects', [])
    # else:
    #    files = []
    #    recent_files = []
    #    current_file = ''
    #    projects = []

    # Include files received from console args
    # file_with_nro = list([(f[0], (f[1] - 1, 0), 0)
    #                     for f in zip(filenames, linenos)])
    # file_without_nro = list([(f, (0, 0), 0) for f in filenames[len(linenos):]])
    # files += file_with_nro + file_without_nro
    # Include projects received from console args
    # if projects_path:
    #    projects += projects_path
    # FIXME: IMPROVE THIS WITH THE NEW WAY OF DO IT
    # ninjaide.load_session_files_projects(files, projects,
    #                                     current_file, recent_files)
    # Load external plugins
    # if extra_plugins:
    #     ninjaide.load_external_plugins(extra_plugins)
    splash.finish(ninjaide)
    # ninjaide.notify_plugin_errors()
    # ninjaide.show_python_detection()
