#!/usr/bin/env fish

set program $argv[1]
set indir $argv[2]

# Check that program args are valid
if not contains -- $program "ustacks" "sstacks"
  echo "Error: \"$program\" is an invalid program argument"
  exit 1
end

set popmap (sed -n 's/^popmap: //p' $indir/config.txt)
set expectedSampleNum (grep -v '^\s*$' $popmap | wc -l)
set fileNum (ls $indir/logs/$program-*.out | wc -l)

# Make sure the number of log files matches the number of samples in popmap
if test $expectedSampleNum -eq $fileNum
  echo "Success: Log file number matches popmap sample number"
else
  echo "Error: Unexpected number of log files"
  exit 1
end

for file in $indir/logs/$program-*.out
  
  # Check that first line begins with Assembling and store the sample id
  set firstLine (head -n 1 $file)
  set -l firstLine (string split " " $firstLine)
  if test $firstLine[1] = "Assembling"
    set id $firstLine[2] 
  else
    echo "Error: Unexpected output at first line in $file"
    exit 1
  end

  # Check that the last line says "ustacks is done."
  set lastLine (tail -n 1 $file)
  if [ $lastLine = "$program is done." ]
    echo "$id done"
  end
end

for file in $indir/logs/$program-*.out
  # Check that the last line says "ustacks is done."
  set lastLine (tail -n 1 $file)
  if [ $lastLine != "$program is done." ]
    echo "$id unfinished"
  end
end