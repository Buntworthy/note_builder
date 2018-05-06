# Main build script should:
#
# (putting everything in \build)
# Use pandoc for markdown to html conversion
# Copy static assets
# Run tag index generation
# Run stats
# Run plotting
# Build an index page

from glob import glob
import os
import subprocess
from jinja2 import Environment, FileSystemLoader, select_autoescape


def files_in(directory, extension):
    for (dirpath, dirname, filenames) in os.walk(directory, followlinks=True):
        for filename in filenames:
            if not filename.endswith(extension):
                break
            yield os.path.join(dirpath, filename)

def convert_all_files(directory, destination):
    build_directory = os.path.join(directory, destination)
    for markdownFile in glob(os.path.join(directory, '*.md')):
        print('Building file ' + markdownFile)
        (_, filename) = os.path.split(markdownFile)
        htmlFile = os.path.join(build_directory, filename.replace('.md', '.html'))
        subprocess.run(['pandoc',
                        markdownFile,
                        '-f', 'markdown',
                        '-t', 'html',
                        '-s', '-o', htmlFile,
                        '--css', '../assets/css/tufte.css',
                        '--css', '../assets/css/custom.css'])

def copy_assets(root, name, destination):
    source_location = os.path.join(root, name)
    destination_location = os.path.join(root, destination)
    print('Moving assets from ' + source_location)
    subprocess.run(['cp',
                    '-r',
                    source_location,
                    destination_location])

def get_all_tags(directory):
    cmd = 'ag ";;" ' + directory + ' | grep -o ";;[a-z\-]*" | sort | uniq'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    all_tags = result.stdout.decode("utf-8").split('\n')
    for tag in all_tags:
        if tag == ';;' or tag == '':
            continue
        yield tag

def build_tag_indexes(directory, destination):
    for tag in get_all_tags(directory):
        print('Building tag index ' + tag)
        tag_index_file = 'tagged-' + tag.replace(';;', '') + '.html'
        out_file_location = os.path.join(directory, destination, tag_index_file)
        with open(out_file_location, 'w') as out_file:
            html_files = []
            for filename in tagged_files_in(directory, tag):
                (root, htmlFile) = os.path.split(filename.replace('.md', '.html'))
                html_files.append(htmlFile)
            out_file.write(make_webpage(html_files))

def tagged_files_in(directory, tag):
    for markdownFile in glob(os.path.join(directory, '*.md')):
        with open(markdownFile) as f:
            for line in f:
                if tag in line:
                    yield markdownFile
                    break


def make_webpage(filenames):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('food.html')
    return template.render(files=filenames)

if __name__ == '__main__':
    base_directory = os.path.expanduser('~/notes')
    destination = 'build'
    assets = 'assets'
    convert_all_files(base_directory, destination)
    copy_assets(base_directory, assets, destination)
    build_tag_indexes(base_directory, destination)
