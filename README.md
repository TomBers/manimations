# manimations

A small repository for creating mathematical animations using [Manim Community](https://www.manim.community/).

This project is structured as a set of Manim “scene scripts” (Python files that define `Scene` subclasses). You render a specific scene by passing the file and class name to the `manim` CLI.

## Prerequisites

- Python (this repo targets Python 3.13 via `pyproject.toml`)
- Manim Community (`manim>=0.19.1`)

Manim docs and installation guide:
- https://docs.manim.community/
- https://www.manim.community/

## Rendering a scene

From the repository root, run:

```
manim -pql main.py FractalBranchingTree
```

What the flags mean:
- `-p` opens the rendered video when finished
- `-q l` renders at “low” quality (fast for iteration)

If your scene lives in a subdirectory, run the command from that directory (or pass the path). For example:

```
cd my-project
manim -pql main.py FractalBranchingTree
```

## Example scene

`FractalBranchingTree` is a “pure fractal” branching tree that grows generation-by-generation while the camera smoothly zooms out to keep the full structure in frame.

You can tweak parameters like `generations`, `branch_angle`, and `length_ratio` inside the scene to change the look and performance.