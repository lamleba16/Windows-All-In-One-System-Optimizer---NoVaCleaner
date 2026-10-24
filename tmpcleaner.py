import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QProgressBar, QTextEdit, QLabel)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from Resources import ui

class Worker(QObject):
    scan_progress = Signal(int, int)
    scan_done = Signal(int, int, list)
    clean_progress = Signal(int, int, int)
    clean_done = Signal(int, int, int)

    def __init__(self, include_user, include_win, include_local):
        super().__init__()
        self.include_user = include_user
        self.include_win = include_win
        self.include_local = include_local
        self.files = []

    def scan(self):
        roots = []
        if self.include_user:
            roots.append(os.environ.get("TEMP", ""))
        if self.include_win:
            roots.append(os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Temp"))
        if self.include_local:
            roots.append(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"))
        roots = list(dict.fromkeys([r for r in roots if r and os.path.exists(r)]))
        files = []
        total = 0
        for root in roots:
            for dirpath, _, filenames in os.walk(root):
                for fn in filenames:
                    p = os.path.join(dirpath, fn)
                    try:
                        sz = os.path.getsize(p)
                    except OSError:
                        continue
                    files.append(p)
                    total += sz
                    if len(files) % 100 == 0:
                        self.scan_progress.emit(len(files), total)
        self.scan_done.emit(len(files), total, files)

    def clean(self):
        removed = skipped = 0
        reclaimed = 0
        n = len(self.files)
        for i, p in enumerate(self.files):
            try:
                sz = os.path.getsize(p)
                os.remove(p)
                removed += 1
                reclaimed += sz
            except OSError:
                skipped += 1
            pct = int((i + 1) * 100 / n) if n else 100
            self.clean_progress.emit(pct, removed, skipped)
        self.clean_done.emit(removed, skipped, reclaimed)

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("Temporary File Cleaner")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Scan and remove temporary files to reclaim disk space.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        row = QHBoxLayout()
        self.scan_btn = QPushButton("🔍  Scan")
        self.clean_btn = QPushButton("🧹  Clean")
        self.clean_btn.setEnabled(False)
        row.addWidget(self.scan_btn)
        row.addWidget(self.clean_btn)
        row.addStretch()
        cl.addLayout(row)

        self.progress = QProgressBar()
        cl.addWidget(self.progress)

        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setMinimumHeight(200)
        cl.addWidget(self.results)

        self.reclaimed = QLabel("Reclaimed space: 0 bytes")
        self.reclaimed.setStyleSheet("font-weight: 600; color: #4f46e5;")
        cl.addWidget(self.reclaimed)

        v.addWidget(card, 1)

        self.scan_btn.clicked.connect(self.on_scan)
        self.clean_btn.clicked.connect(self.on_clean)

        self._thread = None
        self._worker = None
        self._files = []

    def on_scan(self):
        from Resources import settings
        s = settings.settings
        self.results.clear()
        self.clean_btn.setEnabled(False)
        self.progress.setRange(0, 0)
        self._thread = QThread()
        self._worker = Worker(s.temp_user, s.temp_windows, s.temp_localappdata)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.scan)
        self._worker.scan_progress.connect(self.on_scan_progress)
        self._worker.scan_done.connect(self.on_scan_done)
        self._thread.start()

    def on_scan_progress(self, files_found, total_bytes):
        self.results.setText(f"Scanning... files: {files_found}, bytes: {total_bytes}")

    def on_scan_done(self, count, total, files):
        self._files = files
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.results.setText(f"Scan complete.\nFiles found: {count}\nTotal size: {total} bytes")
        self.clean_btn.setEnabled(bool(files))
        self._thread.quit()

    def on_clean(self):
        if not self._files:
            return
        self.progress.setValue(0)
        self.clean_btn.setEnabled(False)
        self._thread = QThread()
        self._worker = Worker(False, False, False)
        self._worker.files = self._files
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.clean)
        self._worker.clean_progress.connect(self.on_clean_progress)
        self._worker.clean_done.connect(self.on_clean_done)
        self._thread.start()

    def on_clean_progress(self, pct, removed, skipped):
        self.progress.setValue(pct)
        self.results.setText(f"Cleaning... removed: {removed}, skipped: {skipped}")

    def on_clean_done(self, removed, skipped, reclaimed):
        self.progress.setValue(100)
        self.results.setText(f"Clean complete.\nRemoved: {removed}\nSkipped: {skipped}\nReclaimed: {reclaimed} bytes")
        self.reclaimed.setText(f"Reclaimed space: {reclaimed} bytes")
        self._files = []
        self._thread.quit()