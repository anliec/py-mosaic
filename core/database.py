import sqlite3 as lite
from core import PhotosManaging
from PIL import ExifTags


class DataBase:
    con = None

    def create_photo_table(self):
        cur = self.con.cursor()
        create_table_request = "CREATE TABLE photos( id INTEGER primary key, path VARCHAR UNIQUE"
        # generate a column for every color of every 6x4 pixels
        for x in range(1, 7):
            for y in range(1, 5):
                for c in ["R", "G", "B"]:
                    create_table_request += ", px" + str(x) + "x" + str(y) + c + " TINYINT"
        # close request
        create_table_request += ");"
        # execute request
        cur.execute(create_table_request)
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
        return

    def commit(self):
        self.con.commit()
        return

    def add_photo(self, picture_path):
        """add the given picture to DB if the image as the good ratio (3:2)"""
        cur = self.con.cursor()
        image = PhotosManaging.image_from_path(picture_path)
        # check Exif information for rotation
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation': break
            exif = dict(image._getexif().items())
            # if the image is upside down, rotate it's just +/-90° rotation return
            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                return
            elif exif[orientation] == 8:
                return
        except:
            # exception raised if the picture is not jpeg or has no exif data.
            pass
        size = image.size
        # take image ratio from 1:1 to 2:1
        if (size[0] // size[1]) != 1:
            # if image ration is not good skip the image
            print(picture_path + " don't have the good ratio: " + str(size[0]) + ":" + str(size[1]))
            return
        pixels = PhotosManaging.pixelize(PhotosManaging.miniaturize(image))
        data = (picture_path,)
        request = "INSERT OR IGNORE INTO photos (path"
        request_value = " VALUES (?"
        for x in range(1, 7):
            for y in range(1, 5):
                for c in [("R", 0), ("G", 1), ("B", 2)]:
                    # add the current color to the data tuple
                    data += (pixels[(y-1)*6+x-1][c[1]],)
                    # add the current color to the request
                    request += ", px" + str(x) + "x" + str(y) + c[0]
                    # and add a value field at the end of the request
                    request_value += ",?"
        # finish the request generation
        request += ")" + request_value + ")"
        # execute request
        cur.execute(request, data)
        return

    def get_bests_candidates(self, target_pixels):
        # change here to use other computation method for error
        # available are: 'SE' (Squared Error), 'E' (Error)
        error_compute = "SE"
        result_list = []
        px = target_pixels
        request = 'SELECT path, '
        for i in range(0, 6):
            for j in range(0, 4):
                for c in [('R', 0), ('G', 1), ('B', 2)]:
                    if error_compute is "SE":
                        # compute the difference on the given pixel
                        diff = '(px' + str(i+1) + 'x' + str(j+1) + c[0] + '-' + str(px[i+6*j][c[1]]) + ') '
                        # square this difference
                        request += diff + '* ' + diff
                    else:
                        request += 'abs(px' + str(i+1) + 'x' + str(j+1) + c[0] + '-' + str(px[i+6*j][c[1]]) + ') '
                    if i != 5 or j != 3 or c[1] != 2:
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
        for (path, score) in rows:
            result_list.append((score, path))
        # sort the list by score ascending (may be use less as ordered by SQL)
        result_list.sort(key=lambda tup: tup[0])
        return result_list
