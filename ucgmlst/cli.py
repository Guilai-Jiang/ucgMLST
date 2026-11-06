# SPDX-License-Identifier: GPL-3.0-or-later
"""Command line interface for the ucgMLST program."""

import os
from datetime import datetime

import click

from . import __version__, configure
from .configure import (check_tools, default_db_folder, missing_db_files,
                        set_db_folder)
from .read_seq import process_input_file
from .run_cgmlst import run_cgmlst
from .run_print import print_name
from .write_result import write_cgMLST, write_summary

SEPARATOR = '=' * 89


def _resolve_database(db):
    folder = db or default_db_folder()
    if folder is None:
        raise click.ClickException(
            'ucgMLST database not found. Pass --db PATH or set UCGMLST_DB.')
    try:
        set_db_folder(folder)
    except ValueError as exc:
        raise click.ClickException(str(exc))
    missing = missing_db_files(folder)
    if missing:
        raise click.ClickException(
            'Database directory {0} is missing: {1}'.format(folder, ', '.join(missing)))


@click.command()
@click.option('-q', '--query', required=True,
              help='Input genome file (fasta/fastq, optionally gzipped).')
@click.option('-p', '--prefix', required=True, help='Prefix for output files.')
@click.option('-o', '--outdir', required=True, help='Output directory for results.')
@click.option('-n', '--n_thread', default=8, type=int, help='Number of threads to use.')
@click.option('--db', default=None,
              help='Database directory. Defaults to $UCGMLST_DB, the conda '
                   'share directory, or ./db next to the source checkout.')
@click.version_option(__version__, prog_name='ucgmlst')
def main(query, prefix, outdir, n_thread, db):
    print_name()
    try:
        check_tools()
    except RuntimeError as exc:
        raise click.ClickException(str(exc))
    _resolve_database(db)

    print('Database directory : {0}'.format(configure.db_folder))
    outdir_abpath = os.path.abspath(outdir)
    if not os.path.exists(outdir_abpath):
        os.makedirs(outdir_abpath, exist_ok=True)
        print('The working directory does not exist. Created directory: {0}'.format(outdir_abpath))
    else:
        print('The working directory already exists: {0}'.format(outdir_abpath))

    fasta = process_input_file(query, outdir_abpath)
    print(SEPARATOR)
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('\033[33m{0} Running cgMLST typing and hierarchical clustering\033[0m'.format(current_time))
        show_data, alleles, hiercc = run_cgmlst(fasta, n_thread)
        write_cgMLST(outdir_abpath, prefix, alleles)
        summary_row = [prefix,
                       hiercc['Reference_genome'],
                       hiercc['Allelic_distance'],
                       hiercc['Hierarchical_cluster_level - HC6'],
                       hiercc['Hierarchical_cluster_level - HC650']]
        write_summary(outdir_abpath, prefix, summary_row)
        print('\n'.join(show_data))
        print(SEPARATOR)
    finally:
        if os.path.exists(fasta):
            os.remove(fasta)


if __name__ == '__main__':
    main()
