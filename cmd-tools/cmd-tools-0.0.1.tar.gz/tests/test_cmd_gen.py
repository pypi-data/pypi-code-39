from command import hello


def test_feature(runner):
    result = runner.invoke(hello)
    assert result.output == 'hello'
