# улучшенная производительность
Running 10s test @ http://localhost:8000/users/admin
1 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency      25.12ms    9.45ms   88.76ms   88.23%
Req/Sec     398.40     59.80    480.00     85.42%
3972 requests in 10.06s, 686.32KB read
Requests/sec: 394.83
Transfer/sec: 68.22KB

Running 10s test @ http://localhost:8000/users/admin
5 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency      25.98ms   10.05ms   95.42ms   90.12%
Req/Sec      78.85     13.21     220.00     86.34%
3938 requests in 10.08s, 680.62KB read
Requests/sec: 390.67
Transfer/sec: 67.52KB

Running 10s test @ http://localhost:8000/users/admin
10 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency      24.89ms    9.67ms   94.28ms   89.37%
Req/Sec      40.15      6.82      55.00     70.15%
4013 requests in 10.02s, 693.45KB read
Requests/sec: 400.50
Transfer/sec: 69.21KB

# обычная производительность
Running 10s test @ http://localhost:8000/users/admin
1 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency      98.76ms   82.14ms  752.34ms   91.45%
Req/Sec     126.45     42.80    180.00     72.34%
1203 requests in 10.04s, 207.92KB read
Requests/sec: 119.82
Transfer/sec: 20.71KB

Running 10s test @ http://localhost:8000/users/admin
5 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency     102.34ms   57.62ms  398.76ms   89.23%
Req/Sec      21.45      8.45      35.00     70.88%
1042 requests in 10.08s, 180.06KB read
Requests/sec: 103.37
Transfer/sec: 17.86KB

Running 10s test @ http://localhost:8000/users/admin
10 threads and 10 connections
Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency     107.22ms   60.15ms  498.34ms   86.77%
Req/Sec      11.05      4.89      18.00     60.12%
982 requests in 10.05s, 169.69KB read
Requests/sec: 97.71
Transfer/sec: 16.89KB

# Отчёт о нагрузочном тестировании

## Конфигурация теста
- **URL**: `http://localhost:8000/users/admin`
- **Метод**: GET с аутентификацией (Lua-скрипт)
- **Тестовые сценарии**:
  - 1 поток, 10 соединений
  - 5 потоков, 10 соединений
  - 10 потоков, 10 соединений
- **Длительность**: 10 секунд для каждого теста

## Результаты тестирования

### 1. Тест с 1 потоком (10 соединений)
| Метрика          | Значение             |
|------------------|----------------------|
| Средняя задержка | 98.76 ms ± 82.14 ms  |
| Макс. задержка   | 752.34 ms            |
| Запросов/сек     | 126.45 ± 42.80       |
| Всего запросов   | 1203                 |
| Пропускная способность | 119.82 RPS  |
| Передача данных  | 20.71 KB/sec         |

---

### 2. Тест с 5 потоками (10 соединений)
| Метрика          | Значение             |
|------------------|----------------------|
| Средняя задержка | 102.34 ms ± 57.62 ms |
| Макс. задержка   | 398.76 ms            |
| Запросов/сек     | 21.45 ± 8.45         |
| Всего запросов   | 1042                 |
| Пропускная способность | 103.37 RPS  |
| Передача данных  | 17.86 KB/sec         |


---

### 3. Тест с 10 потоками (10 соединений)
| Метрика          | Значение             |
|------------------|----------------------|
| Средняя задержка | 107.22 ms ± 60.15 ms |
| Макс. задержка   | 498.34 ms            |
| Запросов/сек     | 11.05 ± 4.89         |
| Всего запросов   | 982                  |
| Пропускная способность | 97.71 RPS   |
| Передача данных  | 16.89 KB/sec         |

---

## выводы

1. **Зависимость RPS от потоков**:
   - Наибольшая пропускная способность (119.82 RPS) достигнута при 1 потоке
   - Увеличение потоков приводит к падению RPS на ~13-18% на каждый +5 потоков

2. **Задержки**:
   ```python
   Средняя задержка:
   1 поток:  98.76 ms
   5 потоков: +3.6% 
   10 потоков: +8.6%