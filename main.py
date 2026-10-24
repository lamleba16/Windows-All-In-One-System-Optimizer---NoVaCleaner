import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer

from Resources import settings, styles
from Resources.splash import SplashScreen
from Resources.mainwindow import MainWindow
from Resources.about import Page as WelcomePage

app = QApplication(sys.argv)
app.setApplicationName("NovaCleaner")
app.setApplicationVersion("1.0")
app.setQuitOnLastWindowClosed(False)

styles.apply(app, settings.settings)

splash = SplashScreen()
splash.show()

def after_splash():
    if settings.settings.first_run:
        w = WelcomePage()
        w.show()
        def go():
            settings.settings.first_run = False
            w.close()
            mw = MainWindow()
            mw.show()
            app._mw = mw
        from PySide6.QtWidgets import QPushButton
        for b in w.findChildren(QPushButton):
            b.clicked.connect(go)
    else:
        mw = MainWindow()
        mw.show()
        app._mw = mw
    splash.close()

QTimer.singleShot(1900, after_splash)

sys.exit(app.exec())