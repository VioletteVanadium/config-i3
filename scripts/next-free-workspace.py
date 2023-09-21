#!/usr/bin/env python3

import i3ipc
import argparse
import subprocess
import re

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find the next non-opened workspace and go there."
    )
    parser.add_argument("-s", "--startnum", type=int, default=1, help="DEPRECATED")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-mv",
        "--move-window",
        action="store_true",
        help="Instead of going to next non-opened workspace, move current window there.",
    )
    group.add_argument(
        "-mvf",
        "--move-window-and-follow",
        action="store_true",
        help="Move current window to next non-opened workspace and follow.",
    )
    args = parser.parse_args()

    # Get names of the Xserver
    mapping_names = {}
    output, err = subprocess.Popen(
        ["xrdb", "-query"], stdout=subprocess.PIPE
    ).communicate()
    output = output.decode().split("\n")
    output = [
        line.split("\t")[1]
        for line in output
        if re.search("wm\.workspace\...\.name:", line)
    ]
    mapping_names = {}
    for line in output:
        if ":" in line:
            key, value = line.split(":")
            mapping_names[int(key)] = value
        else:
            mapping_names[int(line)] = line

    startnum = min(mapping_names.keys())
    endnum = 50
    i3 = i3ipc.Connection()
    workspaces = i3.get_workspaces()
    nums = {w.num for w in workspaces}
    s_ = {x for x in range(startnum, endnum)}
    targetnum = min(s_ - nums)
    try:
        targetstring = f"{targetnum}:{mapping_names[targetnum]}"
    except KeyError:
        targetstring = f"{targetnum}:{targetnum}"

    if args.move_window or args.move_window_and_follow:
        i3.command("move container workspace " + targetstring)
    if not args.move_window:
        i3.command("workspace number " + targetstring)
