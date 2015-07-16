#
# BlobEdit - A totally silly application for showing
#  ========   off the GUI framework and providing an example
#             of its use.
#
#  Blobs are red squares that you place on a Blob Document
#  by clicking and move around by dragging. You can save
#  your blob arrangement in a file and load it back later
#  to impress your friends (or send them away screaming).
#
#  News flash: Got a blob you don't want? Now you can
#  get rid of it by shift-clicking it! Isn't that useful!
#

import pickle
from GUI import Application, ScrollableView, Document, Window, Cursor, rgb, Font
from GUI.Files import FileType
from GUI.Geometry import pt_in_rect, offset_rect, rects_intersect
from GUI.StdColors import black, red, clear

GRID_SIZE = 50


class BlobApp(Application):
    def __init__(self, board):
        Application.__init__(self)
        self.blob_type = FileType(name="Blob Document", suffix="blob",
                                  # mac_creator = "BLBE", mac_type = "BLOB", # These are optional
        )
        self.file_type = self.blob_type
        self.blob_cursor = Cursor("C:\\Python27\\lib\\site-packages\\GUI\\Resources\\cursors\\arrow.tiff")
        self.board = board

    def open_app(self):
        self.new_cmd()

    def make_document(self, fileref):
        return BlobDoc(file_type=self.blob_type)

    def make_window(self, document):
        win = Window(size=(1000, 1000), document=document)
        view = BlobView(model=document, extent=(1000, 1000), scrolling='hv',
                        cursor=self.blob_cursor)
        win.place(view, left=0, top=0, right=0, bottom=0, sticky='nsew')
        win.show()
        view.draw_grid(self.board)


class BlobView(ScrollableView):
    # def draw_grid(self, board):
    #     x, y = 0, 0
    #     plopped_regions = []
    #
    #     # self.model.add_blob(Blob(x, y))
    #     for item in board.get_continents():
    #         for territory in item.get_territories():
    #             self.model.add_blob(Blob(x, y, territory=territory.get_name(), continent = item.get_name()))
    #             x = x + GRID_SIZE
    #         x = 0
    #         y = y + GRID_SIZE

    def draw_grid(self, board):
        x, y = 100, 200
        sx, sy = 100, 100
        plopped_regions = []

        def find_pos(x, y):
            for nx in range(-1, 2):
                for ny in range(-1, 2):
                    if not self.model.find_blob(nx * GRID_SIZE + x, ny * GRID_SIZE + y):
                        point = (nx * GRID_SIZE + x, ny * GRID_SIZE + y)
                        return point
            else:
                raise RuntimeError('raaape')

        # self.model.add_blob(Blob(x, y))
        for continent in board.get_continents():
            for territory in continent.get_territories():
                if territory.get_name() not in plopped_regions:
                    pos = find_pos(x, y)
                    x = pos[0]
                    y = pos[1]
                    self.model.add_blob(Blob(x, y, territory.get_name(), territory.get_active_soldiers(), territory.get_continent()))
                    plopped_regions.append(territory.get_name())
                for connection in territory.get_connections():
                    if connection.get_name() not in plopped_regions and connection.get_continent() == continent.get_name():
                        pos = find_pos(x, y)
                        plopped_regions.append(connection.get_name())
                        self.model.add_blob(
                            Blob(pos[0], pos[1], connection.get_name(), connection.get_active_soldiers(), connection.get_continent()))
                x = pos[0]
                y = pos[1]
            x += GRID_SIZE * 7
            y = sy + GRID_SIZE * 2

        lista = []
        settet = set()
        for blob in self.model.blobs:
            lista.append(blob.get_territory())
            settet.add(blob.get_territory())
        print "Antal territorier utritade: " + str(len(lista))
        print "Antal unika territorier utritade: " + str(len([i for i in settet]))

    def draw(self, canvas, update_rect):
        canvas.erase_rect(update_rect)
        canvas.fillcolor = clear
        canvas.pencolor = black
        for blob in self.model.blobs:
            if blob.intersects(update_rect):
                blob.draw(canvas)

    def mouse_down(self, event):
        x, y = event.position
        blob = self.model.find_blob(x, y)
        if blob:
            print "Territory: " + blob.get_territory() + " in continent: " + blob.get_continent()

    def drag_blob(self, blob, x0, y0):
        for event in self.track_mouse():
            x, y = event.position
            self.model.move_blob(blob, x - x0, y - y0)
            x0 = x
            y0 = y

    def blob_changed(self, model, blob):
        self.invalidate_rect(blob.rect)


class BlobDoc(Document):
    blobs = None

    def new_contents(self):
        self.blobs = []

    def read_contents(self, file):
        self.blobs = pickle.load(file)

    def write_contents(self, file):
        pickle.dump(self.blobs, file)

    def add_blob(self, blob):
        self.blobs.append(blob)
        self.changed()
        self.notify_views('blob_changed', blob)

    def find_blob(self, x, y):
        for blob in self.blobs:
            if blob.contains(x, y):
                return blob
        return None

    def move_blob(self, blob, dx, dy):
        self.notify_views('blob_changed', blob)
        blob.move(dx, dy)
        self.changed()
        self.notify_views('blob_changed', blob)

    def delete_blob(self, blob):
        self.notify_views('blob_changed', blob)
        self.blobs.remove(blob)
        self.changed()


class Blob:
    def __init__(self, x, y, territory, soldiers,continent):
        self.rect = (x, y, x + GRID_SIZE, y + GRID_SIZE)
        self.territory = territory
        self.start_soldiers = soldiers
        self.continent = continent

    def contains(self, x, y):
        return pt_in_rect((x, y), self.rect)

    def intersects(self, rect):
        return rects_intersect(rect, self.rect)

    def move(self, dx, dy):
        self.rect = offset_rect(self.rect, (dx, dy))

    def draw(self, canvas):
        canvas.moveto(self.rect[0] + 2, self.rect[1] + 14)
        font_size = 12
        f = Font("Times", font_size, [])
        canvas.font = f
        st = self.territory.split('_')
        ny = self.rect[1] + 14
        for word in st:
            canvas.show_text(word)
            ny += font_size
            canvas.moveto(self.rect[0] + 2, ny)
        canvas.moveto(self.rect[0] + (GRID_SIZE - 10 * len(self.start_soldiers)), self.rect[1] + (GRID_SIZE - 3))
        canvas.show_text(self.start_soldiers)
        canvas.fill_frame_rect(self.rect)

    def get_territory(self):
        return self.territory

    def get_start_soldiers(self):
        return self.start_soldiers

    def get_continent(self):
        return self.continent

# BlobApp().run()
