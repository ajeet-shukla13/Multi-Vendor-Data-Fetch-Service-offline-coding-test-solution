Load Test Analysis (k6)

I conducted a 10-second load test using [k6](https://k6.io) with 10 virtual users sending requests to the FastAPI job service.

For the test load-test.js script was used
Target endpoints:
1 POST /jobs
2 GET /jobs/{request_id}

Results:
1 Total requests: 200 (100 job creations + 100 status polls)
2 100% success rate for all checks
3 No HTTP failures (0% request errors)
4 Average response time: 35.17ms
5 Peak response time (p95): 185.24ms
6 Data Sent: 30 KB | Data Received: 33 KB
