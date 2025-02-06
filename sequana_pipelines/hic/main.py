#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/sequana
#  Documentation: http://sequana.readthedocs.io
#  Contributors:  https://github.com/sequana/sequana/graphs/contributors
##############################################################################
import os

import rich_click as click
import click_completion

click_completion.init()


from sequana_pipetools.options import *
from sequana_pipetools import SequanaManager


NAME = "hic"

help = init_click(NAME, groups={
    "Pipeline Specific": [
        "--aligner-choice",
        "--reference-file"
       ],
        }
)
@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--aligner-choice",
    "mapper",
    default="bwa",
    type=click.Choice(["bwa", "bwa_split", "minimap2", "bowtie2"]),
    help="""Choose one of the valid mapper. bwa_split is experimental. it first split the fastq files in chunks of 1Mreads,
aligns the reads with bwa and merge back the sub BAM files. Should be equivalent to using bwa but could be used on
cluster to speed up analysis.""",
)
@click.option("--reference-file", required=True, help="You input reference file in fasta format")
def main(**options):


    # the real stuff is here
    manager = SequanaManager(options, NAME)
    options = manager.options

    # creates the working directory
    manager.setup()

    cfg = manager.config.config

    # --------------------------------------------------- input  section
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag

    cfg.general.mapper = options.mapper
    cfg.general.reference_file = os.path.abspath(options.reference_file)
    manager.exists(cfg.general.reference_file)

    # Given the reference, let us compute its length and the index algorithm
    from sequana import FastA

    f = FastA(cfg.general.reference_file)
    N = f.get_stats()["total_length"]

    # seems to be a hardcoded values in bwa according to the documentation
    if N >= 2000000000:
        cfg["bwa"]["index_algorithm"] = "bwtsw"
        cfg["bwa_split"]["index_algorithm"] = "bwtsw"
    else:
        cfg["bwa"]["index_algorithm"] = "is"
        cfg["bwa_split"]["index_algorithm"] = "is"

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()



    import shutil
    shutil.copy("collateral", self.workdir / ".sequana")





if __name__ == "__main__":
    main()
