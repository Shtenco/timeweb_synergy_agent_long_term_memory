import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from prototypes.scenarios.article13 import retain_facts, run
from experiments.sqlite_cross_session import experiment, load_corpus

class MemoryExperimentTests(unittest.TestCase):
    def test_window_boundary_and_recent_fact(self):
        self.assertEqual(retain_facts(['old','middle','new'],2),['middle','new'])
        self.assertEqual(run(capacity=4)['memory_size'],4)
        with self.assertRaises(ValueError):retain_facts(['a'],0)

    def test_sqlite_four_connections(self):
        docs={f'{i:02}.md':f'# Doc {i}\ncontents {i}' for i in range(15)}
        result=experiment(docs, 'test_fixture')
        self.assertEqual(len(result['sessions']),4)
        self.assertTrue(result['state_change_survived_restart'])
        self.assertTrue(all(x['matches']==15 for x in result['sessions']))

    def test_reload_with_user_supplied_corpus(self):
        with TemporaryDirectory() as td:
            folder=Path(td)
            (folder/'08_test.md').write_text('# Проверка\nНовый текст',encoding='utf-8')
            corpus,kind=load_corpus(folder)
            self.assertEqual(kind,'user_supplied_real_corpus')
            self.assertEqual(experiment(corpus,kind)['record_count'],1)

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):experiment({})

if __name__=='__main__':unittest.main()
