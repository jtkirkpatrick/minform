"""
minform - Minimal indicators for text interfaces.

There are four indicators:
- Bouncer
- Spinner
- Ellipsis
- ProgressBar

All are used as context managers. Bouncer, Spinner, and Ellipsis take
only two arguments: message and erase. Setting erase=True will erase the
message after the task is complete, erase=False will reprint the message
without the text animation. These objects create a separate thread that
displays the indicator and message.

Example usage:

    with Spinner('This might take a while', erase=True):
        time.sleep(20)  # Pretend to do something.

    # This might take a while...


The ProgressBar requires a known quantity, `n`, of things to be done. It
also allows for a message, custom size, and k/n displayed in raw count
or in percent. Inside the with block, us the `.update(k)` method to
redraw the progress bar.

Example usage:

    with ProgressBar(150, 'Doing things', percent=True) as pb:
        for i in range(150):
            time.sleep(0.1)  # Pretend to do something.
            pb.update(i + 1)

    # Doing things [####################--------------------] (50%)
"""
import threading
import time


class _CharacterIterator(threading.Thread):

    def __init__(self, characters, message, erase):
        super().__init__()

        self._characters = characters
        self._message    = message
        self._erase      = erase
        self._run        = True

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self._run = False
        self.join()

        if not self._erase and self._message:
            print('{}  '.format(self._message))
        else:
            print(' '*(len(self._message) + 2), end='\r')

    def run(self):
        i = 0
        n = len(self._characters)
        while self._run:
            print('{} {}\r'.format(self._characters[i], self._message), end='')
            i = (i + 1)%n

            time.sleep(0.1)


class Bouncer(_CharacterIterator):
    """Text bouncer, use for long running tasks of unknown duration."""

    def __init__(self, message='', erase=False):
        """Initialize a text bouncer for tasks of unknown duration."""
        super().__init__(('.:\':'), message, erase)


class Ellipsis(threading.Thread):
    """Ellipsis, ..., use for long running tasks of unknown duration."""

    def __init__(self, message='', erase=False):
        super().__init__()

        self._message = message
        self._erase   = erase
        self._run     = True

    def __enter__(self):
        self.start()

    def __exit__(self, type, value, traceback):
        self._run = False
        self.join()
        
        if not self._erase and self._message:
            print('{}   '.format(self._message))
        else:
            print(' '*(len(self._message) + 3), end='\r')

    def run(self):
        i = 0
        while self._run:
            print('{}{}\r'.format(self._message, '.'*(i) + ' '*(3 - i)), end='')
            i = (i + 1)%4

            time.sleep(0.5)


class ProgressBar(object):
    """Text progress bar, use for long running tasks of known size."""

    def __init__(self, n, message='', size=40, percent=True):
        """Initialize a progress bar with a few simple properties."""
        self._n       = n
        self._message = message
        self._size    = size
        self._percent = percent

    def __enter__(self):
        """Initializes progress bar with zero complete items."""
        self.update(0)
        return self

    def __exit__(self, type, value, traceback):
        """Completely fills progress bar, then exits."""
        self.update(self._n)
        print('')

    def update(self, k):
        """Update progress bar to indicate `k` items are complete."""
        filled = int(self._size*float(k)/self._n)
        
        if self._percent:
            complete = '{:.0%}'.format(k/self._n)
        else:
            complete = '{}/{}'.format(k, self._n)

        print(
            '{}{}[{}{}] ({})\r'.format(
                self._message,
                ' ' if self._message else '',
                '#'*filled,
                '-'*(self._size - filled),
                complete
            ),
            end=''
        )


class Spinner(_CharacterIterator):
    """Text spinner, use for long running tasks of unknown duration."""

    def __init__(self, message='', erase=False):
        """Initialize a text spinner for tasks of unknown duration."""
        super().__init__((r'-\|/'), message, erase)


if __name__ == '__main__':
    print('Welcome to the `minform` demo!\n')
    
    with Spinner('It can spin!'):
        time.sleep(3)

    with Bouncer('It can bounce!'):
        time.sleep(3)

    with Ellipsis('It can do the dot-dot-dot!'):
        time.sleep(5)

    with ProgressBar(40, 'It can load!') as pb:
        for i in range(40):
            time.sleep(0.1)
            pb.update(i + 1)
    
    print('\nAnd that\'s all it can do!')
