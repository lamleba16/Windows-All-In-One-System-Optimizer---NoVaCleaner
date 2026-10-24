from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QStackedWidget, QLabel, QFrame)
from PySide6.QtCore import Qt
from Resources import ui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NovaCleaner")
        self.resize(1180, 760)
        self.setMinimumSize(960, 640)

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header bar
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #4f46e5, stop:1 #06b6d4);")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)
        title = QLabel("NovaCleaner")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 800; background: transparent;")
        hl.addWidget(title)
        hl.addStretch()
        subtitle = QLabel("System Optimization Suite")
        subtitle.setStyleSheet("color: rgba(255,255,255,170); font-size: 12px; background: transparent;")
        hl.addWidget(subtitle)
        root.addWidget(header)

        # Body
        body = QWidget()
        h = QHBoxLayout(body)
        h.setContentsMargins(16, 16, 16, 16)
        h.setSpacing(16)

        self.nav = QListWidget()
        self.nav.setMaximumWidth(240)
        self.nav.setMinimumWidth(200)
        ui.shadow(self.nav, blur=18, y=4, alpha=40)
        icons = ["🧹", "🩺", "🔄", "🪟", "🗑️", "⚙️"]
        labels = ["Temp Cleaner", "System Damage", "Windows Update", "Old Windows", "File Shredder", "Settings"]
        for ic, lb in zip(icons, labels):
            self.nav.addItem(f"  {ic}   {lb}")

        self.stack = QStackedWidget()

        from Resources import (tmpcleaner, chckpc, update_checker,
                               old_windows, file_shredder, settings_page)
        pages = [
            tmpcleaner.Page(),
            chckpc.Page(),
            update_checker.Page(),
            old_windows.Page(),
            file_shredder.Page(),
            settings_page.Page(),
        ]
        for p in pages:
            self.stack.addWidget(p)
            ui.fade_in(p, 400)

        h.addWidget(self.nav)
        h.addWidget(self.stack, 1)
        root.addWidget(body, 1)
        self.setCentralWidget(central)

        self.nav.currentRowChanged.connect(self._on_nav)
        self.nav.setCurrentRow(0)

    def _on_nav(self, idx):
        self.stack.setCurrentIndex(idx)
        w = self.stack.widget(idx)
        if w:
            ui.fade_in(w, 250)