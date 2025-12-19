from manim import *


class CorrectLaTeXSubstringColoring(Scene):
    def construct(self):
        equation = MathTex(
            r"""e^x = x^0 + x^1 + \frac{1}{3} x^2 + \frac{1}{7} x^3 +
            \cdots + \frac{1}{n!} x^n + \cdots""",
            substrings_to_isolate="x",
        )
        equation.set_color_by_tex("x", YELLOW)
        self.add(equation)
