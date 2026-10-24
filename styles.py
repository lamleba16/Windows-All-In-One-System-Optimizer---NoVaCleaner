LIGHT_QSS = """
QWidget { background-color: #f1f5f9; color: #0f172a; font-family: 'Segoe UI', 'Inter', sans-serif; font-size: 13px; }
QLabel { background: transparent; }
QPushButton { background-color: #4f46e5; color: white; border: none; border-radius: 10px; padding: 9px 18px; font-weight: 600; }
QPushButton:hover { background-color: #4338ca; }
QPushButton:pressed { background-color: #3730a3; }
QPushButton:disabled { background-color: #cbd5e1; color: #64748b; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    border: 1px solid #cbd5e1; border-radius: 10px; padding: 8px 12px; background: white; color: #0f172a; }
QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #4f46e5; }
QListWidget { border: none; border-radius: 12px; background: white; padding: 6px; }
QListWidget::item { padding: 12px 14px; border-radius: 8px; margin: 2px 0; }
QListWidget::item:hover { background-color: #eef2ff; }
QListWidget::item:selected { background-color: #4f46e5; color: white; }
QProgressBar { border: none; border-radius: 10px; text-align: center; background: #e2e8f0; height: 16px; }
QProgressBar::chunk { background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #4f46e5, stop:1 #06b6d4); border-radius: 9px; }
QGroupBox { border: 1px solid #e2e8f0; border-radius: 12px; margin-top: 12px; padding: 12px; font-weight: 600; background: white; }
QFrame#card { background: white; border-radius: 14px; border: 1px solid #e2e8f0; }
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #94a3b8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QHeaderView::section { background: #f8fafc; padding: 6px; border: none; font-weight: 600; }
"""

DARK_QSS = """
QWidget { background-color: #0b1120; color: #e2e8f0; font-family: 'Segoe UI', 'Inter', sans-serif; font-size: 13px; }
QLabel { background: transparent; }
QPushButton { background-color: #6366f1; color: white; border: none; border-radius: 10px; padding: 9px 18px; font-weight: 600; }
QPushButton:hover { background-color: #4f46e5; }
QPushButton:pressed { background-color: #4338ca; }
QPushButton:disabled { background-color: #334155; color: #64748b; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    border: 1px solid #334155; border-radius: 10px; padding: 8px 12px; background: #1e293b; color: #e2e8f0; }
QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border: 1px solid #6366f1; }
QListWidget { border: none; border-radius: 12px; background: #1e293b; padding: 6px; }
QListWidget::item { padding: 12px 14px; border-radius: 8px; margin: 2px 0; }
QListWidget::item:hover { background-color: #334155; }
QListWidget::item:selected { background-color: #6366f1; color: white; }
QProgressBar { border: none; border-radius: 10px; text-align: center; background: #1e293b; height: 16px; }
QProgressBar::chunk { background-color: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #6366f1, stop:1 #22d3ee); border-radius: 9px; }
QGroupBox { border: 1px solid #334155; border-radius: 12px; margin-top: 12px; padding: 12px; font-weight: 600; background: #1e293b; }
QFrame#card { background: #1e293b; border-radius: 14px; border: 1px solid #334155; }
QScrollBar:vertical { background: transparent; width: 10px; }
QScrollBar::handle:vertical { background: #475569; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #64748b; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

def resolve_theme(settings):
    t = settings.theme
    if t == "system":
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtCore import Qt
        scheme = QGuiApplication.styleHints().colorScheme()
        return "dark" if scheme == Qt.ColorScheme.Dark else "light"
    return t

def apply(app, settings):
    app.setStyleSheet(DARK_QSS if resolve_theme(settings) == "dark" else LIGHT_QSS)