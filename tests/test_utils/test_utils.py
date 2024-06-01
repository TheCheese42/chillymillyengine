import pytest

from cme import types, utils


@pytest.mark.requires_window
def test_get_optimal_font_size(initialize_window: None) -> None:
    input_args = [
        ("Hello World!", "Times New Roman", 64, 96),
        ("This is part of our amazing test suite", "Calibri", 12345, 67890),
        ("Sage, the life you give... Have you ever wondered where it's taken from?", "Arial", 1000, 200),  # noqa
    ]
    expected_output = [
        9,
        512,
        23,
    ]
    for (
        (text, font_name, container_width, container_height), expected
    ) in zip(input_args, expected_output):
        assert utils.get_optimal_font_size(
            text, font_name, container_width, container_height
        ) == expected


def test_str2bool() -> None:
    truthy: list[str] = [
        "true", "TRUE", "tRuE", "t", "T", "1", "y", "Y", "yes", "YES", "YeS",
        "enabled", "enable", "on",
    ]
    falsy: list[str] = [
        "false", "FALSE", "fAlSe", "f", "F", "0", "n", "N", "disabled",
        "disable", "off",
    ]
    invalid: list[str | bool | int] = [
        "10", True, False, 0, 1, "nope", "fake", "sure", "AHAHHAHAHAHA"
    ]
    v: str | bool | int
    for v in truthy:
        assert utils.str2bool(v) is True
    for v in falsy:
        assert utils.str2bool(v) is False
    for v in invalid:
        with pytest.raises((ValueError, TypeError)):
            utils.str2bool(v)  # type: ignore
    for v in invalid:
        assert utils.str2bool(v, True) is False  # type: ignore


def test_point_in_rect() -> None:
    assert utils.point_in_rect(0, 0, types.LBWH(0, 0, 10, 10))
    assert utils.point_in_rect(5, 5, types.LBWH(0, 0, 10, 10))
    assert utils.point_in_rect(10, 10, types.LBWH(0, 0, 10, 10))
    assert not utils.point_in_rect(-1, -1, types.LBWH(0, 0, 10, 10))
    assert not utils.point_in_rect(11, 11, types.LBWH(0, 0, 10, 10))
    assert not utils.point_in_rect(5, 15, types.LBWH(2, 4, 12, 9))

    assert utils.point_in_rect(0.0, 0.0, types.LBWH(0.0, 0.0, 10.0, 10.0))
    assert utils.point_in_rect(5.5, 5.5, types.LBWH(0.0, 0.0, 10.0, 10.0))
    assert utils.point_in_rect(10.2, 10.2, types.LBWH(0.5, 0.5, 10.2, 10.2))
    assert not utils.point_in_rect(-1.0, -1.0, types.LBWH(0.0, 0.0, 10.0, 10.0))  # noqa
    assert not utils.point_in_rect(11.5, 11.5, types.LBWH(0.1, 0.1, 10.6, 10.6))  # noqa
    assert not utils.point_in_rect(5.6, 15.3, types.LBWH(2.6, 4.7, 12.2, 9.4))

    assert utils.point_in_rect(0, 0, types.LBWH(0, 0, 0, 0))
    assert utils.point_in_rect(0.0, 0.0, types.LBWH(0.0, 0.0, 0.0, 0.0))
    assert not utils.point_in_rect(-1, 1, types.LBWH(0, 0, 0, 0))
    assert not utils.point_in_rect(1, 1, types.LBWH(0, 0, 0, 0))
    assert not utils.point_in_rect(1.0, 1.0, types.LBWH(0.0, 0.0, 0.0, 0.0))
    assert not utils.point_in_rect(-1.0, 1.0, types.LBWH(0.0, 0.0, 0.0, 0.0))


def test_missing_keys() -> None:
    assert utils.missing_keys({1: 2, 2: 3, 3: 4}, {1: 5, 3: 6}) == [2]
    assert utils.missing_keys({1: 2, 3: 4}, {1: 5, 3: 6}) == []
    assert utils.missing_keys({1: 2, 3: 4}, {1: 5, 2: 42, 3: 6}) == []


def test_shrink_list_simple() -> None:
    assert utils.shrink_list_simple(list(range(1, 11)), 5) == [1, 3, 5, 7, 9]
    assert utils.shrink_list_simple(list(range(1, 11)), 2) == [1, 6]
    assert utils.shrink_list_simple([1, 2, 3], 1) == [1]
    assert utils.shrink_list_simple([1, 2, 3, 4, 5], 2) == [1, 4]


def test_calc_change_x_y() -> None:
    assert utils.calc_change_x_y(10, 0) == (10, 0)
    assert utils.calc_change_x_y(10, 90) == (0, 10)
    assert utils.calc_change_x_y(10, 180) == (-10, 0)
    assert utils.calc_change_x_y(10, 270) == (0, -10)
    assert utils.calc_change_x_y(10, -90) == (0, -10)
    assert utils.calc_change_x_y(10, -180) == (-10, 0)
    assert utils.calc_change_x_y(10, -270) == (0, 10)
    assert utils.calc_change_x_y(10, 360) == (10, 0)
    assert utils.calc_change_x_y(10, 450) == (0, 10)
    assert utils.calc_change_x_y(0, 348) == (0, 0)
    assert utils.calc_change_x_y(-10, 270) == (0, 10)
    assert utils.calc_change_x_y(10, 45) == (7.0710678119, 7.0710678119)
    assert utils.calc_change_x_y(10, 127) == (-6.0181502315, 7.9863551005)


def test_calc_angle() -> None:
    assert utils.calc_angle((0, 0), (0, 0)) == 0
    assert utils.calc_angle((1, 1), (2, 1)) == 0
    assert utils.calc_angle((2, 1), (1, 1)) == 180
    assert utils.calc_angle((1, 1), (2, 2)) == 45
    assert utils.calc_angle((-1, -1), (-2, -2)) == 225
    assert utils.calc_angle((-5, -2), (2, 3)) == 35.53767779197438


def test_null_stream() -> None:
    stream = utils.NullStream()
    assert stream.write() is None  # type: ignore[func-returns-value]
    assert stream.write("I NEED HELP") is None  # type: ignore[func-returns-value]  # noqa
    assert stream.write(kwarg="test") is None  # type: ignore[func-returns-value]  # noqa
    assert stream.write("NVM", key=42) is None  # type: ignore[func-returns-value]  # noqa
