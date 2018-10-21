from bs4 import BeautifulSoup
from glob import glob
import networkx as nx
from networkx.drawing.nx_pydot import write_dot


def find_links(filename):
    with open(filename) as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    linked_files = []
    for link in soup.find_all("a"):
        linked_file = link.get("href")
        linked_files.append(linked_file)

    return linked_files

if __name__ == "__main__":
    files = glob("*.html")
    note_graph = nx.Graph()
    for f in files:
        if f.startswith(("tag_", "gallery")):
            continue
        linked_files = find_links(f)
        for link in linked_files:
            if not link.startswith(("http", "#", "assets", "tag_index", "gallery")):
                print(f"{f} -> {link}")
                note_graph.add_edge(f, link)


    write_dot(note_graph, "links.dot")
