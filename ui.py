from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation

def card(parent=None):
    f = QFrame(parent)
    f.setObjectName("card")
    f.setFrameShape(QFrame.StyledPanel)
    return f

def shadow(widget, blur=24, x=0, y=6, alpha=60):
    eff = QGraphicsDropShadowEffect(widget)
    eff.setBlurRadius(blur)
    eff.setOffset(x, y)
    eff.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(eff)
    return eff

def fade_in(widget, duration=350):
    from PySide6.QtWidgets import QGraphicsOpacityEffect
    eff = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(eff)
    eff.setOpacity(0.0)
    anim = QPropertyAnimation(eff, b"opacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.finished.connect(lambda: widget.setGraphicsEffect(None))
    anim.start(QAbstractAnimation.DeleteWhenStopped)
    return anim

def page_layout(widget):
    v = QVBoxLayout(widget)
    v.setContentsMargins(24, 24, 24, 24)
    v.setSpacing(16)
    return v