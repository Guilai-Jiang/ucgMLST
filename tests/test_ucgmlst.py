# SPDX-License-Identifier: GPL-3.0-or-later
"""Unit tests that do not need the reference database or external tools."""

from click.testing import CliRunner

from ucgmlst import __version__
from ucgmlst.cli import main
from ucgmlst.read_seq import fastq_to_fasta


def test_fastq_to_fasta_keeps_header_marker():
    content = "@read1\nACGTACGT\n+\nIIIIIIII\n"
    assert fastq_to_fasta(content) == ">read1\nACGTACGT\n"


def test_cli_version():
    result = CliRunner().invoke(main, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_rejects_invalid_database(tmp_path, monkeypatch):
    import ucgmlst.configure as configure

    monkeypatch.setattr(configure, 'exe', {tool: '/bin/true' for tool in configure.TOOLS})
    query = tmp_path / 'genome.fna'
    query.write_text('>c\nACGT\n')
    result = CliRunner().invoke(
        main, ['-q', str(query), '-p', 'x', '-o', str(tmp_path / 'out'),
               '--db', str(tmp_path / 'missing')])
    assert result.exit_code != 0
    assert 'Not a ucgMLST database directory' in result.output
