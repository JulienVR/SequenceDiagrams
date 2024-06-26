import unittest

from src.builder import Builder
from src.parser import Parser


class Test(unittest.TestCase):

    def test1(self):
        builder = Builder("""msc {
          hscale = "2", arcgradient = "20";
        
          a,b,c;
        
          a->c [ label = "ac1()\nac2()\nanother new long line\nand yet another one", textbgcolor = "turquoise"];
          a -> b [ label = "this should be on line X", textbgcolor = "turquoise"],
          b-> c [ label = "this should be on line X as well", textbgcolor = "turquoise"];
          c =>c [ label = "process(1)", textbgcolor = "turquoise"];
          c=>c [ label = "process(2)" ];
          ...;
          c=>c [ label = "ac1()\nac2()\nanother new long line", linecolor="blue", textbgcolor = "turquoise" ];
          c=>c [ label = "process(END)" ];
          a<<=c [ label = "callback()"];
          ---  [ label = "If more to run", ID="*" ];
          a->a [ label = "next()"];
          b<-c [ label = "cb(TRUE)"];
          b->b [ label = "stalled(...)"];
          a<-b [ label = "ab() = FALSE"];
        }""")
        print(builder.parser)
        image = builder.generate()

    def test2(self):
        """
        Vertical step = 28 (arbitrary value) + arcgradient = 36
        """
        builder = Builder("""msc {
        
         # Comment
         arcgradient = "8";
        
         a [label="Client"],b [label="Server"];
        
         a=>b [label="data1"];
         a-xb [label="data2"];
         a=>b [label="data3"];
         a<=b [label="ack1, nack2"];
         a=>b [label="data2", arcskip="1"];
         |||;
         a<=b [label="ack3"];
         |||;
        }""")
        print(builder.parser)
        image = builder.generate()

    def test_drawing_boxes(self):
        builder = Builder("""msc {
           arcgradient = "20";
           fontsize = "15";
           # The entities
           A, B, C, D;
        
           # Small gap before the boxes
           |||;
        
           # Next four on same line due to ','
           A box A [label="box", textbgcolour="turquoise"],
           B rbox B [label="rbox"], C abox C [label="abox"] ,
           D note D [label="note\nline1\nline2"];
        
           # Example of the boxes with filled backgrounds
           A abox B [label="abox", textbgcolour="#ff7f7f"];
           B rbox C [label="rbox", textbgcolour="#7fff7f"];
           C note D [label="note", textbgcolour="#7f7fff"];
        }""")
        print(builder.parser)
        image = builder.generate()

    def test_drawing_boxes_hscale(self):
        builder = Builder("""msc {
           arcgradient = "10";
           hscale = "2";
           # The entities
           A, B, C, D;

           # Small gap before the boxes
           |||;

           # Next four on same line due to ','
           A box A [label="box\nturlututu", textbgcolour="turquoise"],
           B rbox B [label="rbox"], C abox C [label="abox"] ,
           D note D [label="note"];

           # Example of the boxes with filled backgrounds
           A abox B [label="abox", textbgcolour="#ff7f7f"];
           B rbox C [label="rbox", textbgcolour="#7fff7f"];
           C note D [label="note", textbgcolour="#7f7fff"];
        }""")
        print(builder.parser)
        image = builder.generate()

    def test_arc_to_self_and_arcgradient(self):
        builder = Builder("""msc {
        arcgradient = "30";
        # The entities
        A, B;
        
        # Next four on same line due to ','
        A -> B [label = "this is label ppp", linecolor="red", textbgcolour = "grey"];
        B -> A [label = "this is label", linecolor="red"];
        B => B [label = "this is label 1", linecolour="blue", textbgcolor = "turquoise"];
        A => B [label = "this is label 1", linecolour="blue"];
        A >> A [label = "label >>"]; 
        A << B [label = "label >>"]; 
        A =>> B [label = "label =>>", textbgcolour = "turquoise"];
        A :> B [label = "label :>"];
        A <: B [label = "label :> bla bla bla"];
        B <: B [label = "label :> bla bla bla"];
        B -x A [label = "label -x"];
        }
        """)
        print(builder.parser)
        image = builder.generate()

    def test_newline_char(self):
        # TODO: manually draw another text box in the SVG
        builder = Builder("""msc {
        arcgradient = "10";
        a, b;
        a->b [label="this is a line\nand a new line"];
        }""")
        print(builder.parser)
        image = builder.generate()
        
    def test4(self):
        line = ' ... [label = "this is ...", ID="1"], --- [label = "2nd", ID="2"];'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ['... [label = "this is ...", ID="1"]', '--- [label = "2nd", ID="2"]'])

    def test5(self):
        line = ' ...  , --- ;'
        lines = Parser.split_elements_on_line(line)
        self.assertEqual(lines, ['...', '---'])

    def test_arity1_elements(self):
        builder = Builder("""msc {
        arcgradient = "30";
        a, b;
        a->b [label="first arc"];
        ||| [label="extra space", textbgcolor="turquoise"];
        b->a [label="second arc"];
        ... [label="omitted signal", textbgcolor="turquoise"];
        a->b [label="third arc"];
        --- [label="general comment\nwhich is on several lines\nanother one", textbgcolor="turquoise"];
        }""")
        print(builder.parser)
        image = builder.generate()


if __name__ == "__main__":
    unittest.main()
