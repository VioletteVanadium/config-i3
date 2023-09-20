if [ $(xrandr | grep '*' | sed -E 's/^\s*([0-9]+)x.*$/\1/') -lt 2000 ]; then
    i3-msg "gaps inner all set 12"
    i3-msg "gaps outer all set 24"
    i3-msg "gaps horizontal all set 48"
else
    i3-msg "gaps inner all set 120"
    i3-msg "gaps outer all set 240"
    i3-msg "gaps horizontal all set 480"
fi
