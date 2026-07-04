import os
import shutil
import subprocess
import threading
import time
import pygame


class PlayerInitError(RuntimeError):
    """Raised when the audio system cannot be initialized."""


class Player:
    """Controls playback using pygame.mixer in a background thread.

    If no audio backend is available, the player falls back to a CLI-friendly
    mode that reports the problem instead of crashing.
    """

    def __init__(self):
        os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', 'hide')
        self.backend = "pygame"
        self._thread = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._current = None
        self._paused = False
        self._fallback_command = None

        try:
            pygame.mixer.init()
        except Exception as e:
            self.backend = self._choose_fallback_backend()
            if self.backend == "none":
                self._fallback_command = None
                self.backend = "none"
                return

    def _choose_fallback_backend(self):
        for cmd in ("ffplay", "mpg123", "mpg321", "vlc"):
            if shutil.which(cmd):
                return cmd
        return "none"

    def _play_worker(self, filepath):
        try:
            if self.backend == "pygame":
                with self._lock:
                    pygame.mixer.music.load(filepath)
                    pygame.mixer.music.play()
                    self._current = filepath
                    self._paused = False

                while not self._stop_event.is_set() and pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            else:
                self._fallback_command = [self.backend, filepath]
                subprocess.Popen(self._fallback_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._current = filepath
                self._paused = False
                time.sleep(0.2)
                while not self._stop_event.is_set():
                    time.sleep(0.1)

        except Exception as e:
            print("Playback error:", e)
        finally:
            with self._lock:
                if self.backend == "pygame":
                    pygame.mixer.music.stop()
                self._current = None
                self._paused = False
                self._stop_event.clear()

    def _play_worker(self, filepath):
        try:
            with self._lock:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
                self._current = filepath
                self._paused = False

            # Wait while music plays or until stop requested
            while not self._stop_event.is_set() and pygame.mixer.music.get_busy():
                time.sleep(0.1)

        except Exception as e:
            print("Playback error:", e)
        finally:
            with self._lock:
                pygame.mixer.music.stop()
                self._current = None
                self._paused = False
                self._stop_event.clear()

    def play(self, filepath):
        """Start playing `filepath` in a background thread.

        Calling `play` stops any existing playback first.
        """
        self.stop()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._play_worker, args=(filepath,), daemon=True)
        self._thread.start()

    def pause(self):
        with self._lock:
            if self._current and not self._paused:
                if self.backend == "pygame":
                    pygame.mixer.music.pause()
                self._paused = True

    def resume(self):
        with self._lock:
            if self._current and self._paused:
                if self.backend == "pygame":
                    pygame.mixer.music.unpause()
                self._paused = False

    def stop(self):
        """Stop playback immediately."""
        self._stop_event.set()
        with self._lock:
            if self.backend == "pygame":
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
            self._paused = False
            self._current = None

    def is_playing(self):
        return self._current is not None

