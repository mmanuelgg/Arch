#!/bin/sh

# Import the colors
#. "${HOME}/.cache/wal/colors.sh"
Background="#282a36"
Foreground="#f8f8f2"
CurrentSelection="#44475a"
Comment="#6272a4"
Cyan="#8be9fd"
Orange="#ffb86c"
Pink="#ff79c6"
Purple="#bd93f9"
Red="#ff5555"
Yellow="#f1fa8c"

dmenu_run -nb "$Background" -nf "$Foreground" -sb "$CurrentSelection" -sf "$Purple" -fn "NotoMonoRegular:bold:pixelsize=16"

#dmenu_run -nb "$color0" -nf "$color15" -sb "$color1" -sf "$color15"
