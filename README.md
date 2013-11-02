pyre
====

A simple Python regular expression library.


Installation
----

You may want to install this package, if so, please follow the instructions
below:

### Ubuntu

Change the working directory to the package folder(such as `pyre0.2.1`),
then type the following command in terminal:

```shell
sudo python setup.py install
```

### Windows

Open cmd(use shortcut key `Win`+`R` or open `Start` menu, type `cmd` in
`Run`), then change the current directory to the package folder(such as
 `pyre0.2.1`), and type the following command in cmd:

```shell
python setup.py install
```

### Other platform

Try to change the current directory to the package folder(such as
 `pyre0.2.1`) in the command line tool and type

```shell
python setup.py install
```

If it doesn't work, report to me if you'd like.


Supported Syntax
----

In total, syntax supported by the library is the most basic ones.
As following described in detail:

1. selection: `a|b`

2. concatenation: `ab`

3. loop: `a*`


Special Symbol
----

0. `\`: escape. To indicate backslash itself, use `\\` instead.

1. `\e`: epsilon.

2. `|`: selection. To indicate vertical bar, use `\|` instead.

3. `*`: loop. To indicate star, use `\*` instead.

4. `(` and `)`: group. To indicate parentheses, use `\(` and `\)` instead.


Honor Code
----

You should **NOT** copy it to complete your homework.
