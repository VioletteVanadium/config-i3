#!/usr/bin/zsh

export XSECURELOCK_AUTH_BACKGROUND_COLOR=$(xrdb -query -get color0)
export XSECURELOCK_AUTH_FOREGROUND_COLOR=$(xrdb -query -get color7)
export XSECURELOCK_AUTH_TIMEOUT=60
export XSECURELOCK_AUTH_WARNING_COLOR=$(xrdb -query -get color1)
export XSECURELOCK_BACKGROUND_COLOR=$(xrdb -query -get background)
export XSECURELOCK_BLANK_DPMS_STATE=off
export XSECURELOCK_BLANK_TIMEOUT=-1
export XSECURELOCK_COMPOSITE_OBSCURER=0
export XSECURELOCK_DIM_TIME_MS=500
export XSECURELOCK_FONT=$(xrdb -query -get font)
export XSECURELOCK_PASSWORD_PROMPT=asterisks
export XSECURELOCK_SAVER=saver_blank
export XSECURELOCK_SHOW_DATETIME=1
export XSECURELOCK_SHOW_KEYBOARD_LAYOUT=off

/usr/bin/xsecurelock
