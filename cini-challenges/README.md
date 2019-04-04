At the moment, **you can't browse the challenge list on GitHub; clone the repo and open `challenge-list.html` locally.**

# "Database" organization
Challenges are organized according to their *categories*, which correspond to *top-level directories* (e.g. `pwn`, `web`, ...)

Each subdirectory contains one, typically, or more related challenges (e.g. `reversing/be-quick-or-be-dead` contains three challenges, with increasing difficulty level).

## Challenge (sub)directory
Each (sub)directory contains
* usually, a text file called `description.txt`, describing the challenge and its setup, if any (e.g. how to start a dockerized server). This file can be missing in "pure" reversing challenges.
* optionally, some exploit\*/solution\* files that complement the write-up(s)
* challenge files (e.g. an executable); in some case, e.g. `pwn/arraymaster2`, there is a `distrib` subdirectory, which contains only the files to be distributed to players (for instance, challenge source code may, or may not, be distributed depending on difficult level)
* `chall-metadata.yml` a [YAML](https://yaml.org/) file, used by `refresh-challenge.py` to produce `challenge-list.html`. Each `chall-metadata.yml` can contain the description of one or more challenges (for instance, `pwn/1996/chall-metadata.yml` contains the description of *1996* only, while `reversing/be-quick-or-be-dead/chall-metadata.yml` contains the description of *be-quick-or-be-dead-1*, *be-quick-or-be-dead-2* and *be-quick-or-be-dead-3*).
  Each challenge consists of:
  * `name` (mandatory)
  * `ctf` (optional), used to identify the CTF the challenge comes from
  * `author` (optional)
  * `difficulty` (optional), the expected "difficulty level" for a beginnner; suggested values: Warm-up (<10 minutes), Easy (<30 minutes), Medium (30 minutes-1 hour), Hard (hours), Insane (days)
  * `tags` (optional), can be used to indicate, for instance, sub-categories (e.g. \#crypto for a reversing challenge) or needed techniques (e.g. \#ROP)
  * `notes` (optional)
  * `original_writeups` (mandatory), it can be an URL, or a list of URLs, "pointing" to write-ups for the challenge. Typically using [CTFtime](https://ctftime.org/)
  * `backup_writeups` (mandatory) that can be a filename, or a list of filenames, with a "backup" of one or more writeups. Typically consistings of a PDF print-page of one of the original writeups.

For instance, `pwn/arraymaster2` is described by:
```YAML
name: arraymaster2
ctf: 35c3 Junior CTF
author: Katharina Männle https://github.com/tharina
difficulty: hard
original_writeups: https://ctftime.org/task/7448
backup_writeups: writeup.pdf
```
