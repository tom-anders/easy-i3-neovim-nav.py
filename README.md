# This project is not maintained anymore, please use the [Rust version](https://github.com/tom-anders/easy-i3-neovim-nav) instead!

# easy-i3-neovim-nav

Quickly navigate and resize i3wm windows and Neovim splits with the same keybindings

This script is heavily inspired by

- [i3-vim-nav](https://github.com/termhn/i3-vim-nav)
- [i3-vim-focus](https://github.com/jwilm/i3-vim-focus)
- [i3-dispatch](https://github.com/teto/i3-dispatch)

Here are the major advantages to the solutions listed above:
- Also supports seemless resizing of i3 windows and vim splits
- Does not rely on `xdotool`, thus avoiding
  [an annoying bug where your modifier key might get stuck after switching windows](https://github.com/jordansissel/xdotool/issues/43)
  and providing better performance in general
- No need for an additional vim-plugin, only needs three additional lines in your `init.vim`

# Installation

    pip install easy-i3-neovim-nav

# Usage

## Neovim configuration

Add this to your `init.vim`:

    call serverstart(tempname())
    let &titlestring="nvim %F -- [" . v:servername . "]"
    set title

> **_Note:_** `easy-i3-neovim-nav` uses the window's titlestring in order to extract the server name
used for communicating with Neovim. The default regex assumes that the servername is contained in
square brackets at the very end of your `titlestring`. To customize this, use the `--path-regex` option

## i3wm configuration

Here's an example configuration for your i3 config. Adapt this to your preferred current keybindings

    # Move focus
    bindsym $mod+h exec --no-startup-id easy-i3-neovim-nav focus left
    bindsym $mod+j exec --no-startup-id easy-i3-neovim-nav focus down
    bindsym $mod+k exec --no-startup-id easy-i3-neovim-nav focus up
    bindsym $mod+l exec --no-startup-id easy-i3-neovim-nav focus right

    # Resizing                                                               
    bindsym $mod+Shift+Left  exec --no-startup-id easy-i3-neovim-nav resize shrink width  5 10 5
    bindsym $mod+Shift+Down  exec --no-startup-id easy-i3-neovim-nav resize shrink height 5 10 5
    bindsym $mod+Shift+Up    exec --no-startup-id easy-i3-neovim-nav resize grow   height 5 10 5
    bindsym $mod+Shift+Right exec --no-startup-id easy-i3-neovim-nav resize grow   width  5 10 5

The last three arguments control the amount by which windows are resized:

    $ easy_i3_neovim_nav resize -h
    usage: easy_i3_neovim_nav.py resize [-h] {shrink,grow} {width,height} amount_vim amount_i3_px amount_i3_ppt

    positional arguments:
      {shrink,grow}
      {width,height}
      amount_vim      will be passed as a count to vim's wincmd, see :h wincmd
      amount_i3_px    number of pixels by which to resize a floating window, for details see
                      https://i3wm.org/docs/userguide.html#resizingconfig
      amount_i3_ppt   percentage points by which to resize a tiled window, for details see
                      https://i3wm.org/docs/userguide.html#resizingconfig

    optional arguments:
      -h, --help      show this help message and exit
