# SPDX-License-Identifier: GPL-3.0-or-later
"""Output writers for the ucgMLST program."""

import os


def write_cgMLST(outdir_abpath, prefix, alleles):
    output_name = prefix + '.alleles.profile'
    outfile = os.path.join(outdir_abpath, output_name)
    with open(outfile, 'wt') as fout:
        fout.write('#Query\t{0}\n'.format('\t'.join(sorted(alleles.keys()))))
        fout.write('{0}\t{1}\n'.format(
            prefix, '\t'.join(allele.get('value_md5', '-')
                              for _, allele in sorted(alleles.items()))))


def write_summary(outdir_abpath, prefix, summary_list):
    output_name = prefix + '.summary.txt'
    header = ['Query genome', 'Reference genome', 'Allelic distance', 'HC6', 'HC650']
    outfile = os.path.join(outdir_abpath, output_name)
    with open(outfile, 'wt') as fout:
        fout.write('\t'.join(header) + '\n')
        fout.write('\t'.join(str(value) for value in summary_list) + '\n')
