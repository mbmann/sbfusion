#!/usr/bin/env bash

export PATH=python:~/nnlab/sbfusion/bin:$PATH

if [ $# -eq 0 ];
then
  echo "fastq2fusion.sh [transposonRefPath] [mouseRefPath] [fastqFilePath]"
  exit
fi

if [ ! $# -eq 3 ];
then
  echo "incorrect number of inputs"
  exit
fi

transposonrefpath="$1"
mouserefpath="$2"
inputfilepath="$3"

transposonrefprefix=${transposonrefpath%.*}
mouserefprefix=${mouserefpath%.*}

inputdir=`dirname $inputfilepath`
dataset=`echo $inputfilepath | rev | cut -d'.' -f2 | cut -d'/' -f1 | rev`

workdir=$inputdir/$dataset

mkdir -p $workdir

bowtie2 -p 32 --very-sensitive-local -x $transposonrefprefix $inputfilepath | samtools view -@ 4 -bS - | samtools sort -@ 8 -m 10G -o - - > $workdir/$dataset.onc2.bam
samtools index $workdir/$dataset.onc2.bam
samtools view $workdir/$dataset.onc2.bam onc2 | cigar.py S - 2> /dev/null | fastqstream.py minlen 20 - | bowtie2 -p 30 --very-sensitive -x $mouserefprefix - | samtools view -bS - | samtools sort -@ 5 -m 5G -o - - > $workdir/$dataset.sbInMouse.bam
samtools view -q 30 -F4 -h $workdir/$dataset.sbInMouse.bam | grep -v "XS:i:" | samtools view -bhS - | bamToBed -i  - > $workdir/$dataset.sbInMouse.filtered.bed
samtools view $workdir/$dataset.onc2.bam onc2 | sbf_fmtbed.py - $workdir/$dataset.sbInMouse.filtered.bed > $workdir/$dataset.fusion.bed 2> $workdir/$dataset.failed.bed
