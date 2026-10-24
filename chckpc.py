import ctypes
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QProgressBar, QLabel, QMessageBox)
from PySide6.QtCore import Qt, QProcess
from Resources import ui

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("System Damage Checker")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Run SFC and DISM to check and repair system files. This can take several minutes.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        warn = QLabel("⚠️  Warning: This scan can take several minutes.")
        warn.setStyleSheet("color: #f59e0b; font-weight: bold;")
        cl.addWidget(warn)

        self.scan_btn = QPushButton("🩺  Scan")
        cl.addWidget(self.scan_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        cl.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(220)
        cl.addWidget(self.log)

        self.summary = QLabel("")
        self.summary.setStyleSheet("font-weight: 700;")
        cl.addWidget(self.summary)

        v.addWidget(card, 1)

        self.scan_btn.clicked.connect(self.on_scan)
        self._proc = None
        self._queue = []
        self._idx = 0
        self._output = ""

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def relaunch_elevated(self):
        import sys
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        from PySide6.QtWidgets import QApplication
        QApplication.quit()

    def on_scan(self):
        if not self.is_admin():
            r = QMessageBox.question(self, "Admin rights needed",
                "This feature requires administrator rights.\nRelaunch as administrator?",
                QMessageBox.Yes | QMessageBox.Cancel)
            if r == QMessageBox.Yes:
                self.relaunch_elevated()
            return
        self.log.clear()
        self.summary.clear()
        self.scan_btn.setEnabled(False)
        self.progress.setVisible(True)
        self._output = ""
        self._queue = [("sfc", ["/scannow"]), ("DISM", ["/Online", "/Cleanup-Image", "/CheckHealth"])]
        self._idx = 0
        self.run_next()

    def run_next(self):
        if self._idx >= len(self._queue):
            self.progress.setVisible(False)
            self.scan_btn.setEnabled(True)
            low = self._output.lower()
            if "did not find any integrity violations" in low or "no component store corruption" in low:
                self.summary.setText("Summary: No issues found.")
                self.summary.setStyleSheet("color: #10b981; font-weight: bold;")
            elif "corrupt" in low or "corruption" in low:
                self.summary.setText("Summary: Issues detected.")
                self.summary.setStyleSheet("color: #ef4444; font-weight: bold;")
            else:
                self.summary.setText("Summary: Scan finished. Review log above.")
            return
        prog, args = self._queue[self._idx]
        self._idx += 1
        self.log.append(f"$ {prog} {' '.join(args)}\n")
        self._proc = QProcess(self)
        self._proc.setProcessChannelMode(QProcess.MergedChannels)
        self._proc.readyReadStandardOutput.connect(self.on_ready)
        self._proc.finished.connect(lambda code, st: self.on_finished(code))
        self._proc.start(prog, args)

    def on_ready(self):
        if not self._proc:
            return
        data = self._proc.readAllStandardOutput()
        text = bytes(data).decode("utf-8", "replace")
        self._output += text
        self.log.moveCursor(self.log.textCursor().End)
        self.log.insertPlainText(text)
        self.log.moveCursor(self.log.textCursor().End)

    def on_finished(self, code):
        self.log.append(f"\n[exit code: {code}]\n")
        self._proc = None
        self.run_next()