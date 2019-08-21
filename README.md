# Introduction:
This script will parse a file with nucleotide sequence data and print certain sequences.

Sequence is defined by a given start codon and a list of possible end codons.

## Usage:
See help file for a list of usage examples:

## Syntax: 

	py -3 dna_sequence.py --input "PIK3CA Nucleotide Sequence.txt" --debug

## Output: 
```python
  > py -3 dna_sequence.py --input "PIK3CA Nucleotide Sequence.txt" --debug
  -I- Debug mode is on.
  -I- Input file: PIK3CA Nucleotide Sequence.txt
  -I- Output file: C:\Users\AllynH\Code\Git\dna_sequence\output[.txt|.csv]
  	-I- Found 632 codons
  	-I- Start codon: ATG Stop codons: ATT ATC ACT
  -I- Run time: 1.760136365890503 seconds
```

# Example: 
How to find the value of a codon that appears 100 places after the start of the 2nd sequence:

    py -3 dna_sequence.py --input "PIK3CA Nucleotide Sequence.txt" --sequence-index 1 --find-codon 1407 --debug


### Version:
	V1.0
## Owner: 

	Allyn Hunt