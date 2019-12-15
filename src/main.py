import json
from ibm_watson import NaturalLanguageClassifierV1 as NLClassifier
from ibm_watson import DiscoveryV1
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

del_marks = ['"', '\'', '\n', '\r', '<br>', 'Q: ', 'A: ', '&amp;', '&quot;']
max_confidence = 1.0
min_confidence = .96

def main():
    # Define everything needed later
    inputs = []
    max_btwness = 0.0
    min_btwness = 0.0
    avg_btwness = 0.0
    
    # Load the classifier
    authenticator = IAMAuthenticator('d61RIxMA4RwhewIoThcevX0xJqAo80mMyAnkjwNb8ePy')
    discovery = DiscoveryV1(version='2018-08-01',
                            authenticator=authenticator)
    discovery.set_service_url('https://gateway.watsonplatform.net/natural-language-classifier/api')
    classifier = NLClassifier(authenticator)

    # Take Input, can input multiple lines
    text_file = open('../data/input.txt')
    for line in text_file:
        line_text = line.split(',', 2) # maximum 2 splits, because some text contains commas
        n1 = -1
        n2 = -1
        try:
            n1 = int(line_text[0])
            n2 = int(line_text[1])
        except:
            print("Node id should be an integer")
        # Clean the text
        for mark in del_marks:
            text = line_text[2].replace(mark, '')
        text = text.replace('&#039;', '\'')
        # Store this line if input is valid
        if not (n1 == -1 or n2 == -1):
            input = [n1, n2, text]
            inputs.append(input)
    text_file.close()
    
    # Get the statistics of the graph
    stat_file = open('../data/stat.txt')
    for line in stat_file:
        if 'max' in line:
            max_btwness = float(line.split(': ')[1])
        if 'min' in line:
            min_btwness = float(line.split(': ')[1])
        if 'avg' in line:
            avg_btwness = float(line.split(': ')[1])
    stat_file.close()

    # Get the betweenness record
    count = 0
    file = open('../data/btwness.txt')
    for line in file:
        line_text = line.split(',')
        n1 = int(line_text[0])
        n2 = int(line_text[1])
        btwness = float(line_text[2])
        # I search if there's an input represents the same edge as appeared in full list
        # so that I only need to iterate the full list of edges once,
        # because the length of inputs is much smaller than the length of all edges
        # and interating through inputs repeatly will be less costly
        # than iterating through all edges repeatly
        for input in inputs:
            # Append btwness as the 4th feature to each input
            index = inputs.index(input)
            if input[0] == n1:
                if input[1] == n2:
                    input.append(btwness)
                    count = count + 1 # count how many inputs have the 4th feature
            if input[1] == n1:
                if input[0] == n1:
                    input.append(btwness)
                    count = count + 1
            inputs[index] = input
            # Don't keep iterating if all inputs are processed
            if count == len(inputs):
                break
    file.close()

    for input in inputs:
        # Classify
        result = classifier.classify('90dbdex665-nlc-266', input[2]).get_result()
        class_name = result['classes'][0]['class_name']
        confidence = result['classes'][0]['confidence']
        # if top class is 'bully'
        if 'bully' in class_name:
            normalized_confidence = (confidence-min_confidence)/(max_confidence-min_confidence)
            if len(input) != 4:
                # This means their is no betweenness data appended in the previous step
                # So the edge does not exist, they are strangers, it is purely bullying
                if normalized_confidence > .9:
                    print(input[2] + "bully")
            else:
                btwness = input[3]
                print(f'{confidence}, {normalized_confidence}, {btwness}')
                if normalized_confidence > .9:
                    if btwness > avg_btwness: # need a better threshold
                        # larger btwness means less significant network
                        print(input[2] + "prob. FP")
                    else:
                        print(input[2] + "bully")
                elif normalized_confidence > .5:
                    if btwness < avg_btwness: # need a better threshold
                        # smaller btwness means more significant network
                        print(input[2] + "prob. FN")

if __name__ == '__main__':
    main()
