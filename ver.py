import argparse
import secrets
import string

def gen_key(file, ktype, keyfile="vlk.key"):
    """
    Generate a Version Lock Key (VLK) in the form of randomart for the specified file

    VLKs are used to lock a file to a specific version of a program. The key is generated completely randomly and is stored in a file.

    This is simular to the SSH keys, but for a file.

    :param keyfile:
    :param file:
    :param ktype:
    :return:
    """
    if keyfile == "vlk.key":
        keyfile = f"{file}.key"


    spacing = len(f" {ktype}: ")

    if ktype == '95':
        keylist = [secrets.randbits(95) for _ in range(1)]
    else:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        keylist = [''.join(secrets.choice(alphabet) for _ in range(128)) for _ in range(1)]

    def split_string_randomly(s, length):
        length -= 4
        pieces = []
        while len(s) > 1:
            # Randomly choose the number of characters to split (between 1 and min(10, len(s)))
            split_length = secrets.choice(range(1, min(10, len(s))))
            key_spacing = length - split_length - secrets.randbelow(length + 1) # 20 minus the length of the split key (10 > split_length > 0) minus a random number between 0 and 20
            pieces.append(f"{" " * key_spacing}{s[:split_length]}{" " * (length - len(" " * key_spacing + s[:split_length]))}")
            # print(f"{" " * key_spacing}{s[:split_length]}{" " * (length - len(" " * key_spacing + s[:split_length]))}")
            # print("Hm: ", f"{len(f"{" " * key_spacing}{s[:split_length]}{" " * (length - len(" " * key_spacing + s[:split_length]))}")}")
            s = s[split_length:]
        if s:
            pieces.append(s)
        return pieces

    keylist = list(split_string_randomly(str(keylist[0]), len(f"┌ {'─' * 10} [ {ktype} ] {'─' * 10} ┐")))
    del keylist[-1]
    # print("this: ", keylist)

    keylength = len(str(keylist[0]))

    # print(keylength)

    print(f"┌ {'─' * 10} [ {ktype} ] {'─' * 10} ┐")
    with open(keyfile, 'w') as f:
        for key in keylist:
            f.write(f"{key}{' ' * (20 - len(key))}")

            print(f"│ {key}{' ' * (20 - len(key))} │")
    print(f"└ {'─' * 10}{'═' * (keylength - 20)}{'─' * 10} ┘")


def info(file):
    """
    Show information about the file

    :param file:
    :return:
    """

def save(file, version, description=None):
    """
    Save information about the file

    :param description:
    :param version:
    :param file:
    :return:
    """
    with open(f"{file}.info", 'w') as f:
        f.write(f"{version}\n"
                f"{description}\n")

def main():
    parser = argparse.ArgumentParser(description='ver 1.0')

    parser.add_argument("file", nargs="?", help="file to read")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-s', '--save', action='store_true', help='save the file info')
    parser.add_argument('-i', '--info', action='store_true', help='show stored info on file')
    parser.add_argument('--description', help='description of the file')
    parser.add_argument('-k', '--key', action='store_true', help='Generate a VLK (Version Lock Key) for the file')
    parser.add_argument('-t', '--type', help='Specify the type for the key generation')

    args = parser.parse_args()

    if args.key:
        if args.file and args.type:
            if args.type in ['vlk', '95']:
                gen_key(args.file, args.type)
            else:
                print('Error: Invalid key type')
        else:
            print('Error: Both file and type must be specified for key generation')
    elif args.file:
        print(f"Reading file: {args.file}")

    elif args.info:
        info(args.file)

    elif args.save:
        if args.file and args.version:
            if args.description:
                print(f"Saving file: {args.file} with version {args.version} and description {args.description}")
                save(args.file, args.version, args.description)
            else:
                print(f"Saving file: {args.file} with version {args.version}")
                save(args.file, args.version)
        else:
            print('Error: Both file and version must be specified for saving')

    else:
        print('No action specified')

if __name__ == "__main__":
    main()