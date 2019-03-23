import math
import shutil


class Printer(object):

    def __init__(self, synchronizer):
        self._synchronizer = synchronizer

    def output(self):
        print(
            """The following {plural} only exist in the sandbox:
{}

The following {plural} only exist in production:
{}

The following {plural} are different between environments:
{}

There are {} other {plural} that are the same between environments.
""".format(
                self.in_columns(self._synchronizer.only_in_sandbox),
                self.in_columns(self._synchronizer.only_in_production),
                self.in_columns(self._synchronizer.in_both_but_different),
                len(
                    set(self._synchronizer.in_both).difference(
                        self._synchronizer.in_both_but_different
                    )
                ),
                plural="{}s".format(self._synchronizer.api_object.__name__)
            )
        )

    def in_columns(self, values):
        if not values:
            return ""

        width = shutil.get_terminal_size().columns
        max_size = max([len(str(value)) for value in values])
        columns = max(
            1,
            min([math.floor(width / (max_size + 1)), len(values)])
        )
        column_width = math.floor(width / columns)

        return "\n".join(
            "".join(
                [
                    str(value).ljust(column_width)
                    for value in values[start:start + columns]
                ]
            )
            for start in range(0, len(values), columns)
        )
