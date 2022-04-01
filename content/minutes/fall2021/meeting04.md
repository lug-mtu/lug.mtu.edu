---
title: vim talk
date: 2021-10-21
tags: minutes,vim
author: Steven Whitaker
template: minutes
---
### Technical Information

We talked about vim and how to set it up. We followed going through this .vimrc:

```vim
set number
set nu
set clipboard=unnamed
syntax on
colorscheme monokai
set termguicolors

call plug#begin('~/.vim/autoload')
Plug 'scrooloose/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'davidhalter/jedi-vim'
call plug#end()

let g:airline_theme='deus'

nmap <F2> :NERDTreeToggle<CR>
```

Half the talk was on topics in vimtutor, and the other half was on plugins.
This was an introductory talk to get people to use vim and not an in-depth
explanation. To be frank, I don't have in-depth knowledge of vim, so it's
not really something I would have been able to do.

## LUG Internal Updates

Going to call RSO because they do not respond to my emails anymore.

We talked with NCSA to work with Kubernetes for our system.
Rekhi 101 was locked, so we instead walked around Fisher until we found an open room and went there instead. I honestly have no idea where we ended up at.
