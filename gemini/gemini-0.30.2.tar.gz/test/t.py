import cyvcf2

for v in cyvcf2.VCF("test.query.vcf"):
    print v.gt_bases
    1/0
