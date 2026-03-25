"""BitString class for representing spin configurations."""

import numpy as np


class BitString:
    """Simple class to implement a configuration of bits."""

    def __init__(self, N):
        self.N = N
        self.config = np.zeros(N, dtype=int)

    def __repr__(self):
        out = ""
        for i in self.config:
            out += str(i)
        return out

    def __eq__(self, other):
        return all(self.config == other.config)

    def __len__(self):
        return len(self.config)

    def on(self):
        """Return number of bits that are on."""
        return np.sum(self.config)

    def off(self):
        """Return number of bits that are off."""
        return self.N - self.on()

    def flip_site(self, i):
        """Flip the bit at site i."""
        self.config[i] = 1 - self.config[i]

    def integer(self):
        """Return the decimal integer corresponding to BitString."""
        val = 0
        for i in range(self.N):
            val += self.config[i] * 2 ** (self.N - 1 - i)
        return val

    def set_config(self, s):
        """Set the config from a list of integers."""
        self.config = np.array(s, dtype=int)

    def set_integer_config(self, dec):
        """Convert a decimal integer to binary and set as config."""
        self.config = np.zeros(self.N, dtype=int)
        for i in range(self.N):
            self.config[self.N - 1 - i] = dec % 2
            dec = dec // 2
