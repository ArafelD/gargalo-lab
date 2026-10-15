import tempfile
import unittest
from pathlib import Path

from gargalo_lab import cli, verify


class Reference(unittest.TestCase):
    def test_all_reference_results_of_the_article_hold(self):
        rows = verify.run_checks()
        failed = [r for r in rows if not r["ok"]]
        self.assertEqual(failed, [], failed)
        self.assertEqual({r["lab"] for r in rows}, {f"{i:02d}" for i in range(1, 9)})


class Cli(unittest.TestCase):
    def test_numeric_alias_and_output_files(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(cli.main(["all", "--out", d]), 0)
            names = {p.name for p in Path(d).iterdir()}
        for prefix in ("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_"):
            self.assertTrue(any(n.startswith(prefix) for n in names), prefix)

    def test_verify_command_returns_zero(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(cli.main(["verify", "--out", d]), 0)
            self.assertTrue((Path(d) / "REFERENCE_CHECK.md").exists())


if __name__ == "__main__":
    unittest.main()
