#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}



#starting utility applications at boot time
lxsession &
run nm-applet &
run pamac-tray &
numlockx on &
blueman-applet &
flameshot &
#picom --config $HOME/.config/picom/picom.conf &
picom --config .config/picom/picom-blur.conf --experimental-backends &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
(sleep 2s; jgmenu --hide-on-startup) &
run emacs --daemon &
feh --randomize --bg-fill ~/wallpapers/all-selected*
run optimus-manager-qt &
run redshift-gtk &
#run flatpak run org.fcitx.Fcitx5 &
fcitx5 &

#starting user applications at boot time
run polychromatic-tray-applet
#run volumeicon &
#run discord &
#nitrogen --random --set-zoom-fill &
#run caffeine -a &
#run dropbox &
#run insync start &
#run telegram-desktop &
