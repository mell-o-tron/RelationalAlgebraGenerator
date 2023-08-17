import sys

from lark import Lark
from lark import UnexpectedEOF
from lark import UnexpectedInput

from lark import lexer

def parse_program (program):
    #print(program)
    f = open("pg.lark", "r")

    l = Lark(f.read())

    try:
        parsed = l.parse(program)
    except Exception as u:
        if type (u) == UnexpectedEOF or type (u) == UnexpectedInput:
            print("Parser Error")
            print(u.get_context(program))
            print(u)
        else:
            print(u)
        exit(1)



    return parsed

def get_nodes(syntax_tree, nodes, edges, node_name, ypos, xpos, width):
    if type(syntax_tree) != lexer.Token: # check if not terminal

        if syntax_tree.data in ["expr", "start"]:
            for c in syntax_tree.children:
                get_nodes(c, nodes, edges, node_name, ypos, xpos, width)
        elif syntax_tree.data == "project":
            kidz = syntax_tree.children

            attributes = kidz[2].children           # bypass attrs_or_funs
            attr_str = ""
            for a in attributes:
                attr_str +=  str(a) + ","
            attr_str = attr_str[:len(attr_str) - 1]
            # add project
            nodes.append ((node_name, "$\\pi_{" + attr_str + "}$", ypos, xpos))
            # add the edge leading to the child
            edges.append((node_name, node_name + "0"))

            get_nodes(kidz[1], nodes, edges, node_name + "0", ypos - 1, xpos, width)

        elif syntax_tree.data == "order_by":
            kidz = syntax_tree.children

            attributes = kidz[2].children           # bypass attrs_or_funs
            attr_str = ""
            for a in attributes:
                attr_str +=  str(a) + ","
            attr_str = attr_str[:len(attr_str) - 1]
            # add project
            nodes.append ((node_name, "$\\tau_{" + attr_str + "}$", ypos, xpos))
            # add the edge leading to the child
            edges.append((node_name, node_name + "0"))

            get_nodes(kidz[1], nodes, edges, node_name + "0", ypos - 1, xpos, width)

        elif syntax_tree.data == "filter":
            kidz = syntax_tree.children
            cond = kidz[2]

            # add filter
            nodes.append ((node_name, "$\\sigma_{" + str(cond) + "}$", ypos, xpos))
            # add the edge leading to the child
            edges.append((node_name, node_name + "0"))

            get_nodes(kidz[1], nodes, edges,  node_name + "0", ypos - 1, xpos, width)

        elif syntax_tree.data == "join":
            kidz = syntax_tree.children
            cond = kidz[3]

            # add join
            nodes.append ((node_name, "$\\Join_{" + str(cond) + "}$", ypos, xpos))
            # add the edge leading to the children
            edges.append((node_name, node_name + "0"))
            edges.append((node_name, node_name + "1"))

            get_nodes(kidz[1], nodes, edges,  node_name + "0", ypos - 1, xpos-(width/abs(ypos)), width)
            get_nodes(kidz[2], nodes, edges,  node_name + "1", ypos - 1, xpos+(width/abs(ypos)), width)

        elif syntax_tree.data == "group_by":
            kidz = syntax_tree.children

            attributes = kidz[2].children       # bypass attrs_or_funs
            attr_str = ""
            for a in attributes:
                attr_str +=  str(a) + ","
            attr_str = attr_str[:len(attr_str) - 1]

            functions = kidz[3].children        # bypass attrs_or_funs
            fun_str = ""
            for f in functions:
                fun_str +=  str(f) + ","
            fun_str = fun_str[:len(fun_str) - 1]

            # add group_by
            nodes.append ((node_name, "$_{\{" + attr_str + "\}}\\gamma_{\{" + fun_str + "\}}$", ypos, xpos))
            # add the edge leading to child
            edges.append((node_name, node_name + "0"))


            get_nodes(kidz[1], nodes, edges, node_name + "0", ypos - 1, xpos, width)


        elif syntax_tree.data == "table":
            name = syntax_tree.children[0]
            nodes.append ((node_name, str(name), ypos, xpos))

        elif syntax_tree.data == "distinct":
            kidz = syntax_tree.children
            # add distinct
            nodes.append ((node_name, "$\\delta$", ypos, xpos))
            # add the edge leading to child
            edges.append((node_name, node_name + "0"))


            get_nodes(kidz[1], nodes, edges, node_name + "0", ypos - 1, xpos, width)

def main():
    input_file = ""
    width = 2
    try:
        input_file = sys.argv[1]
    except:
        print("Argument error - NO INPUT FILE WAS PROVIDED\n\n\n")

    try:
        width = int(sys.argv[2])
    except:
        print("width was not specified: going with default (result might suck)")

    program = open(input_file)
    parsed = parse_program(program.read().strip())

    nodes = []
    edges = []

    get_nodes(parsed, nodes, edges, "node", -1, 0, width)

    print("nodes:")
    print(nodes)
    print("edges:")
    print(edges)

    tikz_program = ""
    for n in nodes:
        name, contents, ypos, xpos = n
        tikz_program += f"\\node ({name}) at ({xpos}, {ypos})" + "{" + contents + "};\n"

    for e in edges:
        n1, n2 = e
        tikz_program += f"\\draw({n1}) -- ({n2});\n"

    print("generated tikz picture:")
    print(tikz_program)

    header = '''\\documentclass{standalone}
    \\usepackage{tikz}
    \\usepackage{amsfonts}
    \\usepackage{cmbright}
    \\begin{document}
    \\begin{tikzpicture}
    \\newcommand{\\lpar}{(}
    \\newcommand{\\rpar}{)}'''

    footer = "\\end{tikzpicture}\n\n\\end{document}\n"

    tikz_program = header + tikz_program + footer

    result_file = open("result.tex", "w")
    result_file.write(tikz_program)
    result_file.close

main()
