from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from scipy import spatial
import math


class Doc2VecSimilarity:

    # Any one-time initialization code can go here.  There entire nested question-and-answer
    # dataset is passed as a parameter, in case the initialization requires any of that data.

    def init(self, allQuestions):

        model = Doc2Vec(alpha=0.025, min_alpha=0.025)
        questions = []
        counter = 0
        for q in allQuestions:
            tagged = TaggedDocument(words=allQuestions[q]['question_words'], tags=['SENT_%s' % counter])
            questions.append(tagged)
            counter += 1
            for r in allQuestions[q]['related']:
                tagged = TaggedDocument(words=allQuestions[q]['related'][r]['question_words'], tags=['SENT_%s' % counter])
                questions.append(tagged)
                counter += 1
        model.build_vocab(questions)

        for q in allQuestions:
            allQuestions[q]['doc2vec'] = model.infer_vector(allQuestions[q]['question'])
            for r in allQuestions[q]['related']:
                allQuestions[q]['related'][r]['doc2vec'] = model.infer_vector(allQuestions[q]['related'][r]['question'])
        return

    # Given a specific question, return a feature vector (one-dimensional array of one
    # or more features.

    def createFeatureVector(self, question, parentQuestion):
        #similaritySciPy = 1 - spatial.distance.cosine(question['doc2vec'], parentQuestion['doc2vec'])
        similarityJosh = Doc2VecSimilarity.cosineSimilarity(question['doc2vec'], parentQuestion['doc2vec'])
        return [similarityJosh]

    # Returns a list of names for the features generated by this module.  Each entry in the
    # list should correspond to a feature in the createFeatureVector() response.

    def getFeatureNames(self):
        return ['doc2vec-similarity']

    def cosineSimilarity(questionNew=[], relatedQuestion=[]):

        '''dot product of two lists'''

        def dotProduct(x=[], y=[]):
            total = 0
            for component, element in zip(x, y):
                prod = component * element
                total = total + prod
            return total

        '''sum of the squares of vector components'''

        def sumSquares(x=[]):
            total = 0
            for component in x:
                sqr = component * component
                total = total + sqr
            return total

        '''main method'''
        numerator = dotProduct(questionNew, relatedQuestion)
        denominator = math.sqrt(sumSquares(questionNew)) * math.sqrt(sumSquares(relatedQuestion))
        cosineSimilarity = numerator / denominator

        return cosineSimilarity
