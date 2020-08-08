GitHub Historian
===============

There can be many reasons to want to delete a repository. For example if it contains old code, dangerous code or just plain crappy code that you're not proud of. Or you may need to move a project somewhere else.. and you don't want to leave outdated code laying around.  
The sad thing is, when you delete your repository on GitHub, all your commit-messages and data points in the contribution activity view are gone.  

That's why I built **GitHub Historian**. It can download the entire commit-history (author, date & message) and re-commit it into a history-repo. And yes, commits in the history-repo are date-accurate. So if you made a commit at `00:00:00 2000 - 'Fireworks *yay*'` it will appear exactly there in your "new" history-repo.

> Lose old code, **KEEP** your history.

## How to use
GitHubHistorian is a Python 2.X script aimed at UNIX operating systems. But it will likely work on Windows too as long as you install Python. GitHubHistorian does not have any special dependencies so you can just download & run it.

1. Make sure to enter your own settings, such as repo-name, username into the designated area at the top of the script.
2. Run the script with `python GitHubHistorian.py` in your favourite shell


## MIT License (MIT)

Copyright (c) 2014 Theo Winter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
