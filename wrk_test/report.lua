
-- Test instruction ：wrk -t16 -c100 -d5s -sreview_digress_list.lua --latency htt://127.0.0.1:8081
wrk = { 
   scheme = “http”, 
   host = “localhost”, 
   port = nil,
   method = “GET”,
   path = “/”,
   headers = {},
   body = nil,
   thread = <userdata>,
 }


-- wrk.path = "/app/{appId}/review_digress_list"
function request()
-- Dynamically generate the... For each request url
-- local requestPath = string.gsub(wrk.path,"{appId}",math.random(1,10))
-- Returns the complete string of the request ：http://127.0.0.1//app/666/review_digress_list
-- return wrk.format(nil, requestPath)
end



-- 1. setup 
-- a random server address to each thread
--The setup phase begins after the target IP address has been resolved 
--and all threads have been initialized but not yet started.
local addrs = nil

function setup(thread)
   if not addrs then
      addrs = wrk.lookup(wrk.host, wrk.port or "http")
      for i = #addrs, 1, -1 do
         if not wrk.connect(addrs[i]) then
            table.remove(addrs, i)
         end
      end
   end

   thread.addr = addrs[math.random(#addrs)]
end

function init(args)
   local msg = "thread addr: %s"
   print(msg:format(wrk.thread.addr))
end

-- 2.running
-- 2.1 init 2.2 request 2.3 response

-- done() function that prints latency percentiles as CSV
done = function(summary, latency, requests)
    io.write("------------------------------\n")
    for _, p in pairs({ 50, 90, 99, 99.999 }) do
       n = latency:percentile(p)
       io.write(string.format("%g%%,%d\n", p, n))
    end
 end