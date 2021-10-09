# Phylogenetic
 Makes a phylogenetic tree based on the UPGMA-method
 **Usage:**
 sequences in a dict like so
 ```python3
 sequences = {
 "Sibirisk tiger":"GCACCGTACCCCCCTCACTTTGTGGCACCTCTATATAATGCTACTAGGCTGCCG",
 "Sydkinesisk tiger":"ACGCCGCACTCCCTCCGCTTTGTGGCATCTCTACATGATGCCATCAAGCCACTG",
 "Indokinesisk tiger I":"GTACCGCACCCCCCTCGCTTTATAGCACTTCTATATAATGCTACTAGGCTGCTG",
 "Indokinesisk tiger II":"GCGCCGCACCCCCCTCGCTTTGTGATATCTTTACGTAATGCTACTAGGCTGCCG",
 "Sumatra tiger":"ACGCCGCACCCCCTTCGCTTTGCGGCGTCTCTACATAACGCCATTAGGTTGCTG",
 "Bengalsk tiger":"GCGCCGGACCCCCCTTGCTCTGTGGCATCTCTACATAACGTCATTAGACTGCTG"
 }
 ```
 The numbers can be displayed on top, or on the bottom by changing the boolean `reversed`. And the trees roots can also be cut to prettify it.
 `root.prettyTree(reversed = False, cut = 6)`

 With the following settings, it constructs the tree like so.
