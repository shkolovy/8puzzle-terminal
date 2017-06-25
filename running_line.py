class RunningLine:
    """Running line"""

    def __init__(self, title, line_length):
        self.line_length = line_length
        self.title = title

        self.print_start_pos = 0
        self.word_start_pos = 0

    def draw(self):
        line = self._draw_line()

        if self.word_start_pos > 0:
            self.word_start_pos -= 1
            self.print_start_pos = 0
        else:
            self.print_start_pos += 1

        if self.print_start_pos > self.line_length:
            self.word_start_pos = len(self.title) - 1
            self.print_start_pos = 0

        return line

    def _draw_line(self):
        row = [" "] * self.line_length

        w = self.word_start_pos
        for i in range(self.print_start_pos, self.line_length):
            if w >= len(self.title):
                break

            row[i] = self.title[w]
            w += 1

        return f"#{''.join(row)}#"
