from dodo import cli

def test_add_and_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "DB", tmp_path / "db.json")
    cli.main(["add", "buy milk"])
    cli.main(["list"])
    assert "buy milk" in capsys.readouterr().out