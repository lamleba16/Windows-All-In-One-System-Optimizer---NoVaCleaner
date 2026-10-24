from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget)
from PySide6.QtCore import Qt, QProcess, QUrl
from PySide6.QtGui import QDesktopServices
from Resources import ui

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("Windows Update Checker")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Check for Windows updates and open the Settings page.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        self.status = QLabel("Not checked yet.")
        cl.addWidget(self.status)

        row = QHBoxLayout()
        self.check_btn = QPushButton("🔄  Check for Updates")
        self.open_btn = QPushButton("⚙️  Open Windows Update")
        row.addWidget(self.check_btn)
        row.addWidget(self.open_btn)
        cl.addLayout(row)

        self.list = QListWidget()
        self.list.setMinimumHeight(180)
        cl.addWidget(self.list)

        v.addWidget(card, 1)

        self.check_btn.clicked.connect(self.on_check)
        self.open_btn.clicked.connect(self.on_open)

    def on_check(self):
        self.list.clear()
        self.status.setText("Triggering update scan (best-effort)...")
        p = QProcess(self)
        p.start("UsoClient", ["StartScan"])
        ps = QProcess(self)
        ps.start("powershell", ["-NoProfile", "-Command",
            "if (Get-Module -ListAvailable -Name PSWindowsUpdate) { Get-WindowsUpdate | Select-Object -ExpandProperty Title } else { Write-Output 'PSWindowsUpdate module not available' }"])
        ps.waitForFinished(15000)
        out = bytes(ps.readAllStandardOutput()).decode("utf-8", "replace")
        found = False
        for line in out.splitlines():
            line = line.strip()
            if not line or "PSWindowsUpdate module not available" in line:
                continue
            found = True
            self.list.addItem(line)
        if not found:
            self.status.setText("Update scan triggered. Could not enumerate updates. Use 'Open Windows Update'.")
        else:
            self.status.setText(f"Found {self.list.count()} update(s).")

    def on_open(self):
        QDesktopServices.openUrl(QUrl("ms-settings:windowsupdate"))