import unittest
from unittest.mock import patch

from player import Player


class PlayerFallbackTests(unittest.TestCase):
    def test_initializes_without_audio_backend(self):
        with patch("player.pygame.mixer.init", side_effect=RuntimeError("no audio")), patch(
            "player.shutil.which", return_value=None
        ):
            player = Player()
            self.assertEqual(player.backend, "none")


if __name__ == "__main__":
    unittest.main()
