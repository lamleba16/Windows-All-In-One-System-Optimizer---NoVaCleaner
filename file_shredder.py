import os, random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QComboBox, QLineEdit, QProgressBar, QTextEdit, QLabel,
    QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from Resources import ui

class Worker(QObject):
    progress = Signal(int, str)
    file_result = Signal(str, bool, str)
    finished = Signal(int, int)

    def __init__(self, files, passes):
        super().__init__()
        self.files = files
        self.passes = passes

    def run(self):
        ok_count = fail_count = 0
        n = len(self.files)
        for i, path in enumerate(self.files):
            ok = True
            err = ""
            try:
                size = os.path.getsize(path)
                for _ in range(self.passes):
                    with open(path, "wb") as f:
                        written = 0
                        while written < size:
                            chunk = min(65536, size - written)
                            f.write(bytes(random.getrandbits(8) for _ in range(chunk)))
                            written += chunk
                        f.flush()
                        os.fsync(f.fileno())
                d = os.path.dirname(path)
                newp = os.path.join(d, format(random.getrandbits(64), "x"))
                try:
                    os.rename(path, newp)
                    os.remove(newp)
                except OSError:
                    try:
                        os.remove(path)
                    except OSError as e:
                        ok = False
                        err = str(e)
            except OSError as e:
                ok = False
                err = str(e)
            if ok:
                ok_count += 1
            else:
                fail_count += 1
            self.file_result.emit(path, ok, err)
            pct = int((i + 1) * 100 / n) if n else 100
            self.progress.emit(pct, path)
        self.finished.emit(ok_count, fail_count)

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("File Shredder")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Securely overwrite and delete files. This cannot be undone.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(12)

        self.select_btn = QPushButton("📂  Select Files")
        cl.addWidget(self.select_btn)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(120)
        cl.addWidget(self.file_list)

        row = QHBoxLayout()
        row.addWidget(QLabel("Passes:"))
        self.passes_combo = QComboBox()
        self.passes_combo.addItems(["1", "3", "7"])
        from Resources import settings
        self.passes_combo.setCurrentText(str(settings.settings.shredder_passes))
        row.addWidget(self.passes_combo)
        row.addStretch()
        cl.addLayout(row)

        self.confirm_edit = QLineEdit()
        self.confirm_edit.setPlaceholderText("Type 'Confirm' to enable Shred")
        cl.addWidget(self.confirm_edit)

        self.shred_btn = QPushButton("🔥  Shred")
        self.shred_btn.setEnabled(False)
        cl.addWidget(self.shred_btn)

        self.progress = QProgressBar()
        cl.addWidget(self.progress)

        self.report = QTextEdit()
        self.report.setReadOnly(True)
        self.report.setMinimumHeight(120)
        cl.addWidget(self.report)

        v.addWidget(card, 1)

        self.selected_files = []
        self.select_btn.clicked.connect(self.on_select)
        self.confirm_edit.textChanged.connect(self.on_confirm_changed)
        self.shred_btn.clicked.connect(self.on_shred)

    def on_select(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files to shred")
        if not files:
            return
        self.selected_files = files
        self.file_list.clear()
        for f in files:
            self.file_list.addItem(f)
        self.on_confirm_changed(self.confirm_edit.text())

    def on_confirm_changed(self, text):
        self.shred_btn.setEnabled(text == "Confirm" and bool(self.selected_files))

    def on_shred(self):
        if not self.selected_files:
            return
        r1 = QMessageBox.question(self, "Confirm Shred",
            "Are you sure? This cannot be undone.", QMessageBox.Yes | QMessageBox.Cancel)
        if r1 != QMessageBox.Yes:
            return
        r2 = QMessageBox.question(self, "Confirm Files",
            "The following files will be destroyed:\n" + "\n".join(self.selected_files) + "\n\nProceed?",
            QMessageBox.Yes | QMessageBox.Cancel)
        if r2 != QMessageBox.Yes:
            return

        self.report.clear()
        self.progress.setValue(0)
        self.shred_btn.setEnabled(False)

        passes = int(self.passes_combo.currentText())
        self._thread = QThread()
        self._worker = Worker(self.selected_files, passes)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self.on_progress)
        self._worker.file_result.connect(self.on_file_result)
        self._worker.finished.connect(self.on_finished)
        self._thread.start()

    def on_progress(self, pct, current):
        self.progress.setValue(pct)

    def on_file_result(self, path, ok, err):
        if ok:
            self.report.append(f"Shredded: {path}")
        else:
            self.report.append(f"FAILED: {path} ({err})")

    def on_finished(self, ok, fail):
        self.report.append(f"\nDone. Success: {ok}, Failed: {fail}")
        self.progress.setValue(100)
        self.selected_files = []
        self.file_list.clear()
        self.confirm_edit.clear()