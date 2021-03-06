#!/usr/bin/python
# filename: msa.py


#
# Copyright (c) 2015 Bryan Briney
# License: The MIT license (http://opensource.org/licenses/MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import os
import re
import subprocess as sp


def align(seqs, fasta):
    '''
    Makes a multiple sequence alignment.

    Input
    seqs: sequences to be aligned (as biopython SeqIO objects)
    fasta: path to use for the alignment input file

    Output
    path to the alignment file generated by MUSCLE
    '''
    build_alignment_input(seqs, fasta)
    return muscle(fasta, len(seqs))


def build_alignment_input(seqs, fasta):
    flist = []
    for s in seqs:
        seq_id = re.sub('[:;]', '_', s.id)
        flist.append('>{}\n{}'.format(seq_id, str(s.sequence).upper()))
    open(fasta, 'w').write('\n'.join(flist))


def muscle(fasta, count):
    output_dir = os.path.dirname(fasta)
    output_name = '{}_aligned.aln'.format(os.path.basename(fasta).replace('.fasta', ''))
    output = os.path.join(output_dir, output_name)
    if count < 100:
        muscle_cline = 'muscle -in {} -out {}'.format(fasta, output)
    elif count < 1000:
        muscle_cline = 'muscle -maxiters 2 -in {} -out {}'.format(fasta, output)
    else:
        muscle_cline = 'muscle -maxiters 1 -diags -in {} -out {}'.format(fasta, output)
    m = sp.Popen(muscle_cline, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    stdout, stderr = m.communicate()
    return output
