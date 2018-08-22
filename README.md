# Note builder

Some simple build tools for compiling my markdown notes into html files.

It also:

 - Compile statistics on the note collection
 - Generate index pages for tags
 - Convert my custom tag syntax to links to the index pages
 - Generate a gallery page
 - (one day) analyse link structure between notes, and check for missing

## Usage

The note directory requires a config.json file as follows:

```
{
  "assets": "assets",
  "css": ["assets/css/tufte.css",
          "assets/css/custom.css"],
  "output": "../_build"
}
```

Where assets are the static assets of the notes, css lists any css files to apply, and output is the final ouput directory

Build the note collection with run.py
