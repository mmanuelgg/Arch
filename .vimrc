"" General
packadd! dracula        " Dracula colorscheme need download
syntax enable           " enable instead of on to keep colorscheme
colorscheme dracula
" Enable transparency
hi Normal guibg=NONE ctermbg=NONE
""set background=dark
filetype on
filetype plugin on
filetype indent on
set cursorline
set showcmd
set showmode
set wildmenu
set number      " Show line numbers
set relativenumber
set linebreak   " Break lines at word (requires Wrap lines)
set showbreak=+++       " Wrap-broken line prefix
set textwidth=100       " Line wrap (number of cols)
set showmatch   " Highlight matching brace
set spell       " Enable spell-checking
set visualbell  " Use visual bell (no beeping)

set mouse=a
set hlsearch    " Highlight all search results
set smartcase   " Enable smart-case search
set ignorecase  " Always case-insensitive
set incsearch   " Searches for strings incrementally

set autoindent  " Auto-indent new lines
set expandtab   " Use spaces instead of tabs
set shiftwidth=4        " Number of auto-indent spaces
set smartindent " Enable smart-indent
set smarttab    " Enable smart-tabs
set softtabstop=4       " Number of spaces per Tab

"" Advanced
set ruler       " Show row and column ruler information

set undolevels=1000     " Number of undo levels
set backspace=indent,eol,start  " Backspace behaviour

inoremap jkj <esc>

set statusline=
set statusline+=\ %F\ %M\ %Y\ %R
set statusline+=%=
set statusline+=\ ascii:\ %b\ hex:\ 0x%B\ row:\ %l\ col:\ %c\ percent:\ %p%%
set laststatus=2


