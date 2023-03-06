"""
Exports all gui related classes from the arcade library and adds custom
Elements.
"""


# Arcade gui elements
from arcade.gui.constructs import UIMessageBox
from arcade.gui.events import (UIEvent, UIKeyEvent, UIKeyPressEvent,
                               UIKeyReleaseEvent, UIMouseDragEvent,
                               UIMouseEvent, UIMouseMovementEvent,
                               UIMousePressEvent, UIMouseReleaseEvent,
                               UIMouseScrollEvent, UIOnChangeEvent,
                               UIOnClickEvent, UIOnUpdateEvent, UITextEvent,
                               UITextMotionEvent, UITextMotionSelectEvent)
from arcade.gui.mixins import (UIDraggableMixin, UIMouseFilterMixin,
                               UIWindowLikeMixin)
from arcade.gui.surface import Surface
from arcade.gui.ui_manager import UIManager
from arcade.gui.widgets import (UIAnchorWidget, UIBorder, UIBoxLayout, UIDummy,
                                UIFlatButton, UIInputText, UIInteractiveWidget,
                                UILabel, UILayout, UIPadding, UISpace,
                                UISpriteWidget, UITextArea, UITextureButton,
                                UITexturePane, UIWidget, UIWidgetParent,
                                UIWrapper)

# Custom gui elements
from .gui import UIBlinkingLabel, UIFixedSizeLabel

__all__ = [
    "Surface",
    "UIAnchorWidget",
    "UIBlinkingLabel",
    "UIBorder",
    "UIBoxLayout",
    "UIDraggableMixin",
    "UIDummy",
    "UIEvent",
    "UIFixedSizeLabel",
    "UIFlatButton",
    "UIInputText",
    "UIInteractiveWidget",
    "UIKeyEvent",
    "UIKeyPressEvent",
    "UIKeyReleaseEvent",
    "UILabel",
    "UILayout",
    "UIManager",
    "UIMessageBox",
    "UIMouseDragEvent",
    "UIMouseEvent",
    "UIMouseFilterMixin",
    "UIMouseMovementEvent",
    "UIMousePressEvent",
    "UIMouseReleaseEvent",
    "UIMouseScrollEvent",
    "UIOnChangeEvent",
    "UIOnClickEvent",
    "UIOnUpdateEvent",
    "UIPadding",
    "UISpace",
    "UISpriteWidget",
    "UITextArea",
    "UITextEvent",
    "UITextMotionEvent",
    "UITextMotionSelectEvent",
    "UITextureButton",
    "UITexturePane",
    "UIWidget",
    "UIWidgetParent",
    "UIWindowLikeMixin",
    "UIWrapper",
]
