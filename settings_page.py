from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QComboBox,
    QCheckBox, QSpinBox, QLabel)
from Resources import settings, ui

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 22px; font-weight: 800;")
        v.addWidget(title)
        sub = QLabel("Customize NovaCleaner preferences.")
        sub.setStyleSheet("color: #64748b;")
        v.addWidget(sub)

        card = ui.card()
        ui.shadow(card)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)

        s = settings.settings
        form = QFormLayout()
        form.setSpacing(10)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["system", "light", "dark"])
        idx = self.theme_combo.findText(s.theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(lambda t: setattr(s, "theme", t))
        form.addRow("Theme:", self.theme_combo)

        self.startup_cb = QCheckBox("Run on Windows startup")
        self.startup_cb.setChecked(s.run_on_startup)
        self.startup_cb.toggled.connect(lambda v: s.set("run_on_startup", v))
        form.addRow(self.startup_cb)

        self.passes_spin = QSpinBox()
        self.passes_spin.setRange(1, 7)
        self.passes_spin.setValue(s.shredder_passes)
        self.passes_spin.valueChanged.connect(lambda v: s.set("shredder_passes", v))
        form.addRow("Shredder passes:", self.passes_spin)

        self.auto_upd_cb = QCheckBox("Auto-check updates on launch")
        self.auto_upd_cb.setChecked(s.auto_check_updates)
        self.auto_upd_cb.toggled.connect(lambda v: s.set("auto_check_updates", v))
        form.addRow(self.auto_upd_cb)

        self.u_cb = QCheckBox("Include user %TEMP%")
        self.u_cb.setChecked(s.temp_user)
        self.u_cb.toggled.connect(lambda v: s.set("temp_user", v))
        form.addRow(self.u_cb)

        self.w_cb = QCheckBox("Include C:\\Windows\\Temp")
        self.w_cb.setChecked(s.temp_windows)
        self.w_cb.toggled.connect(lambda v: s.set("temp_windows", v))
        form.addRow(self.w_cb)

        self.l_cb = QCheckBox("Include %LOCALAPPDATA%\\Temp")
        self.l_cb.setChecked(s.temp_localappdata)
        self.l_cb.toggled.connect(lambda v: s.set("temp_localappdata", v))
        form.addRow(self.l_cb)

        note = QLabel("Settings are applied immediately.")
        note.setStyleSheet("color: #64748b; font-size: 11px;")
        form.addRow(note)

        cl.addLayout(form)
        v.addWidget(card, 1)