from setuptools import setup

setup(name='easy_i3_neovim_nav',
      version='1.7',
      description='Quickly navigate and resize i3wm windows and Neovim splits with the same keybindings',
      keywords='i3wm vim nvim neovim',
      classifiers = [
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent'
      ],
      url='http://github.com/tom-anders/easy_i3_neovim_nav',
      author='Tom Praschan',
      author_email='tom@praschan.de',
      license='GPLv3',
      packages=['easy_i3_neovim_nav'],
      project_urls = {
          'Bug Tracker': 'http://github.com/tom-anders/easy_i3_neovim_nav/issues',
      },
      scripts = ['bin/easy-i3-neovim-nav'],
      zip_safe=False)

