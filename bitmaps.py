class OutOfBounds(Exception):
    "Value you're reading or writing is out of bounds of the bitmap file."
    pass

class BMP:
    def __init__(self, file_name: str):
        self.file_name = file_name

        self.file_width = None
        self.file_height = None
        self.file_contents = None
        self.pixel_data_offset = None

    def read_file(self) -> []:
        with open(self.file_name, 'rb') as f:
            file = f.read()
            f.close()
        return [b'%c' % i for i in file]

    def width(self) -> int:
        # size of 4 bytes
        if self.file_width == None:
            arr = bytearray(b'') 
            for i in range(18, 22):
                arr.extend(self.read_file()[i])
            self.file_width = int.from_bytes(arr, "little")
        return self.file_width

    def height(self) -> int:
        # size of 4 bytes
        if self.file_height == None:
            arr = bytearray(b'') 
            for i in range(22, 26):
                arr.extend(self.read_file()[i])
            self.file_height = int.from_bytes(arr, "little")
        return self.file_height

    def size(self) -> (int, int):
        return self.width(), self.height()

    def pixel_array_offset(self) -> bytearray:
        if self.pixel_data_offset == None:
            # size of 4 bytes
            arr = bytearray(b'') 
            for i in range(10, 14):
                arr.extend(self.read_file()[i])
            self.pixel_data_offset = int.from_bytes(arr, "little")
        return self.pixel_data_offset
i
    def rgb_to_bytearray(self, rgb: []) -> bytearray:
        ba = bytearray()
        for colour in rgb:
            ba.extend((colour).to_bytes(1, byteorder="little"))
        ba.reverse()
        return ba

    def pixel_offset(self, n: int) -> int:
        return self.pixel_array_offset() + 3 * n

    def tuple_check(self, pos: tuple) -> int:
        return len(pos) == 2

    def bounds_check(self, pos: tuple) -> None:
        x, y = pos[0], pos[1]
        if self.file_width == None and self.file_height == None:
            width, height = self.size()
        else:
            width = self.file_width
            height = self.file_height
        if (x >= width or x < 0) or (y >= height or y < 0):
            raise OutOfBounds

    def read_pixel(self, pos: tuple) -> []:
        if not self.tuple_check(pos):
            return
        x, y = pos[0], pos[1]
        self.bounds_check( (x, y) )
        x = (x + (self.width() * y))
        x = self.pixel_offset(x)
        arr = []
        for i in range(x, x+3):
            if self.file_contents != None:
                arr.append(int.from_bytes(self.file_contents[i], "little"))
            else:
                arr.append(int.from_bytes(self.read_file()[i], "little"))
        arr.reverse()
        return arr

    def draw_pixel(self, pos: tuple, rgb: []) -> None:
        # reading and writing too many times to a file causes a permissions err
        # the only chance to fix is to write to the file less frequently.
        if not self.tuple_check(pos):
            return
        rgb = self.rgb_to_bytearray(rgb)
        x, y = pos[0], pos[1]
        self.bounds_check( (x, y) )
        x = (x + self.width() * y)
        x = self.pixel_offset(x)
        with open(self.file_name, "r+b") as f:
            f.seek(x)
            f.write(rgb)
            f.close()
        self.file_contents = self.read_file() 
