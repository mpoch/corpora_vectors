#!/bin/bash

set -e

fl_dir="/home/mpoch/upf_local/tools/freeling/freeling-3.0"
#fl_dir="/usr"

ca_port="40004"
es_port="50005"
en_port="60006"

"$fl_dir/bin/analyze" --server --port "$es_port" --flush -f "$fl_dir/share/freeling/config/es.cfg" &
"$fl_dir/bin/analyze" --server --port "$en_port" --flush -f "$fl_dir/share/freeling/config/en.cfg" &
"$fl_dir/bin/analyze" --server --port "$ca_port" --flush -f "$fl_dir/share/freeling/config/ca.cfg" &

# cat test.tmp | /home/mpoch/upf_local/tools/freeling/freeling-3.0/bin/analyzer_client 50005
