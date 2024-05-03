import xml.etree.ElementTree as ET

import src.utils as utils


class Arity2:
    def __init__(self, src, dst, element, options):
        self.src = src
        self.dst = dst
        self.element = element
        self.options = options


class Arc(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('->', '=>', '>>', '=>>', ':>', '-x'), f"Unsupported type: {element}"
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Arc> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element):
        # Participant's line
        utils.expand_lifelines(builder, root, self.options)
        # Arc
        y1 = builder.current_height + builder.vertical_step / 2
        x1 = builder.participants_coordinates[self.src]
        x2 = builder.participants_coordinates[self.dst]
        y2 = y1 + builder.parser.context['arcgradient']
        if self.src == self.dst:
            # Special case: curved arc
            ET.SubElement(root, 'path', {
                **self.options,
                'stroke': 'black',
                'd': f"M {x1} {y1} A200,15 0 0,1 {x1},{y1 + builder.vertical_step}",
                'fill': 'none',
            })
            builder.current_height += builder.vertical_step
            utils.expand_lifelines(builder, root, self.options)
        else:
            # Class line arc
            ET.SubElement(root, 'line', {
                **self.options,
                'stroke': 'black',
                'x1': str(x1),
                'y1': str(y1),
                'x2': str(x2),
                'y2': str(y2),
            })
        # Label
        label = self.options.get('label')
        if label:
            g = ET.Element('g')
            x_mean = (x1 + x2)/2
            y_mean = (y1 + y2)/2
            # ET.SubElement(g, 'rect', {
            #     # upper left corner coordinates
            #     'x': str(x_mean),
            #     'y': str(y_mean),
            #     # length and height of the rectangle
            #     'width': '40',
            #     'height': '20',
            #     'fill': 'grey',
            # })  # TODO: draw rectangle behind the text elements
            text = ET.SubElement(g, 'text',  {
                'x': str(x1 + 5) if self.src == self.dst else str(x_mean),
                'y': str(y_mean - 5),
                'text-anchor': 'middle' if self.src != self.dst else '',  # the text will be centered around the given coordinates
            })
            text.text = label
            root.append(g)
        # Triangle
        if self.src == self.dst:
            y2 += builder.vertical_step
        y1, y3 = y2 + 6, y2 - 6
        if x1 < x2:
            x1 = x3 = x2 - 10
        else:
            x1 = x3 = x2 + 10
        ET.SubElement(root, 'polygon', {
            'fill': 'black',
            'points': f"{x1},{y1} {x2},{y2} {x3},{y3}",
        })
        # Increase height pointer
        builder.current_height += builder.vertical_step


class Box(Arity2):
    def __init__(self, src, dst, element, options):
        assert element in ('box', 'rbox', 'abox', 'note')
        super().__init__(src, dst, element, options)

    def __repr__(self):
        return f"<Box> {self.src}{self.element}{self.dst} {self.options}"

    def draw(self, builder, root: ET.Element, extra_options: dict = False):
        pass
