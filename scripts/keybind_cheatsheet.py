#!/usr/bin/env python3
import json
import os
import re
import sys
from collections import defaultdict

PATTERNS = {
    "bindsym": re.compile(r"bindsym\s+(.*?)\s+(?:\[.*\]\s+)?(?:.*exec\s+(?:--no-startup-id)?\s+)?(.*)"),
    "mode_start": re.compile(r"mode\s+(.*)\s+{"),
    "mode_end": re.compile(r"bindsym\s+(.*)mode\s+(.*)"),
    "exec": re.compile(r""),
}
ICONS = {
    re.compile(r"\$?mod", flags=re.I): "",
    re.compile(r"\$?alt", flags=re.I): "M",
    re.compile(r"ctrl", flags=re.I): "C",
    re.compile(r"shift", flags=re.I): "󰘶",
    re.compile(r"space", flags=re.I): "󱁐",
    re.compile(r"ret(?:urn)?", flags=re.I): "󰌑",
    re.compile(r"esc(?:ape)?", flags=re.I): "󱊷",
    re.compile(r"question", flags=re.I): "?",
    re.compile(r"grave", flags=re.I): "`",
}
# CONFIG = os.path.join(os.getenv("HOME"), ".config", "i3", "config.d")
CONFIG = os.path.join(os.getenv("HOME"), ".config", "regolith3", "config-i3", "config.d")
CACHE = os.path.join(os.getenv("HOME"), ".cache", "i3-cheat-sheet.json")


def iconify(keys, wrap=None):
    for pattern, replacement in ICONS.items():
        if wrap is not None:
            replacement = wrap[0] + replacement + wrap[1]
        keys = pattern.sub(replacement, keys)
    return keys

def generate(force=False):
    if os.path.exists(CACHE) and force is False:
        try:
            with open(CACHE, "r") as f:
                return json.load(f)
        except:
            pass

    bindings = defaultdict(dict)
    columns = {
        "keys": 0,
        "label": 0,
    }
    for conf in os.listdir(CONFIG):
        with open(os.path.join(CONFIG, conf)) as f:
            for line in f:
                line = line.strip()
                if not(line.startswith("##") and line.endswith("##") and "//" in line):
                    continue
                line = line.strip("#").strip()
                line = [x.strip() for x in line.split("//")]
                if len(line) == 3:
                    category, message, keys = line
                elif len(line) == 2:
                    category = ""
                    message, keys = line
                keys = iconify(keys)
                if len(keys) > columns["keys"]:
                    columns["keys"] = len(keys)
                if len(category) + len(message) > columns["label"]:
                    columns["label"] = len(category) + len(message)
                bindings[category][keys] = message, next(f).strip()

    menu = {}
    template = f"{{:{columns['label'] + 4}s}} {{:{columns['keys']}s}}"
    for category, commands in bindings.items():
        for keys, (message, action) in commands.items():
            item = template.format(f"({category}) {message}", keys)
            menu[item] = action

    with open(CACHE, "w") as f:
        json.dump(menu, f)
    return menu


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        menu = generate(force=True)
    else:
        menu = generate()

    if len(sys.argv) > 1 and sys.argv[1] != "generate":
        sys.exit(0)

    print("\0prompt\x1fi3 bindings:")
    for item, action in menu.items():
        print(item)
    sys.exit(0)
