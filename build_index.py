import execjs
import json
import os
import argparse


default_path = './site/mkdocs/'


def load_mkdocs_index(data_path):
    with open(data_path) as f:
        mkdocs_index = json.load(f)
    return mkdocs_index


def generate_search_index(index_path, project_name):
    """generate pre-built lunr.js search index"""

    build_js = r"""
        var lunr = require("%s");
        function map_to_object(map) {
            const out = Object.create(null)
            map.forEach((value, key) => {
                if (value instanceof Map) {
                out[key] = map_to_object(value)
                }
                else {
                out[key] = value
                }
                })
            return out
        }
        var build_index =function(data) {
            /* Preprocess and index sections and documents */
            mapped_docs = data.docs.map(function(e) {
                return e.location = "%s" + e.location, e
                })
            this.docs_ = mapped_docs.reduce((docs, doc) => {
            const [path, hash] = doc.location.split("#")
              /* Associate section with parent document */
              if (hash) {
                doc.parent = docs.get(path)

                /* Override page title with document title if first section */
                if (doc.parent && !doc.parent.done) {
                  doc.parent.title = doc.title
                  doc.parent.text  = doc.text
                  doc.parent.done  = true
                }
              }

              /* Some cleanup on the text */
              doc.text = doc.text
                .replace(/\n/g, " ")               /* Remove newlines */
                .replace(/\s+/g, " ")              /* Compact whitespace */
                .replace(/\s+([,.:;!?])/g,         /* Correct punctuation */
                  (_, char) => char)

              /* Index sections and documents, but skip top-level headline */
              if (!doc.parent || doc.parent.title !== doc.title)
                docs.set(doc.location, doc)
              return docs
            }, new Map)
            const docs = this.docs_
            index_ = lunr(function() {
              this.field("title", { boost: 10 })
              this.field("text")
              this.ref("location")

              /* Index documents */
              docs.forEach(doc => this.add(doc))
            })
            var combined_index =  JSON.stringify({search_idx: index_, doc_tree: map_to_object(this.docs_)});
            return combined_index;
          }
        """

    lunr_path = os.path.join(os.getcwd(), 'lunr.min.js')
    js = build_js % (lunr_path, project_name)

    try:
        runtime = execjs.get(execjs.runtime_names.Node)
        context = runtime.compile(js)
        return context.call('build_index', load_mkdocs_index(index_path))
    except execjs.Error as e:
        print(e)
        return '{}'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Prebuild lunr.js index')
    parser.add_argument('--i', help='path to search_index.json produced by mkdocs build', required=False,
                        default=os.path.join(default_path, 'search_index.json'))
    parser.add_argument('--n', help='project name matching s3 uri (i.e data.allenai.org/<project name>', required=False,
                        default='.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    combined_idx = generate_search_index(args.i, args.n)
    combined_json = json.loads(combined_idx)
    with open(os.path.join(default_path, 'combined_idx.json'), 'w') as f:
        json.dump(combined_json, f)
