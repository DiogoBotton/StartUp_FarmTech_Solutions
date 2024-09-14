class Terrain:
    def __init__(self, product_code, width, length, space_line, street_width):
        self.product_code = product_code
        self.width = width
        self.length = length
        self.space_line = space_line
        self.street_width = street_width
        self.total_area = 0
        self.usable_area = 0
        self.line_number = 0
        self.street_number = 0
        self.nitrogen_fertilizer = 0
        self.quantity_seeds = 0

    def EditTerrainDetail(self, total_area, usable_area, line_number, street_number, nitrogen_fertilizer, quantity_seeds):
        self.total_area = total_area
        self.usable_area = usable_area
        self.line_number = line_number
        self.street_number = street_number
        self.nitrogen_fertilizer = nitrogen_fertilizer
        self.quantity_seeds = quantity_seeds