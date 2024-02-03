from compiler.main import read_source_code, process_command


def test_read_source_code_from_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("print('Hello, World')")

    assert read_source_code(str(test_file)) == "print('Hello, World')"


def test_read_source_code_from_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin.read', lambda: "print('Hello, stdin')")

    assert read_source_code(None) == "print('Hello, stdin')"


def test_process_command_unknown():
    assert process_command("unknown") == 1
