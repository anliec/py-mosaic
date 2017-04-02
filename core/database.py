import sqlite3 as lite
from core import PhotosManaging


class DataBase:
    con = None

    def create_photo_table(self):
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE photos( id INTEGER primary key,
                                            path VARCHAR UNIQUE,
                                            px1x1R TINYINT,
                                            px1x1G TINYINT,
                                            px1x1B TINYINT,
                                            px2x1R TINYINT,
                                            px2x1G TINYINT,
                                            px2x1B TINYINT,
                                            px3x1R TINYINT,
                                            px3x1G TINYINT,
                                            px3x1B TINYINT,
                                            px1x2R TINYINT,
                                            px1x2G TINYINT,
                                            px1x2B TINYINT,
                                            px2x2R TINYINT,
                                            px2x2G TINYINT,
                                            px2x2B TINYINT,
                                            px3x2R TINYINT,
                                            px3x2G TINYINT,
                                            px3x2B TINYINT
                                            );''')
        return

    def get_number_of_photo(self):
        cur = self.con.cursor()
        cur.execute('''SELECT COUNT(*) FROM photos''')
        return int(cur.fetchone()[0])

    def __init__(self):
        self.con = lite.connect('photos.db')
        cur = self.con.cursor()
        if ("photos", ) in cur.execute("select name from sqlite_master where type = 'table';"):
            pass
        else:
            self.create_photo_table()
            self.con.commit()

    def close(self):
        self.commit()
        self.con.close()

    def commit(self):
        self.con.commit()

    def add_photo(self, picture_path):
        """add the given picture to DB if the image as the good ratio (3:2)"""
        cur = self.con.cursor()
        image = PhotosManaging.image_from_path(picture_path)
        size = image.size
        # take image ratio from 1:1 to 2:1
        if (size[0] // size[1]) != 1:
            # if image ration is not good skip the image
            print(picture_path + " was not the good ration: " + str(size[0]) + ":" + str(size[1]))
            return
        pixels = PhotosManaging.pixelize(PhotosManaging.miniaturize(image))
        data = (picture_path, pixels[0][0], pixels[0][1], pixels[0][2],
                    pixels[1][0], pixels[1][1], pixels[1][2],
                    pixels[2][0], pixels[2][1], pixels[2][2],
                    pixels[3][0], pixels[3][1], pixels[3][2],
                    pixels[4][0], pixels[4][1], pixels[4][2],
                    pixels[5][0], pixels[5][1], pixels[5][2])
        request = '''INSERT OR IGNORE INTO photos (
                    path,px1x1R,px1x1G,px1x1B,
                    px2x1R,px2x1G,px2x1B,
                    px3x1R,px3x1G,px3x1B,
                    px1x2R,px1x2G,px1x2B,
                    px2x2R,px2x2G,px2x2B,
                    px3x2R,px3x2G,px3x2B
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur.execute(request, data)

    def get_bests_candidates(self, target_pixels):
        result_list = []
        px = target_pixels
        request = 'SELECT path, '
        for i in range(0, 3):
            for j in range(0, 2):
                for c in [('R', 0), ('G', 1), ('B', 2)]:
                    request += 'abs(px' + str(i+1) + 'x' + str(j+1) + c[0] + '-' + str(px[i+3*j][c[1]]) + ') '
                    if i != 2 or j != 1 or c[1] != 2:
                        request += '+ '
        request += 'as score '
        request += 'FROM photos '
        request += 'ORDER BY score ASC '
        request += 'LIMIT 0, 20 '
        # execute the request
        cur = self.con.cursor()
        cur.execute(request)
        rows = cur.fetchall()
        # copy the result into a list of tuples
        for (path,score) in rows:
            result_list.append((score, path))
        # sort the list by score ascending (may be use less as ordered by SQL)
        result_list.sort(key=lambda tup: tup[0])
        return result_list
