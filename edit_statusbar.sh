#!/bin/bash

# This script attempts to edit the status bar time in screenshots
# Note: This is a basic approach and may not look perfect

for file in assets/screenshots/*.PNG; do
    echo "Processing $file..."

    # Get image dimensions
    width=$(magick identify -format "%w" "$file")
    height=$(magick identify -format "%h" "$file")

    # Calculate status bar region (top 100 pixels typically)
    # We'll overlay the time at approximately 60 pixels from the right

    # Create a temporary file
    temp_file="${file%.PNG}_temp.PNG"

    # Draw a filled rectangle to cover old time (approximate position)
    # Then add new time text "9:41"
    magick "$file" \
        -fill white -draw "rectangle $((width-90)),10 $((width-20)),40" \
        -font "Helvetica" -pointsize 28 -fill black \
        -draw "text $((width-75)),35 '9:41'" \
        "$temp_file"

    # Replace original with temp file
    mv "$temp_file" "$file"

    echo "Updated $file"
done

echo "Done! Note: Battery indicator update requires more complex image manipulation."
echo "For best results, consider retaking screenshots with Xcode simulator configured to show clean status bar."
