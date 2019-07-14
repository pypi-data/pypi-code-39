# https://stackoverflow.com/questions/22623490/fastest-way-to-add-an-extra-row-to-a-groupby-in-pandas

# lastRowIndex = df.groupby(Group).Date.idxmax()
# rows = df.ix[lastRowIndex]
# df = pd.concat([df,rows], ignore_index=True)
# df = df.sort([Group, Date], ascending=True)
# return df


import pytest
from os.path import expanduser
import pandas as pd
import pyranges as pr
from pydbg import dbg

by_to_id = {"gene": "gene_id", "transcript": "transcript_id"}


def introns(df, exons, kwargs):

    by = kwargs.get("by", "gene")

    d = df[df.Feature.isin([by, "exon"])]

    id_column = by_to_id[by]

    by_ids = (d[id_column].shift() != d[id_column]).cumsum()
    d.insert(2, "ID", by_ids)

    exons = d[d.Feature == "exon"]
    genes = d[d.Feature == by]

    exons = exons[["ID", "Start", "End"]]
    genes = genes[["ID", "Start", "End"]]

    lastrows = exons.groupby("ID").last().reset_index()

    lastrows.loc[:, ["End", "Start"]] = -1

    exons = pd.concat([lastrows, exons, exons.tail(1)], ignore_index=True, sort=False).sort_values(["ID", "Start", "End"])








def test_introns():

    gr = pr.read_gtf(expanduser("~/move/test.gtf"))
    exons = gr.subset(lambda df: df.Feature == "exon").merge()

    df = gr.df

    df2 = introns(df, exons, {"by": "transcript"})
    dbg(df2)

    assert 0
