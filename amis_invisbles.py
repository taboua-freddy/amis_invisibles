from telethon import TelegramClient
import os, csv
from time import sleep
from dotenv import load_dotenv
import pandas as pd
from telethon.tl.types import Channel, User

load_dotenv()


class AmisInvisible:
    message = "Bienvenue {} 🤗 à la 3è Edition de Noel en Famille💐🥳.\n\nPour cette année tu devras préparer le " \
              "cadeau🎁 de {} que lui remettra le 25 Décembre.\nTu recevras sa photo d’ici peu.\nIl est bon de ne pas " \
              "offrir un cadeau consommable(Chocolat…) et quel que soit le prix de le garder anonyme😉.\n\nSois " \
              "bénis🙏🏽.\n\nNB: Ceci est un message automatique prière de ne pas répondre. "

    friends_dir = "amis_invisibles"
    members_dir = "members"
    final_file = os.path.join(friends_dir, "final.csv")
    
    if not os.path.exists(friends_dir):
        os.mkdir(friends_dir)
    if not os.path.exists(members_dir):
        os.mkdir(members_dir)

    def __init__(self) -> None:
        api_id = int(os.environ.get("api_id"))
        api_hash = os.environ.get("api_hash")
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.client.start()

    @classmethod
    def _save_final(cls, friends: pd.DataFrame):
        if os.path.exists(cls.final_file):
            df = pd.read_csv(cls.final_file)
            friends = pd.concat([df, friends], axis=0)

        friends.to_csv(cls.final_file, index=False)

    async def scrap_members(self, group_id=-1001275710507):
        group: Channel = await self.client.get_entity(group_id)
        members: list[User] = await self.client.get_participants(group)

        file_name = os.path.join(self.members_dir, group.title + ".csv")
        with open(f"{file_name}", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', "full name", 'user id', "phone number"])
            for member in members:
                if not member.bot:
                    username = member.username if member.username else ""
                    first_name = member.first_name if member.first_name else ""
                    last_name = member.last_name if member.last_name else ""
                    phone_number = "+" + str(member.phone) if member.phone else ""
                    writer.writerow([username, first_name + " " + last_name, member.id, phone_number])

    def make_friends(self, src_file_name: str, targ_name: str):
        """
        Create invisible friends and Merge the given csv file with the final csv file
        :param targ_name:
        :param src_file_name:
        :return: shuffled dataframe
        """
        targ_name = os.path.join(self.friends_dir, targ_name + ".csv")
        df = pd.read_csv(src_file_name) \
            .drop(["username", "phone number"], axis=1) \
            .rename(columns={"full name": "sender"})
        shuffled_df = df.sample(frac=1) \
            .reset_index(drop=True) \
            .drop(["user id"], axis=1) \
            .rename(columns={"sender": "receiver"})
        pd.concat([df, shuffled_df], axis=1).to_csv(targ_name, index=False)

    def merge_files(self, file_path: list[str]):
        dfs = [pd.read_csv(p) for p in file_path]
        if len(dfs) > 0:
            friends = pd.concat(dfs, axis=0)
            self._save_final(friends)

    async def send_message(self, file_name):
        df = pd.read_csv(file_name)
        count = len(df)
        for index, row in df.iterrows():
            print(f"{index}/{count}")
            sleep(1)
            sender_id = row["user id"]
            sender_name = row["sender"]
            receiver_name = row["receiver"]
            await self.client.send_message(sender_id, self.message.format(sender_name, receiver_name))
            print(f"\n Sent to {sender_name}")

        print("\nAll messages have been sent")

    async def send_final_file(self, phones: list[str], file_name: str = None):
        if file_name is None:
            file_name = self.final_file
        if not os.path.exists(file_name):
            return
        count = len(phones)
        for index, phone in enumerate(phones, 1):
            print(f"\n{index}/{count}")
            sleep(1)
            await self.client.send_file(phone, file_name)

            print(f"Sent to {phone}")

        print("\nFinal file has been sent")

    async def get_groups_id(self):
        return [(dialog.name, dialog.id) async for dialog in self.client.iter_dialogs() if dialog.is_channel]

    def disconnect(self):
        self.client.disconnect()
