import csv
import json
from ibm_watson import NaturalLanguageClassifierV1 as NLClassifier
from ibm_watson import DiscoveryV1
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

del_marks = ['"', '\'', '\n', '\r', '<br>', 'Q: ', 'A: ', '&amp;', '&quot;']
max_confidence = 1.0
min_confidence = .96

def main():
    output = {}
    
    # Load the classifier
    authenticator = IAMAuthenticator('d61RIxMA4RwhewIoThcevX0xJqAo80mMyAnkjwNb8ePy')
    discovery = DiscoveryV1(version='2018-08-01',
                            authenticator=authenticator)
    discovery.set_service_url('https://gateway.watsonplatform.net/natural-language-classifier/api')
    classifier = NLClassifier(authenticator)

    # Take Input, can input multiple lines
    with open('../data/test_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            text = row[0]
            # Clean the text
            for mark in del_marks:
                text = text.replace(mark, '')
            text = text.replace('&#039;', '\'')

            # Classify
            result = classifier.classify('90dbdex665-nlc-266', text).get_result()
            confidence = result['classes'][0]['confidence']
            normalized_confidence = (confidence-min_confidence)/(max_confidence-min_confidence)
            output[text] = normalized_confidence
    csvfile.close()

    # Write output
    file = open('output.txt', 'w+')
    for out in output:
        string = out + ', ' + str(output[out])
        file.write(string)
    file.close()


if __name__ == '__main__':
    main()
