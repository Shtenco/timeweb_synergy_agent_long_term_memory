#!/usr/bin/env python3
"""SQLite persistence across 4 connections (not LLM semantic memory).

Default input: 15 deterministic *synthetic* fixture docs.
To reproduce the historical 15-document corpus test, pass --corpus to
an accessible directory containing the article Markdown source files.
The stored historical result is not replaced by new runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def load_corpus(root: Path | None):
    if root is None:
        return {f"article_{i:02}.md": f"# Тестовый документ {i:02}\nСодержимое {i:02}" for i in range(1, 16)}, 'synthetic_fixture'
    if not root.is_dir():
        raise ValueError(f"Директория корпуса не найдена: {root}")
    files = sorted(root.glob('*.md'))
    if not files:
        raise ValueError('Корпус не содержит Markdown-файлов (*.md)')
    return {p.name: p.read_text(encoding='utf-8') for p in files}, 'user_supplied_real_corpus'


def checksum(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def experiment(corpus: dict[str, str], input_type: str = 'user_supplied_real_corpus') -> dict:
    if not corpus:
        raise ValueError('Пустой корпус')
    article_names = sorted(corpus)
    target_name = next((n for n in article_names if n.startswith('08_')), article_names[0])
    rows = [(n, txt.splitlines()[0].lstrip('# ').strip(), checksum(txt), 'approved') for n, txt in sorted(corpus.items())]
    snapshots=[]
    with tempfile.TemporaryDirectory() as td:
        db=Path(td) / 'facts.sqlite'
        con=sqlite3.connect(db)
        con.execute('CREATE TABLE facts(article_name TEXT PRIMARY KEY, title TEXT, sha256 TEXT, state TEXT)')
        con.executemany('INSERT INTO facts VALUES (?,?,?,?)', rows)
        con.commit(); con.close()
        for idx in range(1,5):
            # A distinct SQLite connection for each session, no live LLM or agent.
            con=sqlite3.connect(db)
            actual=dict(con.execute('SELECT article_name,sha256 FROM facts'))
            correct=sum(actual.get(n)==checksum(txt) for n,txt in corpus.items())
            snapshots.append({'session':idx,'fact_count':len(actual),'matches':correct})
            if idx==2:
                con.execute('UPDATE facts SET state=? WHERE article_name=?',('requires_correction',target_name))
                con.commit()
            con.close()
        con=sqlite3.connect(db)
        state=con.execute('SELECT state FROM facts WHERE article_name=?',(target_name,)).fetchone()[0]
        con.close()
    survived=state=='requires_correction'
    assert all(x['matches']==len(corpus) and x['fact_count']==len(corpus) for x in snapshots)
    assert survived
    return {
        'article':'13', 'evidence_type':'measured_SQLite_persistence_across_connections',
        'input_type':input_type, 'sessions':snapshots,'record_count':len(corpus),
        'state_change_survived_restart':survived,
        'update_target':target_name,'created_utc':datetime.now(timezone.utc).isoformat(),
        'environment':{'python':platform.python_version(),'platform':platform.platform()},
        'limitations':['Tests SQL persistence over new connections, not real LLM long-term memory',
                       'No multi-day tasks, vector search, context compression or semantic recall',
                       'Uses an in-process four-connection experiment, not separate OS processes'],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus',type=Path,help='Directory containing source *.md files (optional)')
    parser.add_argument('--out',type=Path,default=Path('results/local/13_sqlite_run.json'))
    opts=parser.parse_args()
    corpus,kind=load_corpus(opts.corpus)
    result=experiment(corpus,kind)
    opts.out.parent.mkdir(parents=True,exist_ok=True)
    opts.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'result':str(opts.out),'records':result['record_count'],'sessions':len(result['sessions']),'type':kind},ensure_ascii=False))

if __name__=='__main__':
    main()
