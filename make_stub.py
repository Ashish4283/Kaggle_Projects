"""Write the stub notebook: the three cells that never change."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "https://github.com/Ashish4283/Kaggle_Projects.git"


def rows(src):
    out = src.strip("\n").split("\n")
    return [r + "\n" for r in out[:-1]] + out[-1:]


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": rows(src)}


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": rows(src)}


cells = [
    md("""
# CastForge on a rented GPU

**This notebook never changes.** It pulls the code from
[Kaggle_Projects](https://github.com/Ashish4283/Kaggle_Projects) and runs it, so a fix on GitHub
reaches this machine by re-running cell 1 - nothing to download, nothing to re-upload.

**Before you run anything:**

* **Kaggle** - the panel on the **right**: **Settings > Accelerator > GPU T4 x2**, and
  **Settings > Internet > On**. Internet is off by default and nothing can be downloaded without it.
* **Colab** - **Runtime > Change runtime type > T4 GPU**.

Then **Run all**. Cell 2 stops with one plain line if either switch is wrong.
"""),

    md("## 1 - Get the latest code"),
    code("""
import pathlib, shutil, subprocess, sys

REPO = "https://github.com/Ashish4283/Kaggle_Projects.git"
HERE = pathlib.Path("/kaggle/working" if pathlib.Path("/kaggle").is_dir() else "/content")
MINE = HERE / "Kaggle_Projects"

if (MINE / ".git").is_dir():
    subprocess.run(["git", "-C", str(MINE), "pull", "--ff-only", "-q"], check=False)
    print("pulled the latest")
else:
    shutil.rmtree(MINE, ignore_errors=True)
    done = subprocess.run(["git", "clone", "--depth", "1", REPO, str(MINE)],
                          capture_output=True, text=True)
    if done.returncode:
        print(done.stderr.strip()[-800:])
        raise SystemExit("could not clone the project repo")
    print("cloned")

sys.path.insert(0, str(MINE / "castforge"))
import boot
import importlib
importlib.reload(boot)          # so a pull actually takes effect without restarting the kernel
print("boot.py loaded from", MINE / "castforge")
"""),

    md("""
## 2 - GPU, internet, ComfyUI, the checkpoint

First run is about ten minutes: it fetches a 6.5 GB checkpoint. Every run after that is about two,
and on Kaggle it is seconds once the model is attached as a dataset (it tells you how).
"""),
    code("""
place = boot.setup()
"""),

    md("""
## 3a - Make the whole set, with no tunnel

This is what Kaggle is good at: **Save Version > Run All** runs headless for up to twelve hours with
nothing to keep open and no address to go stale.

When it finishes, download `castforge/swatches` from the output and, on the laptop:

```
python generate/make_fabric.py --folder <the folder you downloaded>
```
"""),
    code("""
boot.batch(boot.CLOTH, place)
"""),

    md("""
## 3b - Or open a door, and drive it from the laptop

Use this instead when somebody is at the other end wanting one swatch, then another. It prints an
address; give that to the laptop:

```
python castforge.py gpu connect https://xxxx.trycloudflare.com
python castforge.py gpu fabric "worn indigo denim" --kind denim
```

The address is **new every time** this cell runs. Leave the tab open or the door closes.
"""),
    code("""
# boot.tunnel(place)
# boot.alive()        # ...and run this to stop the session being reaped while you work
"""),

    md("""
---
### When it goes wrong

| what you see | what it means |
|---|---|
| `No GPU` | Kaggle: Settings > Accelerator. Colab: Runtime > Change runtime type |
| `No internet in this session` | Kaggle: the panel on the RIGHT > Settings > Internet > On |
| `git could not clone ...` | git's own words are printed underneath it |
| `ComfyUI did not start` | its own last forty lines are printed underneath it |
| a 502 from the tunnel | ComfyUI died behind it, almost always out of VRAM. Re-run cell 2 |

Nothing here needs a Hugging Face token: RealVisXL Lightning is not gated. If you ever switch to FLUX,
put the token in Colab's **Secrets** panel as `HF_TOKEN` - never in a cell, because anything typed in a
cell is saved in the notebook.
"""),
]

nb = {"nbformat": 4, "nbformat_minor": 0,
      "metadata": {"accelerator": "GPU",
                   "colab": {"provenance": [], "gpuType": "T4"},
                   "kernelspec": {"display_name": "Python 3", "name": "python3"},
                   "language_info": {"name": "python"}},
      "cells": cells}

out = os.path.join(HERE, "castforge_gpu.ipynb")
io.open(out, "w", encoding="utf-8", newline="\n").write(json.dumps(nb, indent=1))
print("wrote", out, len(cells), "cells")
