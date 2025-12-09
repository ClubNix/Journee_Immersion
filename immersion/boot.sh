#!/bin/bash

# execute the script to start prepare the tp
chmod +x initscript
./initscript $1

# remove unnecessary files
if [[ "$1" == "droite" ]]; then
	rm -rf immersion.rs rustup-init.sh bruteforce_incomplet.py 
	mv immersion Documents/immersion
else
	rm -rf immersion.rs rustup-init.sh immersion 
	mv bruteforce_incomplet.py Documents/bruteforce_incomplet.py

fi


