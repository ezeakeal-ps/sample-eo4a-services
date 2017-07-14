sleep=$1

i=1
while [ "$i" -le "$sleep" ]; do
  progress=$((100*$i/$sleep))
  echo "$progress sleeping.." > $STATUS_FILE
  sleep 1
  i=$(($i + 1))
done