import tempfile
import unittest
from pathlib import Path

from gargalo_lab import beacon_hunt, enhance_myth, exif_osint, usb_detect


class Lab01Enhance(unittest.TestCase):
    def test_collision_two_realities_same_photo(self):
        r = enhance_myth.collision_demo()
        self.assertTrue(r["originals_differ"])
        self.assertTrue(r["downscaled_identical"])

    def test_upscale_does_not_recover_detail(self):
        with tempfile.TemporaryDirectory() as d:
            r = enhance_myth.run(Path(d), factor=8)
        self.assertLess(r["psnr_db_bicubic"], 40)
        self.assertLess(r["hf_energy_upscaled"], r["hf_energy_original"])
        self.assertAlmostEqual(r["info_kept_pct"], 100 / 64, places=1)


class Lab02Exif(unittest.TestCase):
    def test_gps_present_then_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            r = exif_osint.run(Path(d))
        self.assertIsNotNone(r["before"]["gps"])
        self.assertAlmostEqual(r["before"]["gps"]["lat"], exif_osint.SAMPLE_LAT, places=2)
        self.assertIsNone(r["after"]["gps"])
        self.assertIsNone(r["after"]["make"])


class Lab03Usb(unittest.TestCase):
    def test_expected_alerts_only(self):
        with tempfile.TemporaryDirectory() as d:
            r = usb_detect.run(Path(d))
        rules = {(a["rule"], a["host"]) for a in r["alerts"]}
        self.assertIn(("R1-unknown-removable-storage", "WS-042"), rules)
        self.assertIn(("R2-exec-from-removable", "WS-042"), rules)
        self.assertIn(("R3-composite-keyboard-storage", "WS-077"), rules)
        self.assertFalse(any(h == "WS-002" for _, h in rules), "pendrive aprovado não deve alertar")


class Lab04Beacon(unittest.TestCase):
    def test_finds_both_beacons_and_ignores_ntp(self):
        with tempfile.TemporaryDirectory() as d:
            r = beacon_hunt.run(Path(d))
        dsts = {s["dst"] for s in r["suspects"]}
        self.assertEqual(dsts, {"203.0.113.50", "203.0.113.77"})


if __name__ == "__main__":
    unittest.main()
