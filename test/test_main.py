import os
import subprocess
import tempfile

import yaml
from click.testing import CliRunner

from sequana_pipelines.hic.main import main

from . import test_dir

sharedir = f"{test_dir}/data"
reference = f"{sharedir}/chr1.fa"


def _run(tmp_path, *extra):
    runner = CliRunner()
    return runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            reference,
            "--working-directory",
            str(tmp_path / "wk"),
            "--force",
            *extra,
        ],
    )


def test_standalone_script(tmp_path):
    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            reference,
            "--working-directory",
            str(tmp_path / "wk"),
            "--force",
        ],
    )
    assert results.exit_code == 0


def test_standalone_script_bwa_split(tmp_path):
    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            reference,
            "--working-directory",
            str(tmp_path / "wk"),
            "--force",
            "--aligner-choice",
            "bwa_split",
        ],
    )
    assert results.exit_code == 0


def test_standalone_script_chromap(tmp_path):
    results = _run(tmp_path, "--aligner-choice", "chromap")
    assert results.exit_code == 0


def test_invalid_aligner_fails(tmp_path):
    results = _run(tmp_path, "--aligner-choice", "notanaligner")
    assert results.exit_code != 0


def test_missing_reference_fails(tmp_path):
    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--working-directory",
            str(tmp_path / "wk"),
            "--force",
        ],
    )
    assert results.exit_code != 0


def test_setup_artifacts(tmp_path):
    wk = tmp_path / "wk"
    results = _run(tmp_path)
    assert results.exit_code == 0
    # launcher and config produced
    assert (wk / "hic.sh").exists()
    assert (wk / "config.yaml").exists()
    # custom files copied into .sequana by main()
    for name in ("hic_qc.py", "hic_qc_style.css", "report_template.md"):
        assert (wk / ".sequana" / name).exists()


def test_config_reflects_options(tmp_path):
    wk = tmp_path / "wk"
    results = _run(tmp_path, "--aligner-choice", "chromap", "--enable-fastp")
    assert results.exit_code == 0
    cfg = yaml.safe_load((wk / "config.yaml").read_text())
    assert cfg["general"]["mapper"] == "chromap"
    assert cfg["fastp"]["do"] is True


def test_config_fastp_disabled_by_default(tmp_path):
    wk = tmp_path / "wk"
    results = _run(tmp_path)
    assert results.exit_code == 0
    cfg = yaml.safe_load((wk / "config.yaml").read_text())
    assert cfg["fastp"]["do"] is False


def test_version():
    runner = CliRunner()
    results = runner.invoke(main, ["--version"])
    assert results.exit_code == 0


def test_help():
    runner = CliRunner()
    results = runner.invoke(main, ["--help"])
    assert results.exit_code == 0
