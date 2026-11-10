# hoffi-zmk
My shared ZMK configuration for split keyboards

## Keymap

The diagrams are generated from the current bindings. Hold Space for SYM,
hold Enter for NAV, and hold TAB on SYM for ADJ. Smaller legends show
what a key does when held. Hover over a key to see its ZMK binding.

Switch positions and angles come from the [official TOTEM layout SVG](https://github.com/GEIGEIGEIST/TOTEM/blob/main/docs/images/TOTEM_layout.svg)
and the [Sweep v2.2 PCB](https://github.com/davidphilipbarr/Sweep/tree/main/Sweep%20v2.2).
Sweep v2.2 is the geometry reference for the [Boardsource Crab Broom](https://boardsource.xyz/products/crab-broom-choc-ferris-sweep),
whose product page does not specify the revision of its custom PCB.

| Layer | TOTEM | Ferris Sweep |
| --- | --- | --- |
| BASE | [TOTEM BASE](docs/keymap/totem-base.svg) | [Sweep BASE](docs/keymap/universal-34-keys-base.svg) |
| NAV | [TOTEM NAV](docs/keymap/totem-nav.svg) | [Sweep NAV](docs/keymap/universal-34-keys-nav.svg) |
| SYM | [TOTEM SYM](docs/keymap/totem-sym.svg) | [Sweep SYM](docs/keymap/universal-34-keys-sym.svg) |
| ADJ | [TOTEM ADJ](docs/keymap/totem-adj.svg) | [Sweep ADJ](docs/keymap/universal-34-keys-adj.svg) |

## TOTEM and universal-34-keys firmware

Edit `config/totem.keymap`, then regenerate the universal-34-keys map and both sets of diagrams:

```sh
python3 scripts/generate_universal_34_keys.py
python3 scripts/generate_universal_34_keys.py --check
```

ZMK uses the generated `config/cradio.keymap` for both halves of the universal-34-keys build.
The build matrix targets the upstream Cradio shield with nice!nano v2
controllers and the shield's default pinout. Check the controller and PCB
revision before flashing.

Logical positions are zero-based. The left-to-right order below follows
each shield's matrix transform, including the reversed scan order on
Cradio's right half.

| Physical keys | TOTEM positions | universal-34-keys positions |
| --- | --- | --- |
| Top row | 0–9 | 0–9 |
| Home row | 10–19 | 10–19 |
| Bottom row, shared keys | 21–30 | 20–29 |
| Inner two thumbs per half | 33–36 | 30–33 |
| Outer bottom keys and outer thumbs | 20, 31, 32, 37 | — |

The generator projects every layer and translates combo and hold-tap trigger
positions. It rejects combos using removed keys so a replacement chord can
be chosen deliberately. TOTEM's soft-off behavior requires its shield's
wake configuration and is omitted from universal-34-keys.

GitHub Actions checks the generated map and builds both halves of each
keyboard plus the existing TOTEM settings-reset target. A published GitHub
release builds its tagged commit and attaches the UF2 files from that run.
