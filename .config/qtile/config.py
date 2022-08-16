# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule, KeyChord
from libqtile.command import lazy

from libqtile.widget import Spacer

import asyncio

# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


myTerm = "alacritty"  # My terminal of choice
terminal = "kitty"

keys = [



    # SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn('kitty')),
    Key([mod], "KP_Enter", lazy.spawn('kitty')),
    Key([mod], "t", lazy.spawn('telegram-desktop')),

    # SUPER + SHIFT KEYS

    Key([mod, "shift"], "Return", lazy.spawn('pcmanfm')),
    # Key([mod, "shift"], "d", lazy.spawn("dmenu_run -i -nb '#282a36' -nf '#f8f8f2' -sb '#44475a' -sf '#bd93f9' -fn 'NotoMonoRegular:bold:pixelsize=16'")),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "e", lazy.spawn("emacsclient -c -a 'emacs'")),

    # SUPER + CONTROL KEYS

    Key([mod, "control"], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([mod, "control"], "Return", lazy.spawn('alacritty')),
    Key([mod, "control"], "f", lazy.spawn('firefox')),
    Key([mod, "control"], "s", lazy.spawn('spotify')),

    # CONTROL + ALT KEYS

    Key(["mod1", "control"], "o", lazy.spawn(
        home + '/.config/qtile/scripts/picom-toggle.sh')),
    Key(["mod1", "control"], "t", lazy.spawn('xterm')),
    Key(["mod1", "control"], "Return", lazy.spawn('jgmenu_run')),

    # ALT + ... KEYS

    #Key(["mod1"], "b", lazy.spawn('qutebrowser')),
    #Key(["mod1"], "m", lazy.spawn('pcmanfm')),

    # KEY CHORDS

    # Manager chord
    KeyChord([mod], "m", [
        Key([], "f", lazy.spawn('pcmanfm')),
        Key([], "Return", lazy.spawn('thunar')),
        Key([], "t", lazy.spawn('thunar')),
        Key([], "d", lazy.spawn('dolphin')),
        Key([], "c", lazy.spawn('code')),
    ]),

    # Rofi
    KeyChord([mod, "shift"], "d", [
        Key([], "d", lazy.spawn("rofi -show drun")),
        Key([], "w", lazy.spawn("rofi -show window")),
        Key([], "c", lazy.spawn("rofi -show combi")),
        Key([], "f", lazy.spawn("rofi -show filebrowser")),
        Key([], "r", lazy.spawn("rofi -show run")),
        Key([], "k", lazy.spawn("rofi -show keys")),
        Key([], "s", lazy.spawn("rofi -show ssh")),
    ]),

    # Power options
    KeyChord([mod, "shift"], "z", [
        Key([], "z", lazy.spawn("systemctl suspend")),
        Key([], "r", lazy.spawn("reboot")),
        Key([], "x", lazy.shutdown()),
        Key([], "p", lazy.spawn('poweroff')),
        Key([], "l", lazy.spawn('betterlockscreen -l')),
    ]),

    # Browsers
    KeyChord([mod], "b", [
        Key([], "q", lazy.spawn("qutebrowser")),
        Key([], "f", lazy.spawn('firefox')),
        Key([], "b", lazy.spawn('brave')),
    ]),

    # Social
    KeyChord([mod], "s", [
        Key([], "d", lazy.spawn('discord-canary')),
        Key([], "t", lazy.spawn('thunderbird')),
        Key([], "e", lazy.spawn('evolution')),
        Key([], "m", lazy.spawn('element-desktop')),
    ]),

    # Editors
    KeyChord([mod], "c", [
        Key([], "c", lazy.spawn('code')),
        Key([], "n", lazy.spawn('notepadqq')),
    ]),

    # Emacs
    KeyChord([mod], "e", [
        Key([], "e", lazy.spawn("emacsclient -c -a 'emacs'")),
        Key([], "m", lazy.spawn("emacsclient -c -a 'emacs' --eval '(emms)' --eval '(emms-play-directory-tree \"~/Música/\")'")),
        Key([], "b", lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'")),
        Key([], "d", lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'")),
        Key([], "i", lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'")),
        Key([], "n", lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'")),
        Key([], "s", lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'")),
        Key([], "v", lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'")),
        Key([], "w", lazy.spawn("emacsclient -c -a 'emacs' --eval '(doom/window-maximize-buffer(eww \"distro.tube\"))'")),
    ]),

    # Gaming
    KeyChord([mod], "g", [
        Key([], "s", lazy.spawn("steam")),
        Key([], "h", lazy.spawn('heroic')),
        Key([], "r", lazy.spawn('retroarch')),
        Key([], "l", lazy.spawn('lutris')),
        Key([], "g", lazy.spawn('minigalaxy')),
        Key([], "m", lazy.spawn('minecraft-launcher')),
    ]),


    # CONTROL + SHIFT KEYS

    Key([mod2, "shift"], "Escape", lazy.spawn('lxtask')),


    # SCREENSHOTS

    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Imágenes')),
    Key([mod, "shift"], "s", lazy.spawn('flameshot gui')),
    #    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

    # MULTIMEDIA KEYS

    # INCREASE/DECREASE BRIGHTNESS
    #    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    #    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brillo -q -A 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brillo -q -U 5")),

    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioesktopPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # MONITOR SWITCHING

    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),

    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'
        ),



    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()), ]

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = [" ", "", " ", "𝄡 ", "𝄢 ", "𝄞 ", " ", " \uf1d8", " ", " ", ]
group_labels = [" ", "", "\uf03d ", "\uf303 ", "\ue244 ", " ", "\ue217 ", "\uf886", "\uf675 ", "", ]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["max", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", ]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        # CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key(["mod1", "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), lazy.group[i.name].toscreen()),
    ])


def dracula_colors():
    return [["#282a36", "#282a36"],  # 0 Background
            ["#f8f8f2", "#f8f8f2"],  # 1 Foreground
            ["#44475a", "#44475a"],  # 2 Current Line and Selection
            ["#6272a4", "#6272a4"],  # 3 Comment
            ["#8be9fd", "#8be9fd"],  # 4 Cyan
            ["#ffb86c", "#ffb86c"],  # 5 Orange
            ["#ff79c6", "#ff79c6"],  # 6 Pink
            ["#bd93f9", "#bd93f9"],  # 7 Purple
            ["#50fa7b", "#50fa7b"],  # 8 Green
            ["#ff5555", "#ff5555"],  # 9 Red
            ["#f1fa8c", "#f1fa8c"]]  # 10 Yellow


dracula_colors = dracula_colors()


def init_layout_theme():
    return {"margin": 10,
            "border_width": 3,
            "border_focus": dracula_colors[7],  # "#ff00ff",
            "border_normal": dracula_colors[0]  # "#f4c2c2"
            }


layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    # layout.Columns(**layout_theme),
    # layout.Stack(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(
    #   sections=['FIRST', 'SECOND'],
    #   bg_color = dracula_colors[0],#'#141414',
    #   active_bg = dracula_colors[2],#'#0000ff',
    #   inactive_bg = dracula_colors[3],#'#1e90ff',
    #   padding_y =5,
    #   section_top =10,
    #   panel_width = 280),
    # layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme)
]

# COLORS FOR THE BAR


def init_colors():
    return [["#2F343F", "#2F343F"],  # color 0
            ["#2F343F", "#2F343F"],  # color 1
            ["#c0c5ce", "#c0c5ce"],  # color 2
            ["#e75480", "#e75480"],  # color 3
            ["#f4c2c2", "#f4c2c2"],  # color 4
            ["#ffffff", "#ffffff"],  # color 5
            ["#ff0000", "#ff0000"],  # color 6
            ["#62FF00", "#62FF00"],  # color 7
            ["#000000", "#000000"],  # color 8
            ["#c40234", "#c40234"],  # color 9
            ["#6790eb", "#6790eb"],  # color 10
            ["#ff00ff", "#ff00ff"],  # 11
            ["#4c566a", "#4c566a"],  # 12
            ["#282c34", "#282c34"],  # 13
            ["#212121", "#212121"],  # 14
            ["#98c379", "#98c379"],  # 15
            ["#b48ead", "#b48ead"],  # 16
            ["#abb2bf", "#abb2bf"],  # color 17
            ["#81a1c1", "#81a1c1"],  # 18
            ["#56b6c2", "#56b6c2"],  # 19
            ["#c678dd", "#c678dd"],  # 20
            ["#e06c75", "#e06c75"],  # 21
            ["#fb9f7f", "#fb9f7f"],  # 22
            ["#ffd47e", "#ffd47e"]]  # 23


colors = init_colors()


def base(fg='text', bg='dark'):
    return {'foreground': dracula_colors[1], 'background': dracula_colors[0]}
    # return {'foreground': colors[14],'background': colors[15]}


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font='Ubuntu Nerd Font Bold',  # font="Blex Mono Nerd Font Bold",
                fontsize=16,
                padding=2,
                background=dracula_colors[0])
    # background=colors[1])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

        widget.Image(
            #filename="~/.config/qtile/icons/garuda-purple.png",
            filename="~/.config/qtile/icons/kitsune-tail-purple.png",
            iconsize=20,
            background=dracula_colors[0],  # colors[15],
            #mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('jgmenu_run')}
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('nwggrid -p -o 0.4')}
        ),
        widget.GroupBox(

            **base(bg=dracula_colors[0]),  # colors[15]),
            font='UbuntuMono Nerd Font',

            fontsize=16,
            margin=5,
            padding=3,
            #margin_y=3,
            #margin_x=2,
            #padding_y=5,
            #padding_x=4,
            borderwidth=5,

            active=dracula_colors[1],  # colors[5],
            inactive=dracula_colors[3],  # colors[6],
            rounded=True,
            # highlight_method='block',
            highlight_method='line',
            highlight_color=dracula_colors[2],  # When in 'line' method
            fontshadow=dracula_colors[0],
            urgent_alert_method='block',
            urgent_border=dracula_colors[6],  # colors[16],
            this_current_screen_border=dracula_colors[7],  # colors[20],
            this_screen_border=dracula_colors[8],  # colors[17],
            other_current_screen_border=dracula_colors[4],  # colors[13],
            other_screen_border=dracula_colors[5],  # colors[17],
            disable_drag=True

        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=dracula_colors[1],  # colors[5],
            background=dracula_colors[0],  # colors[3],
            padding=0,
            scale=0.7
        ),

        widget.CurrentLayout(
            foreground=dracula_colors[1],  # colors[5],
            background=dracula_colors[0],  # colors[3]
            fmt=' {} '
        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.WindowCount(
            foreground=dracula_colors[5],
            fmt=' {} '
        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.TaskList(
            highlight_method='border',  # border or block
            # icon_size=19,
            max_title_width=150,
            rounded=True,
            fontsize=16,
            border=dracula_colors[8],  # colors[7],
            foreground=dracula_colors[7],  # colors[9],
            unfocused_border=dracula_colors[3],
            margin=0,
            padding=0,
            txt_floating='🗗',
            txt_minimized='>_ ',
            borderwidth=2,
            background=dracula_colors[0],  # colors[20],
            #unfocused_border = 'border'
        ),

#       widget.Mpris2(
#           foreground=dracula_colors[7],
#           name="spotify",
#           stop_pause_text="Paused",
#           #scroll_chars=None,
#           display_metadata=["xesam:title", "xesam:artist"],
#           objname="org.mpris.MediaPlayer2.spotify",
#       ),

        widget.TextBox(
            fmt=' \ue777 ',
            fontsize=24,
            foreground=dracula_colors[7],
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + ' --hold -e htop'),
                             'Button3': lambda: qtile.cmd_spawn('kitty')}
        ),

        widget.Battery(
            foreground=dracula_colors[8],
            background=dracula_colors[0],
            format='\ue0b7 {char} {percent:2.0%} {hour:d}:{min:02d} ',
            charge_char='C',
            discharge_char='D',
            unknown_char='F',
            hide_threshold=0.9,
            low_foreground=dracula_colors[9],
            update_interval=60
        ),

        widget.CheckUpdates(
            background=dracula_colors[0],
            colour_have_updates=dracula_colors[9],
            distro='Arch_checkupdates',
            display_format='\ue0b7 \uf0f3  Updates: {updates}',
            #no_update_string='\ue0b7 \uf0a2  Updated ',
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                myTerm + ' --hold -e paru -Syu')},
            colour_no_updates=dracula_colors[4]
        ),

        widget.Volume(
            #emoji = True,
            background=dracula_colors[0],
            foreground=dracula_colors[5],
            mouse_callbacks={
                'Button3': lambda: qtile.cmd_spawn('pavucontrol')},
            #fontsize = 14,
            fmt='\ue0b7 \uf9c2 {}'
        ),

        widget.Clock(
            foreground=dracula_colors[7],
            background=dracula_colors[0],
            #fontsize = 14,
            format="\ue0b7   %H:%M:%S"
        ),

        widget.Clock(
            foreground=dracula_colors[4],
            background=dracula_colors[0],
            #fontsize = 14,
            format="\ue0b7    %A %d/%m/%Y"
        ),

        widget.WidgetBox(
            foreground=dracula_colors[7],
            text_open=' \ufc96',
            text_closed='\ue0b7 \ufc95',
            close_button_location='right',
            widgets=[
                widget.OpenWeather(
                    foreground=dracula_colors[7],
                    background=dracula_colors[0],
                    format="\ue0b7 \uf2c7 {main_temp}º{units_temperature} {location_city} {icon} ",
                    languaje='es',
                    location='Marbella,ES'
                ),
            ]
        ),

        widget.Wallpaper(
            directory='~/wallpapers',
            wallpaper_command=['nitrogen', '--head=0', '--set-zoom-fill', '--random'],
            label='\ue0b7   ',
            foreground=dracula_colors[4]
            # fontsize=14
        ),

        widget.TextBox(
            fmt='\ue0b7',
            foreground=dracula_colors[6],
        ),

        widget.Systray(
            background=dracula_colors[0],
            icon_size=20,
            padding=5
        ),

        # widget.Wlan(
        #        interface = 'wlp2s0',
        #        format = '{essid}: {percent:2.0%}'
        #    ),

        widget.TextBox(
            fmt='\ue0b7',
            foreground=dracula_colors[7],
        ),

        widget.QuickExit(
            default_text=' \uf842 ',
            countdown_format='[{}]',
            foreground=dracula_colors[7]
        ),

    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_list2():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

        widget.Image(
            filename="~/.config/qtile/icons/garuda-purple.png",
            iconsize=9,
            background=dracula_colors[0],  # colors[15],
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('nwggrid -p -o 0.4')}
        ),

        widget.GroupBox(

            **base(bg=dracula_colors[0]),  # colors[15]),
            font='UbuntuMono Nerd Font',

            fontsize=16,
            margin=5,
            padding=3,
            #margin_y=3,
            #margin_x=2,
            #padding_y=5,
            #padding_x=4,
            borderwidth=5,

            active=dracula_colors[1],  # colors[5],
            inactive=dracula_colors[3],  # colors[6],
            rounded=True,
            # highlight_method='block',
            highlight_method='line',
            highlight_color=dracula_colors[2],  # When in 'line' method
            fontshadow=dracula_colors[0],
            urgent_alert_method='block',
            urgent_border=dracula_colors[6],  # colors[16],
            this_current_screen_border=dracula_colors[7],  # colors[20],
            this_screen_border=dracula_colors[8],  # colors[17],
            other_current_screen_border=dracula_colors[4],  # colors[13],
            other_screen_border=dracula_colors[5],  # colors[17],
            disable_drag=True

        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=dracula_colors[1],  # colors[5],
            background=dracula_colors[0],  # colors[3],
            padding=0,
            scale=0.7
        ),

        widget.CurrentLayout(
            foreground=dracula_colors[1],  # colors[5],
            background=dracula_colors[0],  # colors[3]
            fmt=' {} '
        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.WindowCount(
            foreground=dracula_colors[5],
            fmt=' {} '
        ),

        widget.Sep(
            linewidth=0,
            padding=2,
            background=dracula_colors[7]
        ),

        widget.TaskList(
            highlight_method='border',  # border or block
            # icon_size=19,
            max_title_width=150,
            rounded=True,
            fontsize=16,
            border=dracula_colors[8],  # colors[7],
            foreground=dracula_colors[7],  # colors[9],
            unfocused_border=dracula_colors[3],
            margin=0,
            padding=0,
            txt_floating='🗗',
            txt_minimized='>_ ',
            borderwidth=2,
            background=dracula_colors[0],  # colors[20],
            #unfocused_border = 'border'
        ),

        widget.TextBox(
            fmt=' \ufce8 ',
            fontsize=20,
            foreground=dracula_colors[7],
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + ' --hold -e htop'),
                             'Button3': lambda: qtile.cmd_spawn('kitty')}

        ),

        widget.Volume(
            #emoji = True,
            background=dracula_colors[0],
            foreground=dracula_colors[5],
            mouse_callbacks={
                'Button3': lambda: qtile.cmd_spawn('pavucontrol')},
            #fontsize = 14,
            fmt='\ue0b7 \uf9c2 {}'
        ),

        widget.Clock(
            foreground=dracula_colors[7],
            background=dracula_colors[0],
            #fontsize = 14,
            format="\ue0b7   %H:%M:%S"
        ),

        widget.Clock(
            foreground=dracula_colors[4],
            background=dracula_colors[0],
            #fontsize = 14,
            format="\ue0b7    %A %d/%m/%Y"
        ),

        widget.WidgetBox(
            foreground=dracula_colors[7],
            text_open=' \ufc96',
            text_closed='\ue0b7 \ufc95',
            close_button_location='right',
            widgets=[

                widget.Battery(
                    foreground=dracula_colors[8],
                    background=dracula_colors[0],
                    format='\ue0b7 {char} {percent:2.0%} {hour:d}:{min:02d} ',
                    charge_char='C',
                    discharge_char='D',
                    unknown_char='F',
                    hide_threshold=0.9,
                    low_foreground=dracula_colors[9],
                    update_interval=60
                ),

                widget.Wttr(
                    location={'Marbella, Spain': '\ue0b7 '},
                    lang='es',
                    foreground=dracula_colors[7],
                    format=' %l %c %t  '
                ),
            ]
        ),


        widget.Wallpaper(
            directory='~/wallpapers',
            wallpaper_command=['nitrogen', '--head=1',
                               '--set-zoom-fill', '--random'],
            label=' \ue0b7    ',
            foreground=dracula_colors[4]
            # fontsize=14
        ),


    ]
    return widgets_list


widgets_list2 = init_widgets_list2()


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list2()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=20, opacity=1, background="000000")),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=20, opacity=1, background="000000"))]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button3", lazy.spawn('jgmenu_run')),
    #Click([mod], "Button2", lazy.spawn("jgmenu_run"))
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []

auto_minimize = True

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
@hook.subscribe.client_new
async def assign_app_group(client):
    d = {}
    #########################################################
    ################ assgin apps to groups ##################
    #########################################################
    d["1"] = ["Navigator", "Firefox", "Brave", "Brave-browser",
              "navigator", "firefox", "brave", "brave-browser", ]
    d["2"] = ["Emacs", "Subl3", "Geany", "Brackets", "Code-oss", "Code",
              "emacs", "subl3", "geany", "brackets", "code-oss", "code", ]
    d["3"] = ["Obs", "Obs-studio",
              "obs", "obs-studio" ]
    d["4"] = ["Steam", "Steam-runtime", "Heroic", "Lutris", "Minecraft-launcher", "Itch", "Minigalaxy", "Retroarch",
              "steam", "steam-runtime", "heroic", "lutris", "minecraft-launcher", "itch", "minigalaxy", "retroarch" ]
    d["5"] = ["Mpv", "Vlc", "Gimp", "Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
              "mpv", "vlc", "gimp", "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
    d["6"] = ["" ]
    d["7"] = ["Telegram-desktop", "Discord", "Element-desktop",
              "telegram-desktop", "discord", "element-desktop", ]
    d["8"] = ["Clementine", "Spotify", "Pragha", "Deadbeef", "Audacious",
              "clementine", "spotify", "pragha", "deadbeef", "audacious", ]
    d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
              "evolution", "geary", "mail", "thunderbird" ]
    d["0"] = ["Pcmanfm", "Pcmanfm-qt", "Dolphin", "Thunar",
              "pcmanfm", "pcmanfm-qt", "dolphin", "thunar", ]
    ##########################################################
    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            if client.name == 'spotify' or client.name == 'minecraft-launcher':
                await asyncio.sleep(0.01)
            client.togroup(group)
            client.group.cmd_toscreen()


# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    # Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),


],  fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "smart"  # "focus" # or smart

wmname = "LG3D"
