#!/usr/bin/env fish

set dir $argv[1]
set files (ls $dir/*.out)
set fileCount (count $files)
set finished 0
for f in $files 
  set lastLine (tail -n2 $f)
  set msg (string split ' ' $lastLine)[1..5]
  if test "$msg" = "Final results printed to file" 
    set finished (math $finished + 1)
  else
    echo (basename $f) "incomplete"
  end
end
echo "$finished/$fileCount complete"
if test $finished = $fileCount 
  echo "Success! All runs complete."
end