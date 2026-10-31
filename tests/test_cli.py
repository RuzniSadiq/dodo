from pathlib import Path

import pytest

from dodo import cli


@pytest.fixture
def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "db.json"
    monkeypatch.setenv("DODO_FILE", str(path))
    return path


def test_add_and_list(db: Path, capsys: pytest.CaptureFixture[str]) -> None:
    cli.main(["add", "buy milk"])
    cli.main(["list"])
    assert "buy milk" in capsys.readouterr().out


def test_ac_4_1_dodo_file_is_used_for_add_list_done(
    db: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    cli.main(["add", "pay rent"])
    cli.main(["done", "1"])
    cli.main(["list"])
    assert db.exists()
    assert "1. [x] pay rent" in capsys.readouterr().out


def test_ac_4_2_default_path_is_home_dodo_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("DODO_FILE", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert cli.db_path() == tmp_path / ".dodo.json"


def test_ac_4_3_path_resolved_at_call_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first, second = tmp_path / "a.json", tmp_path / "b.json"
    monkeypatch.setenv("DODO_FILE", str(first))
    cli.main(["add", "one"])
    monkeypatch.setenv("DODO_FILE", str(second))
    cli.main(["add", "two"])
    assert "one" in first.read_text() and "two" not in first.read_text()
    assert "two" in second.read_text()
