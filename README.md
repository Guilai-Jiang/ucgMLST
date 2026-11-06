# ucgMLST

[![build](https://github.com/Guilai-Jiang/ucgMLST/actions/workflows/build-conda.yml/badge.svg)](https://github.com/Guilai-Jiang/ucgMLST/actions/workflows/build-conda.yml)
[![license](https://img.shields.io/badge/license-GPL--3.0--or--later-blue.svg)](LICENSE)

Updated core-genome MLST (cgMLST) and HierCC assignment for Gram-positive
cocci: allele calling for a configurable core-genome scheme, md5 allele
fingerprints, reference-profile matching and hierarchical cluster assignment.

## Requirements

Python ≥ 3.9 and, on `PATH`:

| Tool | Version |
|---|---|
| `makeblastdb`, `blastn` | ≥ 2.14 |
| `diamond` | ≥ 2.2 |

## Install

```bash
conda create -n ucgmlst -c conda-forge -c bioconda \
  python=3.10 blast diamond numpy pandas numba biopython click
conda activate ucgmlst
pip install .
```

## Database

The database is distributed as a release asset:

```bash
curl -LO https://github.com/Guilai-Jiang/ucgMLST/releases/download/db-v1.0/ucgmlst-db-1.0.tar.gz
mkdir -p ~/ucgmlst-db && tar xzf ucgmlst-db-1.0.tar.gz -C ~/ucgmlst-db
export UCGMLST_DB=~/ucgmlst-db
```

It is located in this order: `--db` → `$UCGMLST_DB` →
`$CONDA_PREFIX/share/ucgmlst/db` → `./db`.

| File | Content |
|---|---|
| `staph_aureus.cgMLST` | core gene identifiers |
| `MLSTdb0.1.fasta` | reference allele for every core gene |
| `new_profile_md5.csv` | md5 allele profiles of the reference genomes |
| `new_HierCC.HierCC` | HierCC levels for the same genomes |

The first run writes `new_profile_md5.csv.pkl` (about 230 MB); later runs start
in ~2 s instead of ~20 s.

## Usage

```bash
ucgmlst -q genome.fna.gz -p sample -o results -n 8
```

| Option | Meaning |
|---|---|
| `-q, --query` | input genome: fasta/fastq, optionally gzipped |
| `-p, --prefix` | output file prefix |
| `-o, --outdir` | output directory |
| `-n, --n_thread` | threads (default 8) |
| `--db` | database directory |

## Output

| File | Content |
|---|---|
| `*.alleles.profile` | md5 allele profile, one column per locus (GrapeTree compatible) |
| `*.summary.txt` | reference genome, allelic distance, HC6, HC650 |

## Citation

> Jiang G, Guo C, Hua Y, Wu C, Li S, Wang Y, Zhao J, Ji L, Cheng Y, Zhou Z,
> Wu X, Li H. **Large-scale genomic analysis places Chinese CC398 as a
> persistent human-associated MSSA lineage apart from the dominant global
> LA-MRSA clade.** *mSystems*. 2026;11(10).
> [doi:10.1128/msystems.00621-26](https://doi.org/10.1128/msystems.00621-26)

## License

GPL-3.0-or-later. See [LICENSE](LICENSE) and [COPYING](COPYING). Database terms
are described in [docs/DATABASE-LICENSES.md](docs/DATABASE-LICENSES.md).

## Contact

Questions, bug reports and suggestions are very welcome. Please open an
[issue](https://github.com/Guilai-Jiang/ucgMLST/issues) or write to
[gljiang@alu.suda.edu.cn](mailto:gljiang@alu.suda.edu.cn).
