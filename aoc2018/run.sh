#!/bin/sh
rustc $1.rs -o $i.elf
./$i.elf
