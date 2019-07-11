import pysam

t = pysam.VariantFile("/home/brentp/src/hts-nim-tools/ceph-95.smoove.square.bcf")
for r in t.fetch("1", 2000, 900000):
    print r
