# fish completion for qnote

function __fish_qnote_complete
    set -lx COMP_WORDS (commandline -opc)
    set -lx COMP_CWORD (count $COMP_WORDS)
    set -lx _QNOTE_COMPLETE fish_complete
    qnote
end

complete -c qnote -f -a '(__fish_qnote_complete)'
