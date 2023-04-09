from cme import gui
import inspect


def test_exports_arcade_gui_classes() -> None:
    all_exports = [
        "Surface",
        "UIAnchorWidget",
        "UIBorder",
        "UIBoxLayout",
        "UIDraggableMixin",
        "UIDummy",
        "UIEvent",
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
    for item in all_exports:
        assert hasattr(gui, item) and inspect.isclass(getattr(gui, item))
