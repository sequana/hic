
.. image:: https://badge.fury.io/py/sequana-hic.svg
     :target: https://pypi.python.org/pypi/sequana_hic

.. image:: https://github.com/sequana/hic/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/hic/actions/workflows

.. image:: https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg
    :target: https://pypi.python.org/pypi/sequana_hic
    :alt: Python 3.10 | 3.11 | 3.12

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI


This is the **Hi-C** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project.

:Overview: Hi-C pipeline to capture 3D chromatin interactions in a genome
:Input: Paired FastQ files and a reference genome in FASTA format
:Output: Cooler contact matrices, Hi-C QC reports, and a MultiQC summary
:Status: Beta
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

If you already have all requirements, install the package with pip::

    pip install sequana_hic --upgrade

You will need third-party tools (see Requirements below). Use apptainer images to avoid installing them locally.

Usage
~~~~~

Set up the pipeline directory with your input data and reference::

    sequana_hic --input-directory DATAPATH --reference-file genome.fa
    sequana_hic --input-directory DATAPATH --reference-file genome.fa --aligner-choice bwa_split

This creates a ``hic/`` directory containing the pipeline and configuration file. Execute the pipeline locally::

    cd hic
    sh hic.sh

See ``.sequana/profile/config.yaml`` to tune Snakemake behaviour (cores, cluster settings, etc.).

Usage with apptainer
~~~~~~~~~~~~~~~~~~~~~

With Apptainer, initiate the working directory as follows::

    sequana_hic --input-directory DATAPATH --reference-file genome.fa --use-apptainer

Images can be stored in a shared location::

    sequana_hic --input-directory DATAPATH --reference-file genome.fa --use-apptainer --apptainer-prefix ~/.sequana/apptainers

then::

    cd hic
    sh hic.sh

If running Snakemake manually, add apptainer options::

    snakemake -s hic.rules --cores 4 --use-apptainer --apptainer-prefix ~/.sequana/apptainers --apptainer-args "-B /home:/home"

By default the home directory is already bound. Additional paths can be set via::

    export APPTAINER_BINDPATH="-B /pasteur"

Requirements
~~~~~~~~~~~~

This pipeline requires the following executables (install via bioconda/conda):

- **bwa** — short-read aligner (default mapper)
- **samtools** — BAM/SAM manipulation
- **pairtools** — processing of Hi-C read pairs
- **cooler** — storage and analysis of Hi-C contact matrices
- **qc3c** — Hi-C quality control
- **fastqc** — raw read quality control
- **multiqc** — aggregate QC reports

Optional:

- **chromap** — fast Hi-C aligner (experimental, use ``--aligner-choice chromap``)
- **seqkit** — split FastQ files (required for ``--aligner-choice bwa_split``)


Pipeline description
~~~~~~~~~~~~~~~~~~~~

1. **FastQC** — quality control on raw reads
2. **Reference indexing** — BWA index build from the provided FASTA reference
3. **Alignment** — BWA-MEM alignment with Hi-C-specific options (``-5SP``), producing sorted BAM files
4. **Pairtools** — parse alignments into Hi-C contact pairs, sort, deduplicate, and split
5. **Cooler** — load pairs into a contact matrix and generate multi-resolution ``.mcool`` file
6. **qc3C** — Hi-C library quality assessment (ligation efficiency, distance distribution)
7. **Visualisation** — contact matrix PNG at 5 kb resolution
8. **MultiQC** — aggregated QC report


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.1.0     Migration to modern sequana_pipetools framework (get_shell/get_run,
          schema validation, apptainer support, Python 3.10+).
0.0.1     **First release.**
========= ====================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
