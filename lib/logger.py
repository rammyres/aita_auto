from proglog import ProgressBarLogger

class FletProgressBarLogger(ProgressBarLogger):
    def __init__(self, update_callback):
        self.update_callback = update_callback
        super().__init__()

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        if bar == 't':
            current = value
            total = self.bars[bar]['total']
            self.update_callback(current, total)