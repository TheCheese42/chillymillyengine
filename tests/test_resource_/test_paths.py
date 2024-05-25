from cme import resource_


def test_path_constants() -> None:
    assert resource_.DATA_PATH
    assert resource_.LOGS_PATH
    assert resource_.SETTINGS_PATH

    assert str(
        resource_.LOGS_PATH.resolve()
    ).startswith(
        str(resource_.DATA_PATH.resolve())
    )
