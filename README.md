# Kaggle Projects

GPU work for [CastForge](https://github.com/Ashish4283/castforge), run on a rented GPU (Kaggle or
Colab) and kept here so the notebook on Kaggle never has to be re-uploaded.

## How it fits together

```
castforge_gpu.ipynb     the notebook on Kaggle. Three cells. NEVER CHANGES.
castforge/boot.py       everything it actually does. Edit this.
make_stub.py            writes the notebook, if the three cells ever do need changing
```

The notebook pulls this repo and imports `boot`, so a fix here reaches the GPU by re-running cell 1.
Nothing to download, nothing to re-upload.

## Using it

1. On Kaggle: **File > Import Notebook**, or link this repo under **File > Link to GitHub**.
2. Right-hand panel: **Settings > Accelerator > GPU T4 x2**, and **Settings > Internet > On**.
   Internet is off by default and nothing can be downloaded without it.
3. **Run all.**

Cell 3a makes a whole set of fabrics with no tunnel - which is what Kaggle is good at, because
**Save Version > Run All** runs headless for up to twelve hours with nothing to keep open. Download
`castforge/swatches` afterwards and, in the CastForge repo on the laptop:

```
python generate/make_fabric.py --folder <the folder you downloaded>
```

Cell 3b instead opens a `trycloudflare` address and lets the laptop drive it one swatch at a time:

```
python castforge.py gpu connect https://xxxx.trycloudflare.com
python castforge.py gpu fabric "worn indigo denim" --kind denim
```

## What the GPU is for, and what it is not

It makes **one square picture of cloth**. That is all. Everything else - whether the square actually
tiles, the relief, the roughness - is worked out on the laptop, where it is free, instant and the same
every time. A rented GPU is the flakiest part of any pipeline, so it does as little as possible.

A swatch that does not tile is **refused on the laptop**, with the reason, rather than discovered later
on a character.

## No secrets here

Nothing in this repo needs a token: RealVisXL Lightning is not gated. If you ever switch to FLUX, the
token goes in Colab's **Secrets** panel (the key icon) as `HF_TOKEN` - never in a cell, because anything
typed into a cell is saved in the notebook and goes wherever the notebook goes.
