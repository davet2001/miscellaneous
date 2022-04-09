"""
Python application to generate esphome energine rf transmitter configs.
Dave T 09/04/2022

Home Assistant no longer supports my 433 gpio rf transmitter wired directly
top my raspberry Pi.

So I configured an esp32 WT32-ETH01 running esphome with a new £2 RF
transmitter to send RF codes to my energenie sockets.

But the yaml to configure this is quite complex, so the helper script below
generates a config to turn on/off each of 4 sockets associated with a 
housecode.

The generation of the code is similar to energenie_rpi-rf_433.sh in this
repository, except this time esphome wants it as binary, and we have
to workaround the fact that it insists on sending a sync bit prefix
even though the energenie scheme doesn't need one.

Thanks again to the awesome universal radio hacker and a £5 DVB USB dongle
which really helped with checking the codes being generated compared with
the original handheld remote.
""" 

def reverse_string(input:str) -> str:
    return input[::-1]

def inverse_binary_string(input:str) -> str:
    return ''.join(['1' if i == '0' else '0' for i in input])

def gen_binary_code(housecode:int, button:int, newstate:bool) -> str:

    housecode_bin = f"{housecode:>020b}"
    button_bin = reverse_string(inverse_binary_string(f"{(button - 1):>03b}"))
    newstate_bin = '1' if newstate else '0'
    return(f"{housecode_bin}{button_bin}{newstate_bin}0")

def gen_action_yaml(housecode:int, button:int, newstate:bool) -> str:
    code = gen_binary_code(housecode, button, newstate)
    # esphome doesn't seem to handle 'no sync pattern'.
    # so we drop the first bit and turn it into the sync pattern.
    if code[:1] == "0":
        sync_pattern = "[1,3]"
    else:
        sync_pattern = "[3,1]"
    code_without_first_bit = code[1:]
    output = ""
    output += f"    turn_{'on' if newstate else 'off'}_action:\n"
    output += f"      - remote_transmitter.transmit_rc_switch_raw:\n"
    output += f"          code: '{code_without_first_bit}'\n"
    output += f"          protocol:\n"
    output += f"            pulse_length: 200\n"
    output += f"            sync: {sync_pattern}\n"
    output += f"          repeat: 5"
    return output

def gen_switch_yaml(housecode:int, button:int) -> str:
    output = ""
    output += f"  - platform: template\n"
    output += f"    name: 'Energenie Socket 0x{housecode:05x}_{button}'\n"
    output += f"    optimistic: true\n"
    output += f"{gen_action_yaml(housecode, button, True)}\n"
    output += f"{gen_action_yaml(housecode, button, False)}"
    return output


if __name__ == "__main__":
    print("switch:")
    for housecode in [0xfd160, 0x59a28]:
        for i in range(1,5):
            print(gen_switch_yaml(housecode, i))
