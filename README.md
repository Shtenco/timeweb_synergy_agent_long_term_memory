# SYNERGY / HIAI — долговременная память агента (исследование №13)

**Исследовательский прототип. Не production, не опубликованная статья и не проверенная долговременная память LLM.**

Два независимых опыта: (1) ограниченное окно точных строк из 12 фактов; (2) сохранность структурированных данных в SQLite при четырёх последовательных подключениях. Результаты второго опыта соответствуют технической базе статьи «Четыре сессии SQLite: фундамент памяти для AI-агента». Тема №13 **не входит в 12 ранее согласованных Timeweb Cloud концепций**, требуется отдельное согласование.

## Воспроизводимая установка

Нужен **Python 3.10+**; для базового стенда внешние зависимости не требуются.

```bash
git clone https://github.com/Shtenco/timeweb_synergy_agent_long_term_memory.git
cd timeweb_synergy_agent_long_term_memory
python -m unittest discover -s tests -v
python -m prototypes run 13 --seed 42 --out results/local
python experiments/sqlite_cross_session.py --out results/local/13_fixture.json
```

Последняя команда использует **искусственный корпус из 15 документов**, поэтому её результат нельзя выдавать за независимое повторение первоначального эксперимента на исходных файлах. Для реального корпуса передайте собственную директорию:

```bash
python experiments/sqlite_cross_session.py --corpus /path/to/15_markdown_articles --out results/local/13_real_corpus.json
```

В `results/reference/13_sqlite_cross_session_memory.json` лежит **архивный результат от 18.11.2026**, не свежий результат CI. Там 15 строк, четыре подключения, корректная проверка 15/15 и сохранение изменения статуса после открытия новой сессии. Проверка точная по ключам и SHA-256; *не проверяет* семантическую память, retrieval, извлечение причин решений, непрерывную неделю работы или восстановление агента после сбоя.

## Содержимое

- [`prototypes/scenarios/article13.py`](prototypes/scenarios/article13.py) — ограниченное окно хранения строк (синтетический опыт).
- [`prototypes/runner.py`](prototypes/runner.py) — CLI с воспроизводимыми JSON-артефактами.
- [`experiments/sqlite_cross_session.py`](experiments/sqlite_cross_session.py) — отдельная воспроизводимая проверка SQLite.
- [`tests/test_memory.py`](tests/test_memory.py) — unittest без сторонних пакетов.
- [`results/reference/13_sqlite_cross_session_memory.json`](results/reference/13_sqlite_cross_session_memory.json) — исторический первичный протокол.
- [`docs/RUNBOOK.md`](docs/RUNBOOK.md) — запуск и интерпретация.
- [`docs/EVIDENCE_SCOPE.md`](docs/EVIDENCE_SCOPE.md) — границы доказательств.
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — происхождение данных и права.
- [`docs/TIMEWEB_STATUS.md`](docs/TIMEWEB_STATUS.md) — статус согласования редакцией.

## Границы и безопасность

- Репозиторий не управляет реальными серверами, не вызывает внешние LLM и не отправляет данные в сеть.
- Исторические результаты не доказывают длительную память модели. Не путайте соединение SQLite и сессию агента.
- Не коммитьте приватные документы, токены и персональные данные. `results/local/` в `.gitignore`.
- MIT в [`LICENSE`](LICENSE) относится к авторскому исходному коду с соответствующими правами. Права третьих лиц, исходные данные и ещё не опубликованные рукописи требуют отдельной проверки.
- Префикс `timeweb_` — имя серии; **не доказательство согласования или официального партнёрства с Timeweb Cloud**.

## Следующая проверка гипотезы

Сравнить SQLite-only vs retrieval vs retrieval+summary на живой LLM; подготовить независимый корпус вопросов с проверяемой разметкой, многодневные сессии и сценарии устаревших/противоречивых фактов, latency, cost, ошибки фактического recall. До этого нельзя объявлять память модели доказанной.

## Цитирование

Используйте [`CITATION.cff`](CITATION.cff) и фиксируйте конкретный SHA коммита при публикации результатов.
