"""Render the split layout using the binding names from the keymap."""

from html import escape
import re

SYMBOLS = dict(zip(
    "EXCL AT HASH DOLLAR PERCENT CARET AMPERSAND ASTERISK SQT DOUBLE_QUOTES "
    "TILDE GRAVE LEFT_BRACKET RIGHT_BRACKET LEFT_PARENTHESIS RIGHT_PARENTHESIS "
    "PIPE LESS_THAN GREATER_THAN LEFT_BRACE RIGHT_BRACE MINUS UNDERSCORE EQUAL "
    "BSLH BACKSLASH FSLH SLASH DOT COMMA SEMI COLON".split(),
    "! @ # $ % ^ & * ' \" ~ ` [ ] ( ) | < > { } - _ = \\ \\ / / . , ; :".split(),
))
LABELS = {
    "PLUS": "+",

    "LEFT_SHIFT": "Shift", "RIGHT_SHIFT": "Shift",
    "LEFT_CTRL": "Ctrl", "LEFT_CONTROL": "Ctrl", "LCTRL": "Ctrl",
    "RIGHT_CONTROL": "Ctrl", "RCTRL": "Ctrl",
    "LEFT_GUI": "L Gui", "RIGHT_GUI": "R Gui",
    "LEFT_ALT": "L Alt", "RIGHT_ALT": "R Alt",
    "UP_ARROW": "↑", "DOWN": "↓", "LEFT": "←", "RIGHT": "→",
    "C_VOLUME_UP": "Vol +", "C_VOLUME_DOWN": "Vol −", "C_VOL_DN": "Vol −",
    "C_MUTE": "Mute", "C_PP": "Play / Pause", "C_PREV": "Previous", "C_NEXT": "Next",
    "LC(C_BRIGHTNESS_INC)": "Brightness +", "LC(C_BRIGHTNESS_DEC)": "Brightness −",
}
ACTIONS = {
    "&bspc_del": ("Backspace", "Shift: Delete"),
    "&hold_soft_off_3s": ("Soft off", "Hold 3 s"),
    "&hold_logout_1s": ("Log out", "Hold 1 s"),
    "&hold_bootloader_3s": ("Bootloader", "Hold 3 s"),
    "&hold_reset_3s": ("Reset", "Hold 3 s"),
    "&hold_bt_clear_3s": ("Clear BT", "Hold 3 s"),
    "&hold_bt_clear_all_10s": ("No action", ""),
    "&logout": ("Log out", ""),
    "&ss_full": ("Screenshot", "Full screen"),
    "&ss_area": ("Screenshot", "Select area"),
    "&ss_tools": ("Screenshot", "Tools"),
}


def key_name(code):
    return LABELS.get(code, SYMBOLS.get(code, re.sub(r"^(?:NUMBER_|N)(?=\d$)", "", code)))


def key_label(binding, layers):
    behavior, *args = binding.split()
    if behavior == "&kp":
        return key_name(args[0]), ""
    if behavior in {"&hmrl", "&hmrr", "&mt"}:
        return key_name(args[1]), f"Hold: {key_name(args[0])}"
    if behavior == "&lt":
        return key_name(args[1]), f"Hold: {layers[int(args[0])]}"
    if behavior == "&mo":
        return layers[int(args[0])], "While held"
    if behavior == "&bt" and args[0] == "BT_SEL":
        return f"BT {args[1]}", ""
    if behavior == "&trans":
        return "▽", ""
    if behavior == "&none":
        return "—", ""
    return ACTIONS.get(behavior, (binding, ""))


def draw_key(binding, x, y, angle, layers, width, height):
    primary, secondary = key_label(binding, layers)
    style = "muted" if binding in {"&trans", "&none"} else "key"
    baseline = -3 if secondary else 5
    size = min(15, 130 // max(len(primary), 1))
    return (
        f'<g transform="translate({x:.3f} {y:.3f}) rotate({angle:g})">'
        f'<title>{escape(binding)}</title>'
        f'<rect class="{style}" x="{-width / 2:g}" y="{-height / 2:g}" '
        f'width="{width}" height="{height}" rx="8"/>'
        f'<text y="{baseline}" font-size="{size}">{escape(primary)}</text>'
        f'<text class="sub" y="15">{escape(secondary)}</text></g>'
    )


def render(title, name, bindings, layer_names, geometry, key_size):
    if len(bindings) != len(geometry):
        raise ValueError(f"{title} {name} has the wrong number of keys")
    xs, ys, _ = zip(*geometry)
    scale = 5
    width = round((max(xs) - min(xs)) * scale) + 132
    height = round((max(ys) - min(ys)) * scale) + 194
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{escape(title)} {escape(name)} keymap">',
        '<style>text{font-family:system-ui,sans-serif;fill:#10263f;text-anchor:middle}'
        '.key{fill:#fff;stroke:#a6b8ce}.muted{fill:#e7edf5;stroke:#c1cede}'
        '.sub{font-size:11px;fill:#405d7e}.heading{text-anchor:start;font-weight:700}</style>',
        '<rect width="100%" height="100%" rx="16" fill="#f3f6fb"/>',
        f'<text class="heading" x="24" y="37" font-size="23">{escape(title)} · {escape(name)}</text>',
        f'<text class="sub" x="{width - 190}" y="37">▽  Transparent (fall through)     ·     —  Disabled</text>',
    ]
    for binding, (x, y, angle) in zip(bindings, geometry):
        svg.append(draw_key(binding, 66 + (x - min(xs)) * scale,
                            128 + (y - min(ys)) * scale, angle, layer_names,
                            *key_size))
    return "\n".join([*svg, "</svg>", ""])
