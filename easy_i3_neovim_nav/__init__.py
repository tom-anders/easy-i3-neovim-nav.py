#! /usr/bin/env python3

import re
import argparse

import i3ipc
import pynvim

def moveInNvim(nvim, direction):
    nvim.command('let oldwin = winnr()') 
    i3DirectionToNvim = {
            'left' : 'h',
            'right' : 'l',
            'up': 'k',
            'down': 'j',
            }
    nvim.command('wincmd ' + i3DirectionToNvim[direction])
    return nvim.eval('oldwin != winnr()')

def canResizeNvimWidth(nvim):
    columns = int(nvim.eval('&columns'))
    winwidth = int(nvim.eval(f'winwidth(winnr())'))

    return columns != winwidth

def canResizeNvimHeight(nvim):
    lines = int(nvim.eval('&lines'))

    winheight = int(nvim.eval(f'winheight(winnr())'))
    cmdheight = int(nvim.eval('&cmdheight'))

    # The "2" is to account for statusline and bufferline
    return (lines - winheight - cmdheight) > 2

def moveOrResizeInNvim(focused, args):
    try:
        match = re.search(re.compile(args.path_regex), focused)
        nvim = pynvim.attach('socket', path = match.group(0))
        if not nvim:
            return False
    except:
        return False

    if args.subparser == 'focus':
        return moveInNvim(nvim, args.direction)
    elif args.subparser == 'resize':
        if args.dimension == 'width' and canResizeNvimWidth(nvim):
            nvim.command(str(args.amount_vim) + 'wincmd ' + ('<' if args.action == 'shrink' else '>'))
            return True
        elif args.dimension == 'height' and canResizeNvimHeight(nvim):
            nvim.command(str(args.amount_vim) + 'wincmd ' + ('-' if args.action == 'shrink' else '+'))
            return True

    return False

def moveOrResizeInI3(i3, args):
    if args.subparser == 'focus':
        i3.command(f'focus {args.direction}')
    elif args.subparser == 'resize':
        i3.command(f'resize {args.action} {args.dimension} {args.amount_i3_px} px or {args.amount_i3_ppt} ppt')

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path-regex', type=str, default=r'(?<=\[)\S+(?=\]$)', \
            help="Regex used to extract neovim's v:servername from the window's title string. \
            The default regex assumes that the servername is contained in square brackets \
            at the very end of the title string.")
            
    subparsers = parser.add_subparsers(dest='subparser', help='action corresponding to i3 config')

    parser_focus = subparsers.add_parser('focus')
    parser_focus.add_argument('direction', type=str, choices=['left', 'right', 'up', 'down'],
                              help='direction in which focus shall be moved')

    parser_resize = subparsers.add_parser('resize')
    parser_resize.add_argument('action', type=str, choices=['shrink', 'grow'])
    parser_resize.add_argument('dimension', type=str, choices=['width', 'height'])
    parser_resize.add_argument('amount_vim', type=int, \
            help="will be passed as a count to vim's wincmd, see :h wincmd")
    parser_resize.add_argument('amount_i3_px', type=int,\
            help='number of pixels by which to resize a floating window, \
                  for details see https://i3wm.org/docs/userguide.html#resizingconfig')
    parser_resize.add_argument('amount_i3_ppt', type=int, \
            help='percentage points by which to resize a tiled window, \
                  for details see https://i3wm.org/docs/userguide.html#resizingconfig')

    args = parser.parse_args()

    if not args.subparser:
        parser.print_help()
        exit()

    i3 = i3ipc.Connection()
    focused = i3.get_tree().find_focused().name

    if not moveOrResizeInNvim(focused, args):
        moveOrResizeInI3(i3, args)

if __name__ == "__main__":
    main()
