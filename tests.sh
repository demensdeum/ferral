mkdir output
python ferral.py tests/0_hello_world/hello_world.ferl "C" output/hello_world.c
python ferral.py tests/0_hello_world/hello_world.ferl "Python" output/hello_world.py
python ferral.py tests/0_hello_world/hello_world.ferl "Node js" output/hello_world.js
python ferral.py tests/0_hello_world/hello_world.ferl "x86_64 syscall nasm" output/hello_world.asm
python ferral.py tests/0_hello_world/hello_world.ferl "PHP" output/hello_world.php
python ferral.py tests/0_hello_world/hello_world.ferl "Rust" output/hello_world.rst
python ferral.py tests/0_hello_world/hello_world.ferl "C Plus Plus" output/hello_world.cpp
