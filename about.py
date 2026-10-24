import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from Resources import ui

class Page(QWidget):
    def __init__(self):
        super().__init__()
        v = ui.page_layout(self)
        v.setAlignment(Qt.AlignCenter)

        card = ui.card()
        ui.shadow(card, blur=30, y=8, alpha=50)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 40, 40, 40)
        cl.setSpacing(16)
        cl.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to NovaCleaner")
        title.setStyleSheet("font-size: 30px; font-weight: 800;")
        title.setAlignment(Qt.AlignCenter)
        cl.addWidget(title)

        desc = QLabel("Clean temporary files, check system health,\nshred sensitive files, and keep Windows up to date.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #64748b; font-size: 14px;")
        cl.addWidget(desc)

        img = QLabel()
        path = os.path.join(os.path.dirname(__file__), "assets", "fly.png")
        if os.path.exists(path):
            img.setPixmap(QPixmap(path).scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img.setAlignment(Qt.AlignCenter)
        cl.addWidget(img)

        btn = QPushButton("🚀  Get Started")
        btn.setMinimumWidth(200)
        cl.addWidget(btn, alignment=Qt.AlignCenter)

        v.addWidget(card)
        ui.fade_in(self, 500)