from colorama import init, Fore
import pyfiglet
import os, random
from amis_invisbles import AmisInvisible

init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]


def banner():
    f = pyfiglet.Figlet(font='slant')
    banner_text = f.renderText('Invisible Friends')
    print(f'{random.choice(colors)}{banner_text}{n}')
    print(r + '  Version: 1.0 | Author: freddy' + n + '\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_color():
    return random.choice(colors)


def get_header(text):
    color = get_color()
    clr()
    print(color + f"\n---------------------{text}-------------------------")
    return color


async def case1(ia: AmisInvisible):
    groups = await ia.get_groups_id()
    color = get_header("Group list")
    for index, (name, id) in enumerate(groups):
        print(color + f"[{index}]" + name)
    b = int(input(f'\nEnter your choice: {r}'))
    group_id = groups[b][1] if 0 <= b < len(groups) else None
    if group_id:
        file_name = os.path.join("members", groups[b][0] + ".csv")
        await ia.scrap_members(group_id=group_id)
        print(color + "You have selected {} Thanks!".format(groups[b][0]))
    else:
        print(r + "Can't handle your choice")
    input('\nPress enter to goto main menu')


def case4(ia: AmisInvisible, friends_dir: str):
    color = get_header("Files list")
    files = os.listdir(friends_dir)

    for index, f in enumerate(files):
        name = f.split(".")[0]
        print(color + f" [{index}] {name} ")

    if len(files) == 0:
        print(r + "There is no file to deleted")
    else:
        b = str(input(f'\nEnter your choice: {r}'))
        for p in b.split():
            p = int(p)
            file_name = os.path.join(friends_dir, files[p]) if 0 <= p < len(files) else None
            if file_name:
                os.remove(file_name)
                print(r + " {} has been deleted".format(file_name))
    input('\nPress enter to goto main menu')


def case2(ia: AmisInvisible):
    color = get_header("Members list")
    files = os.listdir("members")

    for index, f in enumerate(files):
        name = f.split(".")[0]
        print(color + f" [{index}] {name} ")

    if len(files) == 0:
        print(r + "Please Scrape Members in option [1] because making invisible friends")
    else:
        b = int(input(f'\nEnter your choice: {r}'))
        file_name = os.path.join("members", files[b]) if 0 <= b < len(files) else None
        print(color + "You have selected {} Thanks!".format(file_name))
        if file_name:
            b = str(input(f'\nGive a file name: {r}'))
            ia.make_friends(src_file_name=file_name, targ_name=b)
        else:
            print(r + "Can't handle your choice")
    input('\nPress enter to goto main menu')


async def case3(ia: AmisInvisible, friends_dir: str):
    files = os.listdir(friends_dir)
    color = get_header("Sending options")
    print(color + '[1] Merge files in one' + n)
    print(color + '[2] Send message to members' + n)
    print(color + '[3] Send final to someone' + n)
    b = int(input(f'\nEnter your choice: {r}'))
    match b:
        case 1:
            color = get_header("Select file to merge")

            if len(files) < 2:
                print(r + "There is no file to merge")
            else:
                for index, f in enumerate(files):
                    name = f.split(".")[0]
                    print(color + f" [{index}] {name} ")
                b = str(input(f'\nEnter your choice: {r}'))
                file_path = []
                for p in b.split():
                    p = int(p)
                    file_name = os.path.join(friends_dir, files[p]) if 0 <= p < len(files) else None
                    if file_name:
                        file_path.append(file_name)
                ia.merge_files(file_path)
        case 2:
            color = get_header("Select source file with invisible friends")
            for index, f in enumerate(files):
                name = f.split(".")[0]
                print(color + f" [{index}] {name} ")
            b = int(input(f'\nEnter your choice: {r}'))

            file_name = os.path.join(friends_dir, files[b]) if 0 <= b < len(files) else None
            if file_name:
                await ia.send_message(file_name)
        case 3:
            color = get_header("Send final invisible file to someone")
            b = str(input(f'\nEnter the phone numbers: {r}'))
            phones = [n for n in b.split()]

            await ia.send_final_file(phones=phones)

    input('\nPress enter to goto main menu')
