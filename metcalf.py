from __future__ import annotations

import math

import numpy as np
from manim import *


class MetcalfesLawScene(Scene):
    """
    Visualize Metcalfe’s Law: network value ~ n(n-1)/2.
    We show nodes being added, connections increasing, and the formula updating.
    """

    def construct(self):
        title = Text("Metcalfe’s Law", font_size=48)
        subtitle = Text("Connections explode as people join", font_size=28)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN), run_time=1.5)
        self.wait(0.4)

        self.play(
            title.animate.to_edge(UP, buff=0.6),
            subtitle.animate.next_to(title, DOWN, buff=0.2),
            run_time=1.0,
        )
        self.wait(0.2)
        self.play(FadeOut(subtitle), run_time=0.6)

        # Layout for nodes on a circle
        radius = 2.1
        center = ORIGIN + UP * 0.6

        def node_position(k: int, total: int) -> np.ndarray:
            angle = TAU * k / total + PI / 2
            return center + radius * np.array([math.cos(angle), math.sin(angle), 0.0])

        def build_network(n: int) -> VGroup:
            nodes = VGroup(
                *[Dot(point=node_position(i, n), radius=0.07, color=BLUE) for i in range(n)]
            )

            stroke_width = max(0.35, 2.6 - (n * 0.02))
            edge_opacity = min(0.9, 12 / n)

            edges = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    edge = Line(
                        nodes[i].get_center(),
                        nodes[j].get_center(),
                        color=YELLOW,
                        stroke_width=stroke_width,
                    ).set_opacity(edge_opacity)
                    edges.add(edge)

            return VGroup(edges, nodes)

        def stage_label(n: int, connections: int, caption: str) -> VGroup:
            top = Text(f"People: {n}", font_size=28)
            mid = Text(f"Connections: {connections}", font_size=28)
            bot = Text(caption, font_size=28)

            label = VGroup(top, mid, bot).arrange(DOWN, buff=0.15)
            label.to_edge(DOWN, buff=0.2)
            return label

        stages = [
            (3, 3, "A simple triangle."),
            (5, 10, "A pentagram inside a pentagon."),
            (10, 45, "A dense geometric “rose” pattern."),
            (20, 190, "The center becomes a solid black mass of lines."),
            (100, 4950, "Nearly impossible to distinguish individual lines."),
        ]

        current_group: VGroup | None = None
        current_label: VGroup | None = None

        for n, connections, caption in stages:
            network = build_network(n)
            label = stage_label(n, connections, caption)

            if current_group is None:
                self.play(FadeIn(network), FadeIn(label), run_time=1.0)
            else:
                self.play(
                    FadeOut(current_group),
                    FadeOut(current_label),
                    FadeIn(network),
                    FadeIn(label),
                    run_time=1.0,
                )

            self.wait(1.0)
            current_group = network
            current_label = label

        self.wait(1.2)
