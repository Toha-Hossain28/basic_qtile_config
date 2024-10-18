import os
import subprocess
from libqtile import hook
#*******
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([mod], "w", lazy.spawn("brave-browser"), desc="Spawn brave browser"),
    Key([mod], "c", lazy.spawn("code"), desc="Spawn VS Code"),
    Key([mod], "f", lazy.spawn("nautilus"), desc="Spawn file"),
    # Launch Rofi in window mode with Alt+Tab
    Key(["mod1"], "Tab", lazy.spawn("rofi -show window"), desc="Switch windows with Rofi"),
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    #brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    #Screenshot
    Key([mod], "Print", lazy.spawn("flameshot full -p ~/Pictures/"), desc="Take a screenshot with Flameshot"),
    Key(["shift"], "Print", lazy.spawn("flameshot gui"), desc="Take a screenshot with Flameshot without delay"),

]

# Add key bindings to switch VTs in Wayland. 
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width":3,
    "margin":5,
    "border_focus":"#D6BD98",
    "border_normal":"#243642"
}

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                # widget.TextBox(
                #     text="Toha",
                #     background="#ECE3CE",
                #     foreground="#000000",
                # ),
                # widget.GroupBox(
                #     background="#9EC8B9",
                #     foreground="#000000",
                # ),
                widget.GroupBox(
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 14,
                    margin_y = 2,
                    margin_x = 3,
                    padding_y = 2,
                    padding_x = 3,
                    borderwidth = 0,
                    disable_drag = True,
                    active = "#4c566a",
                    inactive = "#2e3440",
                    rounded = False,
                    highlight_method = "text",
                    this_current_screen_border = "#d8dee9",
                    foreground = "#4c566a",
                    background = "#9EC8B9"
                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),
                #widget.Prompt(),
                widget.WindowName(
                    font = "RobotoMono Nerd Font Bold",
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                # widget.TaskList(),
                # widget.Wlan(
                #     interface="wlp3s0",  # Replace 'wlan0' with your Wi-Fi interface (check with `ip a`)
                #     format="{essid} {percent:2.0%}",  # Shows SSID (network name) and signal strength in percentage
                #     foreground="#ffffff",  # Text color (white for visibility)
                #     background="#2e3440",  # Background color (dark for contrast)
                #     fontsize=12,  # Font size
                #     font="RobotoMono Nerd Font Bold",  # Font style
                #     disconnected_message="No Wi-Fi",  # Message when not connected
                #     update_interval=1.0,  # Update interval in seconds
                # ),
                widget.Net(
                    foreground = "#ffffff",  # Text color (dark)
                    background = "#A78295",  # Background color (dark)
                    font = 'RobotoMono Nerd Font Bold',  # Font used in the widget
                    fontsize = 12,  # Font size for the widget
                    format = '{down} ↓↑ {up}',  # Format showing download ↓ and upload ↑ speeds
                    interface = 'wlp3s0',  # Network interface to monitor (replace with your interface, e.g., 'wlan0')
                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),

                widget.Memory(
                    format='{MemUsed:.2f}G / {MemTotal:.2f}G',
                    measure_mem='G',  # Show memory usage in GB
                    update_interval=1.0,  # Update every second (adjust as needed)
                    background="#EB3678",  # Background color
                    foreground="#000000",  # Text color
                    fontsize=12,           # Font size
                    padding=5,             # Padding around the widget
                    font = "RobotoMono Nerd Font Bold",
                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),
                widget.Volume(
                    foreground="#000000",   # Text color
                    background="#D5CEA3",   # Background color
                    fontsize=12,            # Font size
                    # font="Ubuntu Mono",     # Font family
                    font = "RobotoMono Nerd Font Bold",
                    padding=5,              # Padding inside the widget
                    emoji=False,            # Set to True if you want volume level as emoji
                    # update_interval=0.1,    # How frequently to update volume in seconds
                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),
		        widget.Systray(

                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),
                # widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Clock(
                    foreground = "#2e3440",
                    background = "#F39F5A",
                    font = "RobotoMono Nerd Font Bold",
                    fontsize = 12,
                    format = "%D %H:%M",
                ),
                widget.Sep(
                    linewidth = 1,
                    padding = 5,
                    foreground = "#243642",
                    background = "#243642"
                ),
                # widget.QuickExit(),
                # shutdown replacement
                widget.TextBox(
                    text='\uf011',  # Unicode for FontAwesome power-off icon
                    foreground="#000000",  # Red color to indicate shutdown
                    background="#C060A1",  # Background color
                    fontsize=16,  # Set a larger font size for the icon
                    padding=5,   # Padding around the icon
                    font="FontAwesome",  # Use the FontAwesome font
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn("shutdown now")  # Left-click to shutdown
                    }
                ),
                # widget.Sep(
                #     linewidth = 1,
                #     padding = 5,
                #     foreground = "#243642",
                #     background = "#243642"
                # ),

            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#243642",
        ),
        # Wallpaper 
        wallpaper='/home/toha/Pictures/backpacker-7628303.jpg',
        wallpaper_mode='fill'
        
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# autostart thing
@hook.subscribe.startup_once
def autostart():
    subprocess.call([os.path.expanduser("~/.config/qtile/autostart.sh")])
