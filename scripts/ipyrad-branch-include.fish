#!/usr/bin/env fish

set paramsFile $argv[1]
set branchName $argv[2]
set includeList $argv[3]

set includeStr ""
for i in (cat $includeList)
  set sp (string split ' ' $i) 
  # Exclude empty lines and commented lines
  if test (string length $sp[1]) -gt 0; and test $sp[1] != '#' 
    set includeStr $includeStr $sp
  end
end

ipyrad -f -p $paramsFile -b $branchName $includeStr