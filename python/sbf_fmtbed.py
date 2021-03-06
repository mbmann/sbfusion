#!/usr/bin/env python

# Copyright (C) 2016 Justin Y. Newberg
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

def sam_flag(x):
  binstr = bin(x)[2:][::-1]
  values = [2**i for i in xrange(len(binstr)) if binstr[i]=='1' ]
  return values

fid=sys.stdin

index={}
while True:
  line=fid.readline().strip('\n')
  if line=='':break
  row=line.split('\t')
  strand='-' if 16 in sam_flag(int(row[1])) else '+'
  index[row[0]]='.'.join([row[2],row[3],strand,row[5]])


fid=open(sys.argv[-1])

while True:
  line=fid.readline().strip('\n')
  if line=='':break
  row=line.split('\t')
  row[3]=index[row[3]]
  pos=int(row[3].split('.')[1])

  output="stdout"
  if pos<531:output="stderr"
  if (pos>700)&(pos<1215):output="stderr"
  if (pos>1398)&(pos<1528):output="stderr"
  if pos>1961:output="stderr"
  if int(row[4])<30:output="stderr"
  if row[0]=='onc2':output="stderr"

  if (pos>531)&(pos<=700):row[3]="SA_exon"
  if (pos>1210)&(pos<1400):row[3]="LunSD"
  if (pos>1528)&(pos<1961):row[3]="exon_En2SA"

  row[4]="1"
  if output=="stdout":sys.stdout.write('\t'.join(row)+'\n')
  else:sys.stderr.write('\t'.join(row)+'\n')

