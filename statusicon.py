import gtk, os

# TODO: this is an ugly hack, get rid of the DATA_DIRECTORY. Maybe we
#       could draw the numbers as text and scale that...
DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')

class StatusIcon(gtk.StatusIcon):
    def set_from_file_with_counter(self, file_name, count):
        renderer = Renderer.get_singleton()
        image = renderer.draw_with_counter(file_name, count)
        self.set_from_pixbuf(image)

def singleton(wrapped):
    @staticmethod
    def get_singleton():
        instance = wrapped()
        wrapped.get_singleton = staticmethod(lambda: instance)
        return instance
    wrapped.get_singleton = get_singleton
    return wrapped

@singleton
class Renderer(object):
    def __init__(self):
        self.image_root_path = DATA_DIRECTORY
        self.image_cache = {}

    def draw_with_counter(self, image_file, number):
        canvas = self.get_image(image_file).copy()
        if number <= 0:
            return canvas

        digits = [self.get_image('%s/%s.png' % (DATA_DIRECTORY, c))
                  for c in str(number)]

        canvas_height = canvas.get_height()
        canvas_width = canvas.get_width()

        number_height = max(map(lambda x: x.get_height(), digits))
        number_width = sum(map(lambda x: x.get_width(), digits))
        h_scale = (2.0 * canvas_height) / (3.0 * number_height)
        w_scale = (2.0 * canvas_width) / (3.0 * number_width)
        scale = min(h_scale, w_scale)

        offset_x = (canvas_width - int(number_width * scale)) / 2
        offset_y = (canvas_height - int(number_height * scale)) / 2
        for digit in digits:
            digit.composite(canvas, 0, 0, canvas_width, canvas_height,
                            offset_x, offset_y, scale, scale,
                            gtk.gdk.INTERP_BILINEAR, 255)
            offset_x += digit.get_width() * scale
        return canvas

    def get_image(self, image_file):
        if image_file not in self.image_cache:
            image = gtk.gdk.pixbuf_new_from_file(image_file)
            self.image_cache[image_file] = image
        return self.image_cache[image_file]
