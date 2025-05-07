import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
    vus: 10, 
    duration: '10s', 
};

const authToken = "Bearer $2b$12$Ygf0LCIEIi51FoRdzHkJaOOWaUBIQoQ8hgPoJyA0ByN1g/ur.MwCi";

export default function () {
    const headers = {
        "Authorization": authToken,
    };

    const res = http.get('http://localhost:8000/users/admin', { headers: headers });
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
    sleep(1); 
}

export function handleSummary(data) {
    const rps = data.metrics.http_reqs.rate;
    const avgLatency = data.metrics.iteration_duration.values.avg;
    const maxLatency = data.metrics.iteration_duration.values.max;

    return {
        'stdout': `
          Running 10s test @ http://localhost:8000/users/admin
          10 threads and 10 connections
          Thread Stats Avg Stdev Max +/- Stdev
          Latency ${avgLatency !== undefined ? avgLatency.toFixed(2) : 'N/A'}ms ${data.metrics.http_req_duration.stdev !== undefined ? data.metrics.http_req_duration.stdev.toFixed(2) : 'N/A'}ms ${maxLatency !== undefined ? maxLatency.toFixed(2) : 'N/A'}ms
          Req/Sec ${rps} 
          ${rps*10} requests in 10s
        `,
    };
}
