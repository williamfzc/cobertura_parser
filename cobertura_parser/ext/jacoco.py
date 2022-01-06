# from: https://github.com/rix0rrr/cover2cover/blob/master/cover2cover.py
from lxml import etree as ET
import re
import os.path


def find_lines(j_package, filename):
    """Return all <line> elements for a given source file in a package."""
    lines = list()
    for sourcefile in j_package.iterfind("sourcefile"):
        if (
                sourcefile.attrib.get("name").split(".")[0]
                == os.path.basename(filename).split(".")[0]
        ):
            lines = lines + sourcefile.findall("line")
    return lines


def line_is_after(jm, start_line):
    return int(jm.attrib.get("line", 0)) > start_line


def method_lines(jmethod, jmethods, jlines):
    """Filter the lines from the given set of jlines that apply to the given jmethod."""
    start_line = int(jmethod.attrib.get("line", 0))
    larger = list(
        int(jm.attrib.get("line", 0))
        for jm in jmethods
        if line_is_after(jm, start_line)
    )
    end_line = min(larger) if len(larger) else 99999999

    for jline in jlines:
        if start_line <= int(jline.attrib["nr"]) < end_line:
            yield jline


def convert_lines(j_lines, into):
    """Convert the JaCoCo <line> elements into Cobertura <line> elements, add them under the given element."""
    c_lines = ET.SubElement(into, "lines")
    for jline in j_lines:
        mb = int(jline.attrib["mb"])
        cb = int(jline.attrib["cb"])
        ci = int(jline.attrib["ci"])

        cline = ET.SubElement(c_lines, "line")
        cline.set("number", jline.attrib["nr"])
        cline.set(
            "hits", "1" if ci > 0 else "0"
        )  # Probably not true but no way to know from JaCoCo XML file

        if mb + cb > 0:
            percentage = str(int(100 * (float(cb) / (float(cb) + float(mb))))) + "%"
            cline.set("branch", "true")
            cline.set(
                "condition-coverage",
                percentage + " (" + str(cb) + "/" + str(cb + mb) + ")",
            )

            cond = ET.SubElement(ET.SubElement(cline, "conditions"), "condition")
            cond.set("number", "0")
            cond.set("type", "jump")
            cond.set("coverage", percentage)
        else:
            cline.set("branch", "false")


def guess_filename(path_to_class, src_file_name):
    if src_file_name.endswith(".kt"):
        suffix = ".kt"
    else:
        suffix = ".java"
    m = re.match("([^$]*)", path_to_class)
    return (m.group(1) if m else path_to_class) + suffix


def add_counters(source, target):
    target.set("line-rate", counter(source, "LINE"))
    target.set("branch-rate", counter(source, "BRANCH"))
    target.set("complexity", counter(source, "COMPLEXITY", sum))


def fraction(covered, missed):
    return covered / (covered + missed)


def sum(covered, missed):
    return covered + missed


def counter(source, type, operation=fraction):
    cs = source.iterfind("counter")
    c = next((ct for ct in cs if ct.attrib.get("type") == type), None)

    if c is not None:
        covered = float(c.attrib["covered"])
        missed = float(c.attrib["missed"])

        return str(operation(covered, missed))
    else:
        return "0.0"


def convert_method(j_method, j_lines):
    c_method = ET.Element("method")
    c_method.set("name", j_method.attrib["name"])
    c_method.set("signature", j_method.attrib["desc"])

    add_counters(j_method, c_method)
    convert_lines(j_lines, c_method)

    return c_method


def convert_class(j_class, j_package):
    c_class = ET.Element("class")
    c_class.set("name", j_class.attrib["name"].replace("/", "."))

    # source file name can be None
    try:
        source_file_name = j_class.attrib["sourcefilename"]
    except KeyError:
        source_file_name = ""

    c_class.set(
        "filename",
        guess_filename(j_class.attrib["name"], source_file_name),
    )

    all_j_lines = list(find_lines(j_package, c_class.attrib["filename"]))

    # more than 8000 may causes mem issues
    if len(all_j_lines) > 8000:
        return c_class

    c_methods = ET.SubElement(c_class, "methods")
    all_j_methods = list(j_class.iterfind("method"))
    str_list = []
    for j_method in all_j_methods:
        j_method_lines = method_lines(j_method, all_j_methods, all_j_lines)
        each_node = convert_method(j_method, j_method_lines)
        str_list.append(ET.tostring(each_node, encoding="unicode"))

    for each in str_list:
        c_methods.append(ET.fromstring(each))

    add_counters(j_class, c_class)
    convert_lines(all_j_lines, c_class)
    return c_class


def convert_package(j_package):
    c_package = ET.Element("package")
    c_package.attrib["name"] = j_package.attrib["name"].replace("/", ".")

    c_classes = ET.SubElement(c_package, "classes")
    str_list = []
    for j_class in j_package.iterfind("class"):
        each_node = convert_class(j_class, j_package)
        str_list.append(ET.tostring(each_node, encoding="unicode"))

    for each in str_list:
        c_classes.append(ET.fromstring(each))

    add_counters(j_package, c_package)

    return c_package


def convert_root(source, target):
    try:
        ts = int(source.find("sessioninfo").attrib["start"]) / 1000
    except AttributeError:
        ts = -1
    target.set("timestamp", str(ts))

    packages = ET.SubElement(target, "packages")
    str_list = []
    for package in source.iterfind("package"):
        each_node = convert_package(package)
        str_list.append(ET.tostring(each_node, encoding="unicode"))

    for each in str_list:
        packages.append(ET.fromstring(each))

    add_counters(source, target)


def jacoco2cobertura(jacoco_string) -> str:
    root = ET.parse(jacoco_string).getroot()
    into = ET.Element("coverage")
    convert_root(root, into)
    output = f'<?xml version="1.0" ?>{ET.tostring(into, encoding="unicode")}'
    return output


# mem leak in lxml
# https://stackoverflow.com/a/49139904/10641498
# https://www.reddit.com/r/Python/comments/j0gl8t/psa_pythonlxml_memory_leaks_and_a_solution/
def destroy_tree(tree):
    root = tree
    node_tracker = {root: [0, None]}

    for node in root.iterdescendants():
        parent = node.getparent()
        node_tracker[node] = [node_tracker[parent][0] + 1, parent]

    node_tracker = sorted(
        [(depth, parent, child) for child, (depth, parent) in node_tracker.items()],
        key=lambda x: x[0],
        reverse=True,
    )

    for _, parent, child in node_tracker:
        if parent is None:
            break
        parent.remove(child)

    del tree
