#!/bin/sh

while read user group; do
    g_sid=`wbinfo -n "$group"`
    g_gid=`wbinfo -Y "$g_sid"`
    wbinfo -r "$user" | grep -qs "^$g_gid\$" 2>/dev/null && echo "OK" || echo "ERR"
done
