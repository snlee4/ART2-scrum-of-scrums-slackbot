import common.slack as slk
from common.team_names import teams


# # # channel_ids
# # test = C03M2ST52V6
# # prod = C02HDTMC5JR
# Jenkins schedule = 30 8 * * 3


def main():
    print("Beginning Scrum of Scrums")
    channel_id = "C03M2ST52V6"
    slk.post_initial_message(channel_id)
    parent_message_ids = slk.post_parent_message(channel_id, teams)
    slk.threaded_messages(channel_id, parent_message_ids)
    print("Scrum of Scrums Complete")



if __name__ == "__main__":
    main()
    