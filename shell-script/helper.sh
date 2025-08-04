search_for_metadata_dir(){
    local folder_name=".neocli"
    local directory="$PWD"
    while [[ "$directory" != "/" ]];do
        if [[ -d "${directory}/${folder_name}" ]];then
            echo "$directory"
            return 0
        fi
        directory="$(dirname "$directory")"
    
    done

    return 1;
}