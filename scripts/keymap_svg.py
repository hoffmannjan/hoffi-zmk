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


def draw_key(binding, x, y, layers):
    primary, secondary = key_label(binding, layers)
    style = "muted" if binding in {"&trans", "&none"} else "key"
    baseline = y + (26 if secondary else 34)
    size = min(15, 142 // max(len(primary), 1))
    return (
        f'<g><title>{escape(binding)}</title>'
        f'<rect class="{style}" x="{x}" y="{y}" width="94" height="55" rx="8"/>'
        f'<text x="{x + 47}" y="{baseline}" font-size="{size}">{escape(primary)}</text>'
        f'<text class="sub" x="{x + 47}" y="{y + 43}">{escape(secondary)}</text></g>'
    )


def render(title, name, bindings, layer_names, row_sizes):
    if len(bindings) != 2 * sum(row_sizes):
        raise ValueError(f"{title} {name} has the wrong number of keys")
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 335" '
        f'width="1300" height="335" role="img" aria-label="{escape(title)} {escape(name)} keymap">',
        '<style>text{font-family:system-ui,sans-serif;fill:#10263f;text-anchor:middle}'
        '.key{fill:#fff;stroke:#a6b8ce}.muted{fill:#e7edf5;stroke:#c1cede}'
        '.sub{font-size:11px;fill:#405d7e}.heading{text-anchor:start;font-weight:700}</style>',
        '<rect width="100%" height="100%" rx="16" fill="#f3f6fb"/>',
        f'<text class="heading" x="24" y="37" font-size="23">{escape(title)} · {escape(name)}</text>',
        '<text class="sub" x="1050" y="37">▽  Transparent (fall through)     ·     —  Disabled</text>',
    ]
    offset = 0
    for row, half in enumerate(row_sizes):
        for column in range(2 * half):
            x = 616 - (half - column) * 98 if column < half else 686 + (column - half) * 98
            svg.append(draw_key(bindings[offset + column], x, 66 + row * 62, layer_names))
        offset += 2 * half
    return "\n".join([*svg, "</svg>", ""])
