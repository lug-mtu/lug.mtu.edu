---
title: Vim
date: 2022-01-13
tags: minutes,vim
meeting-index: 10
author: David Hochstetler
template: minutes
---

## Making Vim More Usable
An extension to Steven's vim presentation to try and make using Vim a bit easier. The point of this is to try and reach a point of usability so that vim has some of the features that other code editors, like VsCode, has. Features such as extensibility, autocomplete, file exploration, buffer tabbing, and git integration. I am also assuming you paid attention to his presentation so I will gloss over some of the basics.
### Neovim Not Vim
First of all, we will be using Neovim instead of Vim because it is much more extensible, has a well documented API, and is supported by many of the plugins we will be using today. I will probably just call it Vim becuase I am too lazy to try and maintain any sort of consistency.
### Basic Setup
These are some sane default settings to get you started with configuring Vim. These are configurations that make vim a bit more usable without needing to use plugins...yet.
```vim
set tabstop=4 softtabstop=4
set shiftwidth=4
set expandtab
set smartindent
set exrc
set relativenumber
set nu
set nohlsearch
set hidden
set noerrorbells
set nowrap
set noswapfile
set nobackup
set undodir=~/.vim/undodir
set undofile
set incsearch
set termguicolors
set scrolloff=8
set colorcolumn=80
set signcolumn=yes
set updatetime=100
set encoding=utf-8
set showtabline=2
set ruler
set clipboard=unnamedplus
set timeoutlen=100
set mouse+=a
```
Alright, so this is a lot and you may not need all of them, these are just some of my personal preferences. I am not going through all of them because I am lazy (and do not know what all of these do) but I can go through a few.
* set noerrorbells -> Shuts the error bells off
* set nu -> Enables line numbering
* set relativenumber -> Line numbering now shows you numbers for jump distances
* set mouse += a -> Allows for the mouse to be used in Vim (I know, heresy)
* set clipboard=unnamedplus -> Allows you to copy and paste to and from the current Vim buffer
* set colorcolumn=80 -> Sets a column at 80 spaces (make code more good)

Now it's time for some remaps that makes using Vim slightly more gooder. Before we started, the different types of remaps are:
```vim
nnoremap          Normal mode remaps
inoremap          Insert and Replace mode remap
vnoremap          Visual and Select mode remap
xnoremap          Visual mode remap
```
Here are some of the remaps that I use that I find make Vim a bit easier to use. Many of these are personal preference and can be changed to better suit what you want out of Vim.
```vim
" Remap nav keys one to the right. I know this is considered a great evil in the Vim community
" but I am lazy and don't want to have to move my hands over one key to the left for navigation
noremap ; l
noremap l k
noremap k j
noremap j h

" Remap jk and kj to <Esc>. The escape key is too far away
inoremap jk <Esc>
inoremap kj <Esc>

" Better tabbing remaps allows you to use < and > to shift a line left or right by one tab
vnoremap < <gv
vnoremap > >gv

" Remap redo to Shift+U which makes more sense, fight me
noremap U <C-R>

" Better way of splitting vertically
nnoremap <C-g> :vsplit<enter>

" Better way of spliting horizontally
nnoremap <C-t> :sp<enter>

" Better window navigation
nnoremap <C-a> <C-w>h
nnoremap <C-s> <C-w>j
nnoremap <C-w> <C-w>k
nnoremap <C-d> <C-w>l
```
### PLUGINS!!!!
Now this is where things begin to get interesting and make Vim actually fun to use. Here, we are going to use vim-plug solely because it was the first plugin manager for Vim that popped up when I searched for it. The link to the github is https://github.com/junegunn/vim-plug. 
Scroll down the page and you should see a command for installing vim-plug on Linux for Neovim that looks similar to:
```
sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
```
Now remember to just blindly download and trust this command without any hesitation and assume there is nothing malicious about it. This is always a great idea and never backfires. This is especially a great practice for mission critical systems.
Terrible humor aside, there are some basic commands to know to use vim-plug.
```
:PlugInstall			# This installs all plugins that are not currently plugged in
:PlugUpdate				# This updates all currently installed plugins
:PlugClean				# This removes all plugins that are not currently installed installe
```
For including actual plugs that you want to be installed, just add this to your init.vim file.
```vim
call plug#begin('~/.vim/plugged')
    
    Plug 'PLUG/NAME'

call plug#end()
```
### Making Vim Fly as Heck
So, the first and most important step to making Vim a bit more useful is to make it super stylish. This is actaully pretty simple as it takes only a few plugs and some basic configuration.
```vim
    Plug 'gruvbox-community/gruvbox'
    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'
```
Then close and reopen your init.vim and run the :PlugInstall command to install these commands. These three lines have installed the Vim airline theming extension which allows for a wide variety of customization. The other one installed gruvbox, the most epicest theme know to all of mankind.
Now add these to your init.vim after your plug section to configure them
```vim
colorscheme gruvbox
let g:airline_theme='gruvbox'
```
Now we have a mildly better status bar and a theme that 10000 times better.
### File Exploration
You can pretty easily open up files with buffers and use that. The only problem with this is that it requires us to know like three commands and that is two too many. Instead, we will use one command and a plugin called nerdtree. Nerdtree is a file explorer built for Vim that is similar to the one found in VsCode. To install the plugin is just add the following plugin.
```vim
    Plug 'preservim/nerdtree'
```
Now let's remap opening and closing the file explorer to ctrl+e and allow it to see the hidden files in your project as well.
```vim
noremap <silent>  	<c-e> :NERDTreeToggle<CR>			" Toggle the file explorer with ctrl+e
let NERDTreeShowHidden=1       							" See hidden files
```
And that is all you need to setup a basic file explorer in Vim. Imagine how lame it would be to have it just be built in, who wants that kind of convenience??
### File Tabbing
Ok congratulations, you can open multple files, but you have buffers to deal with now. They are a bit annoying to deal with but luckily, we have an extension to help deal with that. This magnificent extension is barbar.vim. With this extension, newly opened files will open up as tabs like they do in most other text editors and IDE's. To intsall it is as simple as adding this to your plug section.
```vim
    Plug 'kyazdani42/nvim-web-devicons'
    Plug 'romgrk/barbar.nvim' 
```
Now you have barbar itself as well as an extension that gives you icon support to differentiate your tabs a bit more. Now, you could just click on each tab to navigate between them which is fine but you can add keybindings for navigation. Some basic remaps are
```vim
" Use alt+, or alt+. to move to the left or right buffer
nnoremap <silent>    <A-,> :BufferPrevious<CR>
nnoremap <silent>    <A-.> :BufferNext<CR>

" Use alt+number to move to that tab
nnoremap <silent>    <A-1> :BufferGoto 1<CR>
nnoremap <silent>    <A-2> :BufferGoto 2<CR>
nnoremap <silent>    <A-3> :BufferGoto 3<CR>
nnoremap <silent>    <A-4> :BufferGoto 4<CR>
nnoremap <silent>    <A-5> :BufferGoto 5<CR>
nnoremap <silent>    <A-6> :BufferGoto 6<CR>
nnoremap <silent>    <A-7> :BufferGoto 7<CR>
nnoremap <silent>    <A-8> :BufferGoto 8<CR>
nnoremap <silent>    <A-9> :BufferGoto 9<CR>

" Use alt+c to close the current buffer
nnoremap <silent>    <A-c> :BufferClose<CR>
```
### Improved Finding and Replacing
Finding and replacing in vim takes too much time and effort.  Good thing there is a plugin for that. The one we are using is far.vim and needs to be plugged with
```vim
    Plug 'brooth/far.vim'
```
After it is plugged we can then configure it to use more sensible shortcuts to find and replace words. Yet another step closer to getting to what VsCode is out of the box, let's gooo.
```vim
" use ctrl+f to find
nnoremap <silent> <C-f>  :Farf<cr>
vnoremap <silent> <C-f>  :Farf<cr>

" use ctrl+r to replace
nnoremap <silent> <C-r>  :Farr<cr>
vnoremap <silent> <C-r>  :Farr<cr>
```
### Autocomplete with COC
COC is really good and stands for Conquer on Completion. It is a really nice and easy way to get autocompletion for multiple languages setup quickly. Basic setup is really quick and easy. It requires you to only plug it and install your desired language servers. Oh yeah, it also requires the latest LTS release of node and npm. To plug it just add this to your plugs.
```vim
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
```
Once you get it installed, you can just run the :CocInstall command to install a language server. The full list of supported language servers can be found here https://github.com/neoclide/coc.nvim/wiki/Language-servers. For example let's say you want to add python support, you just have to run the following command.
```vim
:CocInstall coc-pyright
```
You can set up individual settings for each language in the `coc-settings.json`. I am not getting into that though as I don't know how it works and I am too lazy to figure it out. But you know what I did figure out that is actually super nice to have, tab autocompletion. You can set this with a little vimscript function.
```vim
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction
```
I'm gonna be honest with you, I have no idea what is going on here, I just yoinked it from the COC github and it works.

### Extra, Nice to Have Plugins
These are just a few other plugins that I use personally that make my life substantially easier. The first of which is an autopairs plugin that types in the matching bracket or brace for you. This one just needs to be plugged with no extra setup.
```vim
    Plug 'jiangmiao/auto-pairs'
```
The next one is really only helpful when I work on css files. This plugin highlights the color of hex color codes in their associated color. Once again this one only needs to be plugged.
```vim
    Plug 'ap/vim-css-color'
```

## The End

