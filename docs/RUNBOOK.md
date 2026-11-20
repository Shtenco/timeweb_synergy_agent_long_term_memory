# Запуск эксперимента №13

## Сравниваем две разные гипотезы

1. `prototypes/scenarios/article13.py` — скользящее окно из строк, демонстрация потери давних фактов; не LLM.
2. `experiments/sqlite_cross_session.py` — 4 последовательных SQLite-подключения, сохранение хешей и статуса записи. Это проверка SQLite, а не автономности агента.

## Команды

```bash
python --version
python -m unittest discover -s tests -v
python -m prototypes run 13 --seed 42 --out results/local
python experiments/sqlite_cross_session.py --out results/local/sqlite_fixture.json
python experiments/sqlite_cross_session.py --corpus /path/to/md_files --out results/local/sqlite_my_corpus.json
```

В `--corpus` передавайте только доступные вам Markdown-файлы, которые вправе использовать; скрипт читает файлы напрямую и никуда их не отправляет. Указанные пути будут записаны только в локальный JSON косвенно (через имена файлов), а сами тексты — в SQLite внутри временной директории, автоматически очищаемой после опыта.

## Проверка результата

В JSON должно быть четыре элемента `sessions`, каждый с `matches=record_count`. Поле `state_change_survived_restart` — `true`. `input_type=synthetic_fixture` не является измерением на статье HIAI. Исторический архивный протокол отдельно в `results/reference/`.

## Что НЕ проверяем

Векторные представления, суммаризацию, retrieval, память на неделю, правдивость ответов LLM и масштабирование. Предварительные результаты не даёт права делать вывод о превосходстве над долговременными агентами.
