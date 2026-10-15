import tempfile
import unittest
from pathlib import Path

import numpy as np

from gargalo_lab import custody, deadman, insider, triangulation as tri


class Lab05Triangulation(unittest.TestCase):
    def test_scale_ambiguity_same_pixels(self):
        self.assertTrue(tri.ambiguity_demo()["identical_pixels"])

    def test_known_ruler_recovers_scale_without_noise(self):
        h = tri.estimate_height(0.37, 0.0, np.random.default_rng(1))
        self.assertAlmostEqual(h, tri.TRUE_PERSON_M, places=6)

    def test_geometry_and_noise_matter(self):
        rows = {(r["baseline_m"], r["noise_px"]): r["mean_abs_error_cm"] for r in tri.monte_carlo(600)}
        self.assertGreater(rows[(0.1, 2.0)], 5 * rows[(1.5, 0.25)])
        self.assertGreater(rows[(0.5, 2.0)], rows[(0.5, 0.25)])


class Lab06DeadMan(unittest.TestCase):
    def test_naive_triggers_after_timeout_and_checkin_resets(self):
        s = deadman.Switch(timeout_h=5)
        s.tick(4.9)
        self.assertEqual(s.state, deadman.State.ARMED)
        s.checkin(4.9)
        s.tick(9.0)
        self.assertEqual(s.state, deadman.State.ARMED)
        s.tick(10.0)
        self.assertEqual(s.state, deadman.State.TRIGGERED)

    def test_hardened_needs_quorum(self):
        s = deadman.Switch(timeout_h=5, grace_h=3, quorum=2, vote_fn=lambda: 1)
        for t in range(0, 20):
            s.tick(float(t))
        self.assertEqual(s.state, deadman.State.WARNED)
        s2 = deadman.Switch(timeout_h=5, grace_h=3, quorum=2, vote_fn=lambda: 3)
        for t in range(0, 20):
            s2.tick(float(t))
        self.assertEqual(s2.state, deadman.State.TRIGGERED)

    def test_simulation_hardened_has_fewer_false_triggers(self):
        r = deadman.simulate(120)
        self.assertGreater(r["naive"]["false_trigger_rate"], 0.8)
        self.assertLess(r["hardened"]["false_trigger_rate"], 0.3 * r["naive"]["false_trigger_rate"])


class Lab07Insider(unittest.TestCase):
    def test_charlie_high_ana_not_out_of_role(self):
        with tempfile.TemporaryDirectory() as d:
            alerts = insider.run(Path(d))["alerts"]
        top = alerts[0]
        self.assertEqual(top["user"], "charlie")
        self.assertEqual(top["severity"], "alta")
        ana = next(a for a in alerts if a["user"] == "ana")
        self.assertFalse(any(r.startswith("R1") for r in ana["reasons"]))
        self.assertEqual(len(alerts), 2)


class Lab08Custody(unittest.TestCase):
    def test_chain_and_tamper_detection(self):
        r = custody.run(None)
        self.assertEqual(r["integrity_ok"], [])
        self.assertTrue(any("cctv.mp4" in p for p in r["tampered_evidence"]))
        self.assertTrue(r["tampered_log"])

    def test_volatility_order(self):
        self.assertEqual(custody.collection_plan(["disk", "memory_ram"]), ["memory_ram", "disk"])
        self.assertIn("memory_ram", custody.lost_if_powered_off(["disk", "memory_ram"]))
        self.assertNotIn("disk", custody.lost_if_powered_off(["disk", "memory_ram"]))


if __name__ == "__main__":
    unittest.main()
