#!/usr/bin/env fish

set paramsFile $argv[1]
set branchName $argv[2]
set excludeList $argv[3]

set excludeStr ""
for i in (cat $excludeList)
  set sp (string split ' ' $i) 
  # Exclude empty lines and commented lines
  if test (string length $sp[1]) -gt 0; and test $sp[1] != '#' 
    set excludeStr $excludeStr $sp
  end
end

ipyrad -p $paramsFile -b $branchName - $excludeStr
