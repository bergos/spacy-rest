import os
import spacy
from flask import Flask, request
from flask_restful import Resource, Api

model = spacy.load(os.environ['SPACY_MODEL'])

app = Flask(__name__)
api = Api(app)


class SpacyCoreNlp(Resource):
    def post(self):
        query = request.data.decode(request.charset)
        doc = model(query)

        result = dict()
        result['sentences'] = []

        for sent in doc.sents:
            sentence = dict()
            sentence['basicDependencies'] = []
            sentence['tokens'] = []

            for word in sent:
                node = dict()
                node['dep'] = word.dep_
                if word.dep_ == 'ROOT':
                    node['governor'] = 0
                    node['governorGloss'] = 'ROOT'
                else:
                    node['governor'] = word.head.i + 1
                    node['governorGloss'] = word.head.text
                node['dependent'] = word.i + 1
                node['dependentGloss'] = word.text
                sentence['basicDependencies'].append(node)

                token = dict()
                token['index'] = word.i + 1
                token['word'] = word.text
                token['lemma'] = word.lemma_
                token['pos'] = word.tag_
                sentence['tokens'].append(token)

            result['sentences'].append(sentence)

        return result


api.add_resource(SpacyCoreNlp, '/core-nlp')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
