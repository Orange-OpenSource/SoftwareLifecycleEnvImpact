from api.data_model import TaskInput


def test_task_input() -> None:
    """"""
    t = TaskInput(
        name="Test name",
        kind="Test kind",
        value="Test value",
        task_id=0,
    )
    assert t.name == "Test name"
    assert t.kind == "Test kind"
    assert t.value == "Test value"
    assert t.task_id == 0
