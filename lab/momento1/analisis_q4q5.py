#!/usr/bin/env python3
"""Análisis (no resultado oficial): dónde se va el tiempo de Q4 y Q5, servidor vs. cliente.

    venv/bin/python lab/momento1/analisis_q4q5.py --salida DIR [--host localhost]

Reproduce las mismas secuencias de parámetros que datos/medir_q4.py y datos/medir_q5.py (mismos
proveedores frío/caliente, random.Random(42), 100 ejecuciones) y, para cada ejecución, mide:
  - cliente: lo que cronometran los medir_q*.py (execute + fetchall con psycopg2);
  - servidor: Planning Time + Execution Time de EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) de la
    misma consulta con los mismos parámetros;
  - ida y vuelta mínima: SELECT 1 en la misma conexión.
Además guarda el plan con BUFFERS de una ejecución de cada escenario (texto) para ver qué nodo
consume el tiempo. Escribe DIR/analisis_q4q5.json y DIR/planes_q4q5.txt.
"""
import argparse
import json
import random
import statistics
import time
from pathlib import Path

import psycopg2

RAIZ = Path(__file__).resolve().parents[2]
import sys  # noqa: E402
sys.path.insert(0, str(RAIZ / "datos"))
import medir_q4  # noqa: E402  (solo SQL y constantes; main() no se ejecuta)
import medir_q5  # noqa: E402


def ids_q4(cur):
    cur.execute("""SELECT proveedor_id FROM ordenes.orden_compra WHERE estado = 'CONFIRMADA'
                   GROUP BY proveedor_id ORDER BY COUNT(*) DESC LIMIT 50""")
    hot = [r[0] for r in cur.fetchall()]
    cur.execute("""SELECT proveedor_id FROM ordenes.orden_compra WHERE estado = 'CONFIRMADA'
                   GROUP BY proveedor_id HAVING COUNT(*) BETWEEN 1 AND 20 LIMIT 50""")
    return hot, [r[0] for r in cur.fetchall()]


def ids_q5(cur):
    cur.execute("SELECT proveedor_id FROM ordenes.orden_compra GROUP BY proveedor_id ORDER BY COUNT(*) DESC LIMIT 50")
    hot = [r[0] for r in cur.fetchall()]
    cur.execute("""SELECT proveedor_id FROM ordenes.orden_compra GROUP BY proveedor_id
                   HAVING COUNT(*) BETWEEN 1 AND 20 LIMIT 50""")
    return hot, [r[0] for r in cur.fetchall()]


def secuencia(consulta, ids):
    rng = random.Random(42)
    if consulta == "Q4":
        return [(rng.choice(ids),) for _ in range(100)]
    return [(rng.choice(ids), rng.choice([0, 50, 100])) for _ in range(100)]


def p(v, q):
    return round(statistics.quantiles(v, n=100, method="inclusive")[q - 1], 3)


def resumen(v):
    return {"p50": p(v, 50), "p95": p(v, 95), "p99": p(v, 99)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--salida", required=True)
    ap.add_argument("--host", default="localhost")
    a = ap.parse_args()
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)
    conn = psycopg2.connect(dbname="escalables", user="postgres", password="postgres", host=a.host, port=5432)
    cur = conn.cursor()
    res, planes = {"host": a.host}, []
    for consulta, sql, elegir in (("Q4", medir_q4.QUERY_Q4, ids_q4), ("Q5", medir_q5.QUERY_Q5, ids_q5)):
        hot, cold = elegir(cur)
        for esc, ids in (("caliente", hot), ("frio", cold)):
            params = secuencia(consulta, ids)
            cliente, servidor, plan_ms, rtt = [], [], [], []
            for prm in params:   # en pares: cliente y EXPLAIN con el mismo parámetro, uno tras otro
                t = time.perf_counter()
                cur.execute(sql, prm)
                cur.fetchall()
                cliente.append((time.perf_counter() - t) * 1000)
                cur.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql}", prm)
                j = cur.fetchone()[0][0]
                servidor.append(j["Planning Time"] + j["Execution Time"])
                plan_ms.append(j["Planning Time"])
            for _ in range(100):
                t = time.perf_counter()
                cur.execute("SELECT 1")
                cur.fetchall()
                rtt.append((time.perf_counter() - t) * 1000)
            cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) {sql}", params[0])
            planes.append(f"===== {consulta} {esc} parámetros={params[0]}\n" + "\n".join(r[0] for r in cur.fetchall()))
            med_c, med_s = statistics.median(cliente), statistics.median(servidor)
            res[f"{consulta}_{esc}"] = {
                "cliente_ms": resumen(cliente), "servidor_ms": resumen(servidor),
                "planificacion_ms_mediana": round(statistics.median(plan_ms), 3),
                "select1_ms": resumen(rtt),
                "fraccion_servidor_p50": round(med_s / med_c, 2),
                "resto_cliente_red_p50_ms": round(med_c - med_s, 3)}
            print(f"{consulta} {esc:8} cliente p50 {med_c:.3f} ms | servidor p50 {med_s:.3f} ms "
                  f"({100 * med_s / med_c:.0f} %) | SELECT 1 p50 {statistics.median(rtt):.3f} ms", flush=True)
    (salida / "analisis_q4q5.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (salida / "planes_q4q5.txt").write_text("\n\n".join(planes) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
