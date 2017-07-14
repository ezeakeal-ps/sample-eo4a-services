# Read the CMD args
input_dir=$1
output_dir=$2

# Mkdir if required (possible)
mkdir -p $output_dir

# Do the actual work
echo "Starting GDAL Warp Script on dir: $input_dir"
find $input_dir -name '*.tif' | while read tiff_path; do 
    output_path="$output_dir/$(basename $tiff_path)"
    echo "Gdalwarping $tiff_path -> $output_path"
    gdalwarp -co COMPRESS=LZW -overwrite -tr 1000 1000 "$tiff_path" "$output_path"
done

# Example of updating the WPS status
echo "20 Wasting some time" > $STATUS_FILE
sleep 5
