from cme.sprite import Animator


def test_animator() -> None:
    class AnimatorTester:
        def __init__(self) -> None:
            self.val1 = 0
            self.val2 = 1.0
            self.val3 = 220.5
            self.val4 = -5.3
            self.val5 = -149

    obj = AnimatorTester()
    animator = Animator(
        obj,
        5,
        val1=5,
        val2=-1.5,
        val3=360,
        val4=4.7,
        val5=-150,
    )

    assert obj.val1 == 0
    assert obj.val2 == 1.0
    assert obj.val3 == 220.5
    assert obj.val4 == -5.3
    assert obj.val5 == -149

    animator.update(1)
    assert obj.val1 == 1
    assert obj.val2 == 0.5
    assert obj.val4 == -3.3
    assert obj.val5 == -149.2

    animator.update(2.25)
    assert obj.val3 == 311.175

    animator.update(1.75)
    assert obj.val1 == 5
    assert obj.val2 == -1.5
    assert obj.val3 == 360
    assert obj.val4 == 4.7
    assert obj.val5 == -150
