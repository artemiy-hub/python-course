def test_input_example(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'Анна')
    import input_example
    captured = capsys.readouterr()
    assert "Привет, Анна!" in captured.out 