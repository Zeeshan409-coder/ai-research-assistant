import time


class LatencyTracker:
    def __init__(self):
        """
        Initializes a high-precision performance monitoring stopwatch using 
        system-level hardware monotonic counter clocks.
        """
        self.start_time = time.perf_counter()

    def elapsed_ms(self) -> float:
        """
        Calculates the delta between instantiation and execution check states,
        converting performance metrics into raw milliseconds cleanly.
        """
        return (time.perf_counter() - self.start_time) * 1000
