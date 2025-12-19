from __future__ import annotations

import numpy as np
from manim import *


class FractalBranchingTree(MovingCameraScene):
    """
    Pure fractal branching tree:
    - Each tip splits into two tips (binary branching).
    - Branch length shrinks geometrically each generation.
    - Camera smoothly zooms out to fit the growing structure.
    """

    def construct(self):
        # ----------------------------
        # Parameters (tweak to taste)
        # ----------------------------
        generations = 15  # growth is ~2^n segments per generation
        trunk_length = 2.6
        length_ratio = 0.72  # geometric shrink per generation
        branch_angle = 28 * DEGREES  # symmetric split
        base_stroke = 7.0
        stroke_ratio = 0.82  # stroke shrink per generation

        # Animation pacing
        first_draw_time = 0.9
        per_generation_time = 0.55
        lag_ratio = 0.06  # stagger within each generation

        # Camera framing
        frame_pad = 1.25  # >1 means extra margin
        min_frame_width = 6.5  # don't zoom in too much at start

        # ----------------------------
        # Helpers
        # ----------------------------
        def as_np(p) -> np.ndarray:
            return np.array(p, dtype=float)

        def make_segment(
            start: np.ndarray, direction: np.ndarray, length: float, width: float
        ) -> tuple[Line, np.ndarray]:
            direction = direction / np.linalg.norm(direction)
            end = start + direction * length
            seg = Line(start, end).set_stroke(color=RED, width=width)
            return seg, end

        def fit_frame_to(mobj: Mobject, pad: float = 1.2) -> tuple[np.ndarray, float]:
            """
            Return (center, width) for camera frame to fit mobj with padding.
            Uses width to preserve aspect; Manim will keep height consistent.
            """
            # Guard: if mobj has no size yet (shouldn't happen once trunk exists)
            w = max(mobj.width, 1e-6)
            center = mobj.get_center()
            target_w = w * pad
            return center, target_w

        # ----------------------------
        # Scene setup
        # ----------------------------
        # Start camera near the trunk, but not too tight.
        self.camera.frame.set_width(min_frame_width)
        self.camera.frame.move_to(ORIGIN)

        tree = VGroup()

        # Trunk: start slightly below center so growth goes upward.
        start = as_np([0.0, -3.1, 0.0])
        trunk_dir = as_np(UP)

        trunk, tip = make_segment(start, trunk_dir, trunk_length, base_stroke)
        tree.add(trunk)

        self.play(Create(trunk), run_time=first_draw_time, rate_func=smooth)

        # Each tip is (position, direction)
        tips: list[tuple[np.ndarray, np.ndarray]] = [(tip, trunk_dir)]
        length = trunk_length
        stroke = base_stroke

        # ----------------------------
        # Grow generations
        # ----------------------------
        for _ in range(generations):
            length *= length_ratio
            stroke *= stroke_ratio

            new_segments = VGroup()
            new_tips: list[tuple[np.ndarray, np.ndarray]] = []

            for pos, dir_vec in tips:
                left_dir = rotate_vector(dir_vec, branch_angle)
                right_dir = rotate_vector(dir_vec, -branch_angle)

                left_seg, left_tip = make_segment(pos, left_dir, length, stroke)
                right_seg, right_tip = make_segment(pos, right_dir, length, stroke)

                new_segments.add(left_seg, right_seg)
                new_tips.append((left_tip, left_dir))
                new_tips.append((right_tip, right_dir))

            tree.add(new_segments)

            # Compute camera target after adding the new generation (so we fit the new bounds).
            target_center, target_width = fit_frame_to(tree, pad=frame_pad)
            target_width = max(target_width, min_frame_width)

            self.play(
                Create(new_segments, lag_ratio=lag_ratio),
                self.camera.frame.animate.move_to(target_center).set_width(
                    target_width
                ),
                run_time=per_generation_time,
                rate_func=smooth,
            )

            tips = new_tips

        self.wait(1.0)
