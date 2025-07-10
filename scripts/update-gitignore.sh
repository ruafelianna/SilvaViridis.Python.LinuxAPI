#!/usr/bin/env bash

# dependencies check

if ! command -v curl &> /dev/null; then
    echo "Error: curl is required!" >&2
    exit 1
fi

# config

GITIGNORE='.gitignore'
REPO='https://raw.githubusercontent.com/github/gitignore/refs/heads/main'

declare -A GI_FILES=(
    ['Python']="${REPO}/Python.gitignore"
    ['VisualStudio']="${REPO}/VisualStudio.gitignore"
    ['VisualStudioCode']="${REPO}/Global/VisualStudioCode.gitignore"
)

# script

rm -f "${GITIGNORE}"

for gi_file in "${!GI_FILES[@]}"; do
    # create header
    border_length=$(( ${#gi_file} + 4 ))
    border=$(eval "printf '#%.0s' {1..$((border_length))}")

    printf "%s\n# %s #\n%s\n\n" "${border}" "${gi_file}" "${border}" >> "${GITIGNORE}"

    # download content
    url="${GI_FILES[${gi_file}]}"

    echo "Downloading ${gi_file}..."

    if curl -fsSL -A "Create-Gitignore-Script" "${url}" >> "${GITIGNORE}"; then
        printf "\n\n" >> "${GITIGNORE}"
        echo "Success."
    else
        echo "Failed to download ${gi_file}." >&2
        rm -f "${GITIGNORE}"
        echo "The script will be aborted." >&2
        exit 2
    fi
done
