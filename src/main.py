from textnode import TextNode
from util import generate_pages_recursive
import os, shutil

def main():
    clean_and_set_public("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")

def clean_and_set_public(source, destination):
    shutil.rmtree(destination)
    os.mkdir("public")

    source_abs = os.path.abspath(source)
    files = os.listdir(source)
    for file_name in files:
        if not os.path.isfile(os.path.join(source_abs, file_name)):
            r_clean_and_set_public(source, destination, file_name)
        else:
            shutil.copy(os.path.join(source_abs, file_name), destination)

def r_clean_and_set_public(source, destination, nested_dir):
    os.mkdir("public/" + nested_dir)
    nested_abs = os.path.abspath(source) + "/" + nested_dir
    files = os.listdir(nested_abs)
    for file_name in files:
        if not os.path.isfile(os.path.join(nested_abs, file_name)):
            r_clean_and_set_public(nested_abs, destination+"/" + nested_dir, file_name)
        else:
            print(nested_abs)
            shutil.copy(os.path.join(nested_abs, file_name), destination+"/" + nested_dir)
        

main()