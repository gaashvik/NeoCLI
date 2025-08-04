# In main.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$(realpath "$SCRIPT_DIR/../backend/main.py")"
source "$SCRIPT_DIR/helper.sh"

enforce_histfile_size() {
    tail -n "${HISTFILESIZE:-500}" "$HISTFILE" > "${HISTFILE}.tmp" && mv "${HISTFILE}.tmp" "$HISTFILE"
}
function neo() {
        local meta_dir=$(search_for_metadata_dir)
        if [[ -n "$meta_dir" ]]; then
            echo "Found .neocli file at: $meta_dir"
        else
            echo "Could not find metadata file."
            return 1
        fi
        local subcommand=$1
        shift
        # local global_hist="$HISTFILE"
        # echo "$HISTFILE"
        # local local_hist="$PWD/.neocli/.neocli_history"
        # export HISTFILE="$local_hist"
        case "$subcommand" in 

        shell)
        # history -a
        # local global_hist="$HISTFILE"
        # echo "$HISTFILE"
        # local local_hist="$meta_dir/.neocli/.neocli_history"
        # touch "$local_hist"
        # export HISTFILE="$local_hist"
        # echo "$HISTFILE"
        # history -s "#dummy"
        # history -r
        # echo "🚀 Starting aicopilot REPL (manual mode)..."
        # while true; do
        #     read -e -p "aicopilot> " cmd
        #     if [[ "$cmd" == "exit" ]]; then
        #         history -s "$cmd"
        #         history -a
        #         enforce_histfile_size
        #         export HISTFILE="$global_hist"
        #         echo "$HISTFILE"
        #         break
        #     fi

        #     history -s "$cmd"
        #     local out=$( eval "$cmd" )
        #     echo $out
        # done
        PYTHON_SCRIPT="$(realpath "$SCRIPT_DIR/../backend/main.py")"
        python "$PYTHON_SCRIPT" "$meta_dir"

    ;;

    help|"")

    echo "Usage: aicopilot <command>"
      echo "Commands:"
      echo "  init        Initialize .aicopilot in this project"
      echo "  index       Build or rebuild the vector index"
      echo "  shell       Start interactive REPL"
      echo "  help        Show this message"
    ;;

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
    *)

    echo "Command not found"
    ;;

    esac

}

