import os


def find_mp3s(folder):
    """Recursively find .mp3 files under `folder` and return sorted paths."""
    mp3s = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith('.mp3'):
                mp3s.append(os.path.join(root, f))
    return sorted(mp3s)

