# minform
Minimal indicators for text interfaces.

Minform is a simple Python module to provide basic progress indication in text interfaces. There are four indicators: `Bouncer`, `Spinner`, `Ellipsis`, and `ProgressBar`. Run `minform.py` to see a short demo of each object.

## Usage
All minform objects are used as context managers. They are very simple to work into existing code, improving communication with users.
```
import time
import minform

with minform.Ellipsis('Working on it', erase=True):
    time.sleep(5)
  
with minform.ProgressBar(100, 'Progressing') as pb:
    for i in range(100):
       time.sleep(0.05)
       pb.update(i + 1)
```

`Bouncer`, `Spinner`, and `Ellipsis` take an optional `erase` argument that will remove the message when the context manager exits if `erase` is `True`. Otherwise the message will be left on the screen.
