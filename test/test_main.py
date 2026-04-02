import os
import subprocess
import tempfile

from click.testing import CliRunner

from sequana_pipelines.hic.main import main

from . import test_dir

sharedir = f"{test_dir}/data"
reference = f"{sharedir}/Ld1S_chr1.fa"


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


def test_version():
    runner = CliRunner()
    results = runner.invoke(main, ["--version"])
    assert results.exit_code == 0


def test_help():
    runner = CliRunner()
    results = runner.invoke(main, ["--help"])
    assert results.exit_code == 0
