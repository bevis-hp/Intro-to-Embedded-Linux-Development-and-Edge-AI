#!/bin/bash

# devcat - A mysterious feline translator

if [ -z "$1" ]; then
    echo "  /\_/\  "
    echo " ( o.o ) "
    echo "  > ^ <  "
    echo "Meow, I'm devcat! Nice to meet you."
    echo "I can turn your files into the language of devcat!"
    echo "Usage: $0 <text_file>"
    exit 1
fi

target_file="$1"

if [ ! -f "$target_file" ]; then
    echo "Meow? I can't find that file."
    exit 1
fi

# Count the words in the file
word_count=$(wc -w < "$target_file")
new_content=""

# Generate a meow for every word
for (( i=1; i<=word_count; i++ ))
do
    new_content+="meow "
done

# Overwrite the original file with the new content
echo "$new_content" > "$target_file"

echo "  /\_/\  "
echo " ( o.o ) "
echo "  > ^ <  "
echo ""
echo "Purrfect! '$target_file' has been completely translated."
