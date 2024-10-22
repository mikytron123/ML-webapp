
/usr/local/bin/quickwit run &

pid=$!

sleep 10

/usr/local/bin/quickwit index create --index-config index-config.yaml

wait $pid
