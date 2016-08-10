
from __future__ import print_function
import numpy as np
from preprocessing_keras import preprocess
from model import seq2seq
import pdb

class train(object):
    # Train a sequence to sequence model for hindi to english translation
    def __init__(self, maxlen, vocab_size):
        self.maxlen = maxlen
        self.vocab_size = vocab_size
        self.proproces = preprocess("../data/training.hi-en.hi",
                           "../data/training.hi-en.en", vocab_size, maxlen)
        self.proproces.preprocess()
        self.vocab_en_rev = {v:k for k,v in self.proproces.vocab_en.items()}
        self.vocab_hind_rev = {v:k for k,v in self.proproces.vocab_hind.items()}


    def decode(self, x, y, mode='greedy'):
        # Decodes the probability tensor into english sentence
        if mode=='greedy':
            #pdb.set_trace()
            y = np.argmax(y, axis=2)
            x = x.tolist()[0]
            y = y.tolist()[0]
            vocab_en_rev = self.vocab_en_rev
            vocab_hind_rev = self.vocab_hind_rev
            print("\t".join(map(lambda X:vocab_en_rev[X], x)))
            print("\t".join(map(lambda X:vocab_hind_rev[X], y)))
            print("\n \n")

        elif mode=='viterbi':
            raise NotImplementedError

        else:
            raise NotImplementedError


    def encode(self, inp, lang):
        #Encodes input sentence into fixed length vector
        #print("Enter sentence in hindi")
        inp = raw_input().decode("utf-8")
        tokens = inp.split()
        seq = []
        for token in tokens:
            if token in self.proproces.vocab_hind:
                seq.append(self.proproces.vocab_hind[token])
            else:
                token = "UNK"
                seq.append(self.proproces.vocab_hind[token])
        #seq = map(lambda x:self.proproces.vocab_hind[x], tokens)
        # Normalize seq to maxlen
        X = []
        X.append(seq)
        print(X)
        temp = sequence.pad_sequences(X, maxlen=self.maxlen)
        #temp[0:len(seq)] = seq
        print(len(temp))
        #temp = np.asarray(temp).reshape(128,)
        print(temp.shape)
        prob = model.predict_on_batch(temp)#, batch_size=1, verbose=0)
        translated = self.decode(prob)
        print("Tranlated is", translated)
        print("Probabilities are", prob)
        print("Shape of prob tensor is",prob.shape)



    def train_seq2seq(self):
        print("Input sequence read, starting training")
        s2s = seq2seq(self.vocab_size + 3, self.maxlen + 2, \
                                      self.vocab_size + 3)
        model = s2s.seq2seq_plain()
        for e in range(100):
            print("epoch %d \n" % e)
            for ind, (X,Y) in enumerate(self.proproces.gen_batch()):
                loss, acc = model.train_on_batch(X, Y)#, batch_size=64, nb_epoch=1)
                #print("Loss is %f, accuracy is %f " % (loss, acc), end='\r')
                # After one epoch test one sentence
                if ind % 100 == 0:
                    testX = X[0,:].reshape(1, self.maxlen + 2)
                    testY = Y[0]
                    pred = model.predict(testX, batch_size=1)
                    self.decode(testX, pred)


if __name__ == "__main__":
    Seq2seq = train(10, 5000)
    Seq2seq.train_seq2seq()
