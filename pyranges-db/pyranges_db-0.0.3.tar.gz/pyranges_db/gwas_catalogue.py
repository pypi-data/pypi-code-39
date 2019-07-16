import pandas as pd

import pyranges as pr


def gwas_catalogue():

    f = "https://www.ebi.ac.uk/gwas/api/search/downloads/alternative"
    df = pd.read_csv(f, sep="\t", low_memory=False)

    df = df.rename(columns={"CHR_ID": "Chromosome", "CHR_POS": "Start"})

    bad_locs = df.Start.isnull() | df.Chromosome.isnull() | df.Start.str.contains("x") | df.Chromosome.str.contains("x")
    df = df[~bad_locs]

    # split multiple starts/chromosomes into multiple rows
    new_starts = pd.DataFrame(df.Start.str.split(';', expand=True)).stack().reset_index(level=1, drop=True)
    new_chromosomes = pd.DataFrame(df.Chromosome.str.split(';', expand=True)).stack().reset_index(level=1, drop=True)
    df = df.reindex(new_starts.index)
    df.loc[:, "Start"] = new_starts
    df.loc[:, "Chromosome"] = new_chromosomes

    df = df.copy()
    df.loc[:, "Start"] = df.Start.astype(int)
    most_interesting_cols = ["Chromosome", "Start", "REGION", "SNP_GENE_IDS", "P-VALUE", "OR or BETA", "MAPPED_GENE", "MAPPED_TRAIT"]
    columns = [c for c in df.columns if c not in most_interesting_cols]

    df = df[most_interesting_cols + columns]

    df.insert(2, "End", df.Start + 1)

    return pr.PyRanges(df)
