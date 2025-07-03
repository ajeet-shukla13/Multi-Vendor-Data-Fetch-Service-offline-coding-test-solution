import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  vus: 10,         
  duration: '10s',
};

export default function () {
  const payload = JSON.stringify({
    type: "sync",
    name: " Test ",
    email: "ajeet@king.com"
  });

  const headers = { 'Content-Type': 'application/json' };


  const postRes = http.post('http://host.docker.internal:8000/jobs', payload, { headers });
  check(postRes, {
    'POST status is 200': (r) => r.status === 200,
    'request_id exists': (r) => r.json('request_id') !== undefined,
  });

  const requestId = postRes.json('request_id');
  sleep(1); 

  const getRes = http.get('http://host.docker.internal:8000/jobs/${requestId}');
  check(getRes, {
    'GET status is 200': (r) => r.status === 200,
  });
}