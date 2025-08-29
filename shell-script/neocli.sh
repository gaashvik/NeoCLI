# In main.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENTERY_SCRIPT="$(realpath "$SCRIPT_DIR/../backend/main.py")"
INDEX_SCRIPT="$(realpath "$SCRIPT_DIR/../backend.services.index_codebase")"
VENV_PYTHON="$SCRIPT_DIR/../.venv/bin/python"
source "$SCRIPT_DIR/helper.sh"

enforce_histfile_size() {
    tail -n "${HISTFILESIZE:-500}" "$HISTFILE" > "${HISTFILE}.tmp" && mv "${HISTFILE}.tmp" "$HISTFILE"
}
function neo() {
   local subcommand=$1
    shift
    local meta_dir
    local cwd="$PWD"
    meta_dir=$(search_for_metadata_dir)

    if [[ -n "$meta_dir" ]]; then
        echo "Found .neocli file at: $meta_dir"
    else
        if [[ "$subcommand" != "init" && -n "$subcommand" ]]; then
            echo "Could not find metadata file. Please initialize the neo file."
            return 1
        fi
    fi
        # local global_hist="$HISTFILE"
        # echo "$HISTFILE"
        # local local_hist="$PWD/.neocli/.neocli_history"
        # export HISTFILE="$local_hist"
        case "$subcommand" in 
        init)

    if [[ -z "$1" ]]; then
    echo "❌ Project name is required. Usage: aicopilot init <project-name>"
    return 1
    fi
    local name=$1
    shift
    local root=".neocli"
    mkdir -p "$root/chroma"
    touch "$root/.neocli_history" "$root/session.json" "$root/memory.jsonl" "$root/config.json"
cat <<EOF > "$root/config.json"
{
  "project": "$name",
  "version": "0.1.0"
}
EOF
;;


        shell)
        PYTHONPATH="${SCRIPT_DIR}/.." "$VENV_PYTHON" -m backend.main "$meta_dir" "$cwd"

    ;;

    help|"")

    echo "Usage: aicopilot <command>"
      echo "Commands:" 
      echo "  init        Initialize .aicopilot in this project"
      echo "  index       Build or rebuild the vector index"
      echo "  shell       Start interactive REPL"
      echo "  help        Show this message"
    ;;

   
    index)
    PYTHONPATH="${SCRIPT_DIR}/.." "$VENV_PYTHON" -m backend.services.index_codebase "$meta_dir" "$cwd"
    ;;
    *)

    echo "Command not found"
    ;;

    esac

}

