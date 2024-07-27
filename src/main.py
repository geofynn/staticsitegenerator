import shutil
import os

from markdown_to_html import markdown_to_html

def copy_contents(source, destination, first=True):
    if os.path.exists(destination) and first == True:
        shutil.rmtree(destination)
        os.mkdir(destination)
    current_dir = os.listdir(source)
    for file in current_dir:
        if os.path.isfile(f"{source}/{file}"):
            shutil.copy(f"{source}/{file}", destination)
        else:
            os.mkdir(f"{destination}/{file}")
            copy_contents(f"{source}/{file}", f"{destination}/{file}", False)
def extract_title(markdown):
    split_markdown = markdown.split("\n")
    for split in split_markdown:
        if split.startswith("# "):
            return split.replace("# ", "").strip()
    raise Exception("Invalid Markdown: No Heading 1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file_content = open(from_path)
    markdown = file_content.read()
    file_content.close()
    file_template = open(template_path)
    template = file_template.read()
    file_template.close()
    markdown_as_html = markdown_to_html(markdown).to_html()
    template = template.replace("{{ Title }}", extract_title(markdown))
    template = template.replace("{{ Content }}", markdown_as_html)
    dest_path = dest_path.replace("md", "html")
    dest = open(dest_path, 'x')
    dest.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents_of_content_path = os.listdir(dir_path_content)
    for file in contents_of_content_path:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        else:
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

def main():
    source_path = "./static"
    destination_path = "./public"
    copy_contents(source_path, destination_path)

    generate_pages_recursive("./content", "./template.html", "./public")

main()
