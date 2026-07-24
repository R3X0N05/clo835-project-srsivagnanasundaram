# predictions worksheet -- CLO835 Project 15
# srsivagnanasundaram | 126332246

## formula

time-to-kill = failureThreshold x periodSeconds
             + timeoutSeconds per poll (when endpoint is slow or hanging)

"never Ready but never killed" = readiness fails + liveness passes

## pre-filled examples

| STARTUP_DELAY_SECONDS | HEALTHZ_LATENCY_MS | startupProbe (period/threshold) | livenessProbe (period/timeout/threshold) | time-to-kill        | predicted outcome              |
|-----------------------|--------------------|----------------------------------|-------------------------------------------|---------------------|--------------------------------|
| 0                     | 0                  | 5s / 25                          | 10s / 3s / 3                              | 3 x 10 = 30s        | Ready, self-heals on wedge     |
| 90                    | 0                  | 5s / 25                          | 10s / 3s / 3                              | startup window 125s | Ready at ~90s, 0 restarts      |
| 0                     | 2000               | none                             | 2s / 1s / 1                               | 1 x 2 = 2s          | CrashLoopBackOff               |
| 180                   | 0                  | none (removed)                   | 10s / 3s / 3                              | 3 x 10 = 30s        | restart loop, CrashLoopBackOff |
| 0                     | 2500               | 5s / 25                          | 10s / 3s / 3                              | liveness passes     | 0/1 Ready, never killed        |

## live twist row (filled in during demo)

| STARTUP_DELAY_SECONDS | HEALTHZ_LATENCY_MS | startupProbe (period/threshold) | livenessProbe (period/timeout/threshold) | time-to-kill | predicted outcome |
|-----------------------|--------------------|----------------------------------|-------------------------------------------|--------------|-------------------|
|                       |                    |                                  |                                           |              |                   |