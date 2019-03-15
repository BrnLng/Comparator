import os
from Configs.config import file_ending


class FileDB:

    def set_current_list(self, current_list_file):
        items = []
        try:
            with open(current_list_file + file_ending.RAW, 'r', encoding='utf-8') as f:
                for item in f.readlines():
                    items.append(item.rstrip('\n'))
                f.close()
            #                         {''} == set([''])
            items = list(set(items) - {''})  # normalizing list by first cleaning new lines with set functionality

            # check if initial backup exists, then create one if not and leave it untouched ever after
            if not os.access(current_list_file + file_ending.RAWB, os.R_OK):
                try:
                    with open(current_list_file + file_ending.RAWB, 'w', encoding='utf-8') as fbkp:
                        output = "\n".join(items)
                        fbkp.write(output)
                except IOError as e:
                    print(e)

            return items

        except IOError as e:
            print(e)  # TODO: totally new run: create list or batch read, move file etc.

    def _is_new_list(self, current_ordered_list, current_list_file):
        if len(current_ordered_list) > 0:
            return False
        try:
            with open(current_list_file + file_ending.ORD, 'r', encoding='utf-8') as f:
                if f.seek(4):
                    return True
                f.close()
            return False
        except (IOError, EOFError) as e:
            # print(e)  # list will be created elsewhere
            return True
