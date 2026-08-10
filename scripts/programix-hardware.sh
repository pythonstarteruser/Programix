#!/usr/bin/env bash

echo "================================"
echo "      🐧 PROGRAMIX HARDWARE"
echo "================================"
echo

echo "CPU:"

CPU_MODEL="$(awk -F: '/^model name/ {
    gsub(/^[ \t]+/, "", $2)
    print $2
    exit
}' /proc/cpuinfo)"

CPU_THREADS="$(nproc)"

CPU_CORES="$(awk '
/^physical id/ { physical[$4] = 1 }
/^core id/ { core[$4] = 1 }
END {
    if (length(physical) && length(core))
        print length(physical) * length(core)
}' /proc/cpuinfo)"

echo "Model: ${CPU_MODEL:-Unknown}"
echo "Threads: $CPU_THREADS"
echo "Cores: ${CPU_CORES:-Unknown}"
echo "GPU:"
lspci | grep -Ei 'VGA compatible controller|3D controller|Display controller' | sed 's/^[^:]*: //'

echo
echo "Memory:"

RAM_TOTAL="$(awk '/^MemTotal:/ {
    printf "%.1f GiB", $2 / 1024 / 1024
}' /proc/meminfo)"

RAM_AVAILABLE="$(awk '/^MemAvailable:/ {
    printf "%.1f GiB", $2 / 1024 / 1024
}' /proc/meminfo)"

echo "RAM: ${RAM_TOTAL:-Unknown} total"
echo "Available: ${RAM_AVAILABLE:-Unknown}"

echo
echo "Storage:"
lsblk -d -o NAME,SIZE,MODEL,TYPE | grep -v '^loop'

echo
echo "Network:"
ip -brief link | grep -v '^lo'

echo
echo "Battery:"
if command -v upower >/dev/null 2>&1; then
    upower -e | grep -E 'battery|DisplayDevice' | while read -r device; do
        echo "$device"
        upower -i "$device" 2>/dev/null | grep -E 'state:|percentage:|energy-full:|energy-full-design:'
    done
else
    echo "upower not available"
fi

echo
echo "================================"
echo "Programix hardware detection 0.1"
echo "================================"