import VM  # import the module
import multiprocessing

def parse_code(code: str) -> bytes:
    # This just converts the prettified code below to the raw, ugly bytecode. You can ignore this function.
    import re
    
    binary = ''
    regex = re.compile(r"[0-9a-f]+:\s+([^;]+)\s*;.*", re.DOTALL)

    for i, line in enumerate(code.strip().splitlines(keepends=False)):
        if line.startswith(';'):
            continue
        match = regex.match(line)
        assert match is not None, f"Could not parse code (line {i})"
        
        binary += match.group(1)

    return bytes.fromhex(binary)


if __name__ == "__main__":
    # This is the bytecode we'll run
    code = """
;                           section .text
;                           _start:
0:  b8 04 00 00 00          ;mov    eax,0x4   ; SYS_WRITE
5:  bb 01 00 00 00          ;mov    ebx,0x1   ; STDOUT
a:  b9 29 00 00 00          ;mov    ecx,0x29  ; address of the message
f:  ba 0e 00 00 00          ;mov    edx,0xe   ; length of the message
14: cd 80                   ;int    0x80      ; interrupt kernel
16: e9 02 00 00 00          ;jmp    0x1d      ; _exit
1b: 89 c8                   ;mov    eax,ecx   ; this is here to mess things up if JMP doesn't work
;                           _exit:
1d: b8 01 00 00 00          ;mov    eax,0x1   ; SYS_EXIT
22: bb 00 00 00 00          ;mov    ebx,0x0   ; EXIT_SUCCESS
27: cd 80                   ;int    0x80      ; interrupt kernel
; section .data
29: 48 65 6C 6C 6F 2C 20 77 6F 72 6C 64 21 0A ; "Hello, world!",10
             """

    vm = VM.VMKernel(500)  # Initialize the VM with the Linux kernel and give it 500 bytes of memory.

    # EXECUTE IT!
    vm.execute(
        VM.ExecutionStrategy.BYTES,  # We're executing raw bytecode
        parse_code(code)  # This is the actual bytecode
    )
def calculate_square(numbers, result, square_sum):
    """Function to calculate square of numbers."""
    for idx, number in enumerate(numbers):
        result[idx] = number * number
    square_sum.value = sum(result)

if __name__ == '__main__':
    numbers = range(10)
    result = multiprocessing.Array('i', 10)
    square_sum = multiprocessing.Value('i')

    # Process initialization
    process = multiprocessing.Process(target=calculate_square, args=(numbers, result, square_sum))

    # Start and join the process
    process.start()
    process.join()

    print(f"Squares: {list(result)}")
    print(f"Sum of squares: {square_sum.value}")
