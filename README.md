# Subnetting Calculator

A calculator built with Python to learn network subnetting.

Built as a hands-on study project while working toward CCNA certification — the goal is to actually understand the bitwise math behind subnetting, not just memorize charts.

## Features

- Parses IPv4 CIDR notation (e.g. `192.168.1.0/24`)
- Calculates subnet mask, network address, broadcast address, usable host range, and usable host count
- Handles edge cases correctly, including `/31` (RFC 3021 point-to-point links) and `/32`
- Available as both a command-line tool and a desktop GUI

## Requirements

- Python 3.14+
- [UV](https://docs.astral.sh/uv/) for dependency management

## Installation

```bash
git clone git@github.com:guitarzandy009/subnetting-calculator.git
cd subnetting-calculator
uv sync
```

## Usage

### Command line

```bash
uv run subnetcalc 192.168.1.0/24
```

### GUI

```bash
uv run subnetcalc-gui
```

**Linux note:** if the GUI fails with a `Can't find a usable init.tcl` error, install the Tcl/Tk runtime and point Python at it:

```bash
sudo apt install tk8.6 tcl8.6
export TCL_LIBRARY=/usr/share/tcltk/tcl8.6
export TK_LIBRARY=/usr/share/tcltk/tk8.6
```

Add those two `export` lines to your `~/.bashrc` to make them permanent.

## Running tests

```bash
uv run pytest -v
```

## Project structure

src/subnetcalc/
├── core.py # subnetting logic (pure stdlib, no dependencies)
├── cli.py # command-line interface
└── gui.py # Tkinter GUI
tests/
└── test_core.py

The core logic is deliberately kept independent of any interface, so the same tested functions power the CLI, the GUI, and (planned) a web version.

## Roadmap

- [x] Core subnetting logic with full test coverage
- [x] Command-line interface
- [x] Tkinter desktop GUI
- [ ] Web app (Flask or Anvil) for online deployment
