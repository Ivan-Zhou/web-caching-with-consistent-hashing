#  in multiple connections durations and threads. 

for duration in 10s 1m 10m 1h
do 
  for connections in 100 200 300 400 500 600
  do
    for thread in 1 2 3 4 5
    do
      wrk -d$duration -c$connections -t$thread -s wrk-script.lua http://localhost:4001/beacon/0001/demo-load-test/test/web
    done
  done
done