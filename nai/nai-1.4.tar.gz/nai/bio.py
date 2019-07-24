



#DMA Generate
def dna2rna(dna):
 strand = list(dna.upper())
 if "U" in strand:
  return {
    'type':'RNA',
    'length':len(strand),
    'sequence':''.join(strand)
  } 
  
 elif "T" in strand:
  return {
    'type':'DNA_2_RNA',
    'length':len(strand),
    'sequence':''.join("U".join(dna.upper().split("T")))
  }

def rna2dna(rna):
 strand = list(rna.upper())
 if "U" in strand:
  return {
    'type':'RNA_2_DNA',
    'length':len(strand),
    'sequence':''.join("T".join(rna.upper().split("U")))
  }

 elif "T" in strand:
  return {
    'type':'DNA',
    'length':len(strand),
    'sequence':''.join(strand)
  }