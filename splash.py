import os, time
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QAbstractAnimation
from PySide6.QtGui import QPixmap, QFont, QLinearGradient, QColor, QPainter

ASSETS = os.path.join(os.path.dirname(__file__), "assets")

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(720, 420)
        self._t0 = time.time()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Background image
        self.bg = QLabel()
        self.bg.setAlignment(Qt.AlignCenter)
        path = os.path.join(ASSETS, "splashscreenimage.png")
        if os.path.exists(path):
            px = QPixmap(path).scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.bg.setPixmap(px)
        else:
            self.bg.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #4f46e5, stop:1 #06b6d4);")
        self.bg.setStyleSheet(self.bg.styleSheet() + "background-color: #0f172a;")
        layout.addWidget(self.bg, 1)

        # Overlay container (we'll paint gradient via stylesheet on a frame)
        overlay = QWidget(self.bg)
        overlay.setGeometry(0, 0, self.width(), self.height())
        ol = QVBoxLayout(overlay)
        ol.setContentsMargins(40, 40, 40, 40)
        ol.addStretch()
        title = QLabel("NovaCleaner")
        title.setStyleSheet("color: white; font-size: 46px; font-weight: 800; background: transparent;")
        ol.addWidget(title)
        sub = QLabel("Clean. Optimize. Protect.")
        sub.setStyleSheet("color: rgba(255,255,255,180); font-size: 16px; background: transparent;")
        ol.addWidget(sub)
        ol.addStretch()
        ver = QLabel("v1.0 (Work in Progress)")
        ver.setStyleSheet("color: rgba(255,255,255,140); font-size: 11px; background: transparent;")
        ol.addWidget(ver)

        # Center on screen
        from PySide6.QtGui import QGuiApplication
        scr = QGuiApplication.primaryScreen().availableGeometry()
        self.move(scr.center().x() - self.width()//2, scr.center().y() - self.height()//2)

        # fade in
        self._effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._effect)
        self._effect.setOpacity(0.0)
        self._fadein = QPropertyAnimation(self._effect, b"opacity")
        self._fadein.setDuration(600)
        self._fadein.setStartValue(0.0)
        self._fadein.setEndValue(1.0)
        self._fadein.setEasingCurve(QEasingCurve.OutCubic)
        self._fadein.start()

        QTimer.singleShot(2200, self._dismiss)

    def _dismiss(self):
        self._fadeout = QPropertyAnimation(self._effect, b"opacity")
        self._fadeout.setDuration(500)
        self._fadeout.setStartValue(1.0)
        self._fadeout.setEndValue(0.0)
        self._fadeout.finished.connect(self.close)
        self._fadeout.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        # dark gradient overlay at bottom for text legibility
        p = QPainter(self)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor(0, 0, 0, 40))
        g.setColorAt(0.6, QColor(0, 0, 0, 120))
        g.setColorAt(1.0, QColor(0, 0, 0, 200))
        p.fillRect(self.rect(), g)