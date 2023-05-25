#!/usr/bin/env fish

set dir $argv[1]

for i in $dir/*.out
  set likelihood (grep "mcmc iteration: 0 .* LnL: " $i)
  echo $likelihood
end