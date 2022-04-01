#!/usr/bin/python3
import glob, markdown, jinja2, re, os, shutil

def get_metadata(data):
    # Collect all the metadata at the beginning of the file if it exists
    # NOTE: match -- only first line
    title_table = re.match(r'---(.|\n)*?---', data)
    if title_table is None:
        return None, data

    title_table = title_table[0]

    return title_table

def trim_metadata(data):
    return  data.replace(get_metadata(data), '').strip()

def metadata2dict(table, trim_tags=False):
    """
    Parameters
    ----------
    data : str
        Markdown file of memo.
    trim_tags : bool, optional
        Remove the tags from `data`. The default is False.

    Returns
    -------
    tag_dict : dict of list
        Dictionary of the different types of tags found in the beginning of
        the memo.
        Each tag is a list so as to permit multiple tags.
    data : TYPE
        Returned `data`. If `trim_tags` = False, this is the same as `data`
        input.
    """

    tags = table.split('\n')[1:-1] # The ? doesn't seem to work...

    # Convert tags -> dictionary
    tag_dict = dict()
    for tag in tags:
        # Example is "tags: research,weekly"
        key, value = tag.split(': ', 1)

        # Example is split "research" and "weekly"
        if key == 'tags':
            value = value.split(',')
        tag_dict[key] = value
    return tag_dict

def verify_template(metadatas, templates):
    # This is where I wish Goto's were a thing in Python.
    try:
        metadatas['template'] += '.html'
    except KeyError:
        print('Warning: ' +
              str(metadatas['in_path'] +
              ' template not found, using default.html template instead'))
        metadatas['template'] = 'default.html'

    if metadatas['template'] not in templates:
        print('Warning: ' +
              str(metadatas['in_path'] +
              ' template not found, using default.html template instead'))
        metadatas['template'] = 'default.html'
    return metadatas['template']

if __name__ == "__main__":
    CONTENT_PATH = 'content/'
    TEMPLATE_PATH = 'templates/'
    OUT_PATH = 'public/'
    MARKDOWNS = ['tables', 'fenced_code', 'codehilite']
    IN_STATIC = 'static/'
    IN_RAW = 'raw/'
    OUT_STATIC = OUT_PATH+IN_STATIC

    if os.path.exists(OUT_PATH):
        shutil.rmtree(OUT_PATH)
    if os.path.exists(OUT_STATIC):
        shutil.rmtree(OUT_STATIC)
    # Copy all the raw files too
    shutil.copytree(IN_RAW, OUT_PATH)

    # Copy every static file from the the static folder into the public folder
    shutil.copytree(IN_STATIC, OUT_STATIC)


    templates = sorted(glob.glob(TEMPLATE_PATH+'*.html'))
    templates = [os.path.basename(x) for x in templates]
    env = jinja2.Environment(autoescape=jinja2.select_autoescape("html"),
                                 loader=jinja2.FileSystemLoader(TEMPLATE_PATH),
                                 trim_blocks=True, lstrip_blocks=True)
    env.globals.update(zip=zip)

    # Grab everything in the content file
    contents = sorted(glob.glob(CONTENT_PATH+'**/*.md', recursive=True))

    # Generate the content, they're all static -- and if they aren't,
    # why aren't they static?
    for content in contents:
        # Get metadata for each page
        data = open(content, 'r').read()
        page = {}
        metadata = get_metadata(data)
        page['meta'] = metadata2dict(metadata)
        meta = page['meta']


        # Set the output path for copying the file and
        # Set the path to link from other files.
        # Set the original input path for convenience.
        meta['in_path'] = content

        meta['out_path'] = OUT_PATH+content.replace(CONTENT_PATH,'')[:-3]+'.html'
        meta['out_dir'] = os.path.dirname(meta['out_path'])
        meta['path'] = '/'+content.strip(CONTENT_PATH)[:-3]+'.html'
        meta['dir'] = os.path.dirname(meta['path'])

        # Make sure there's a template, or else set it to default.
        meta['template'] = verify_template(meta, templates)

        # Generate the data
        data = trim_metadata(data)
        page['content'] = markdown.markdown(data, extensions=MARKDOWNS)

        # Minutes-specific things like "previous week" and "next week""
        if page['meta']['template'] == 'minutes.html':
            semesterly_minutes = sorted(glob.glob(os.path.dirname(content)+'/*.md'))

            # This is really hacky because it requires the file names to be
            # "meeting01.md", "meeting02.md", etc
            for i in range(len(semesterly_minutes)):
                if content == semesterly_minutes[i]:
                    position = i
            page['meta']['first'] = position == 0
            page['meta']['last']  = position == len(semesterly_minutes)-1
            if not page['meta']['first']:
                page['meta']['previous'] = os.path.basename(semesterly_minutes[position-1]).replace('.md','.html')
            if not page['meta']['last']:
                page['meta']['next'] = os.path.basename(semesterly_minutes[position+1]).replace('.md','.html')

        # We now have all the information, we can render the HTML.
        render = env.get_template(page['meta']['template'])
        html = render.render(**page)

        # Write to file
        if not os.path.exists(page['meta']['out_dir']):
            os.makedirs(page['meta']['out_dir'])
        print(page['meta']['out_path'])
        open(page['meta']['out_path'], 'w').write(html)
