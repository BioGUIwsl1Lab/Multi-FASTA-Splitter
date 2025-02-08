#!/usr/bin/python3
import sys
import textwrap
# Insert txt file
input_file = sys.argv[1]
file = open(input_file, 'r')
# Stripe leading and trailing characters in each line
lines = list(map(lambda line: str(line).strip(), file))
# close the file
file.close()
# retrieve the header
header = lines[0]
# retrieve the sequence
seq = "".join(lines[1:])
# export to fasta
wrapped_seq = textwrap.fill(seq,width=int(sys.argv[2]))
with open(input_file,'w') as f:
  f.writelines(f"{header}\n{wrapped_seq}\n")
