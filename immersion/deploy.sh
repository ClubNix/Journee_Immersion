#!/bin/bash

for pc in {1..36};
do
  sshpass -p "kali" scp -o ConnectTimeout=30 -o StrictHostKeyChecking=no ./boot.sh kali@pc5004-"$pc":~/
  sshpass -p "kali" scp -o ConnectTimeout=30 -o StrictHostKeyChecking=no ./initscript kali@pc5004-"$pc":~/
  if [ $(($pc % 2)) -eq 0 ]; then
    sshpass -p "kali" ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no kali@pc5004-"$pc" "chmod +x ./boot.sh && ./boot.sh droite && rm boot.sh initscript" &
  else
    sshpass -p "kali" ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no kali@pc5004-"$pc" "chmod +x ./boot.sh && ./boot.sh gauche && rm boot.sh initscript" &
  fi
done
