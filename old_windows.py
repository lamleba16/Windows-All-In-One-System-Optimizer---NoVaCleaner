import winreg
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from Resources import ui

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("Old Windows Support")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Detected Windows version and compatibility status.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        self.version_label = QLabel("Detecting Windows version...")
        self.version_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        cl.addWidget(self.version_label)

        self.banner = QLabel("")
        self.banner.setWordWrap(True)
        self.banner.setStyleSheet("font-weight: bold;")
        cl.addWidget(self.banner)

        link = QPushButton("🌐  Learn more")
        link.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.microsoft.com/en-us/windows")))
        cl.addWidget(link)

        v.addWidget(card, 1)
        self.detect()

    def detect(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            def val(name):
                try:
                    v, _ = winreg.QueryValueEx(key, name)
                    return str(v)
                except FileNotFoundError:
                    return ""
            product = val("ProductName")
            build = val("CurrentBuild")
            display = val("DisplayVersion") or val("ReleaseId")
            winreg.CloseKey(key)
        except Exception as e:
            product, build, display = "Unknown", "", str(e)

        self.version_label.setText(f"Detected: {product} (Build {build}, {display})")

        unsupported = False
        msg = ""
        if "Windows 7" in product or "Windows 8" in product:
            unsupported = True
            msg = "Your Windows version is no longer supported. Please consider upgrading."
        elif "Windows 10" in product:
            try:
                if int(build) < 19045:
                    unsupported = True
                    msg = "Your Windows 10 build is outdated. Consider updating."
            except ValueError:
                pass

        if unsupported:
            self.banner.setText("⚠️  Compatibility warning: " + msg)
            self.banner.setStyleSheet("color: #ef4444; font-weight: bold;")
        else:
            self.banner.setText("✅  Your Windows version is supported.")
            self.banner.setStyleSheet("color: #10b981; font-weight: bold;")