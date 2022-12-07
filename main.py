import os, asyncio

from utils import *

ia = AmisInvisible()


async def main():
    friends_dir = "amis_invisibles"
    group_id = None
    file_name = None
    while True:
        clr()
        banner()
        print(lg + '[1] Scrape user in group' + n)
        print(lg + '[2] Make Invisible friends file' + n)
        print(lg + '[3] Send final message' + n)
        print(lg + '[4] Delete invisible friends file' + n)
        print(lg + '[5] Quit')
        a = int(input(f'\nEnter your choice: {r}'))

        match a:
            case 1:
                await case1(ia)
            case 2:
                case2(ia)
            case 3:
                await case3(ia, friends_dir)
            case 4:
                case4(ia, friends_dir)
            case 5:
                clr()
                banner()
                ia.disconnect()
                quit()
            case _:
                print(r + 'You should write a number between 1-5' + n)
                input('\nPress enter to goto main menu')


if __name__ == "__main__":
    with ia.client:
        ia.client.loop.run_until_complete(main())
