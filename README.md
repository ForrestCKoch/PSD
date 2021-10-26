# PSD

Credit to Seid Miad Zandavi (s.zandavi@unsw.edu.au) for development of this method.  The Python code has simply been adapted from his Matlab implementation.

## Usage

The package can be installed with `pip install psdPy`.  It can then be used as follows:

```
from psdPy import psd
import numpy as np

# Replace X with your data
# X should be in the form (samples x features)
X = np.random.normal(size=(10,10))
psd(X)
```
