# This file has functions to compute shingles, minhash, and Jaccard Similarity.
# Khaled Alhosani (kah579) Myunggun Seo (ms9144)
import string
from datetime import datetime
from hashlib import sha512
import itertools

def getWords(line):
   words = line.strip().lower().split()
   return list( map(lambda w: w.strip(string.punctuation), words) )

#k-shingle based on words
def kShingleWord(k, line, removeFirstWord=True):
    words = getWords(line)
    idx = words.pop(0)
    result = [' '.join([words[i+j] for j in range(k)]) for i in range(len(words)-k)]
    return result if removeFirstWord else (idx, result)
    
#k-shingle based on letters
def kShingle(k, line, removeFirstWord=True):
    words = getWords(line)
    idx = words.pop(0)
    line = ''.join(words)
    result = [''.join([line[i+j] for j in range(k)]) for i in range(len(line)-k)]
    # if removeFirstWord, return list of elements like ['0075c1c5', '005cf4fb',..., '00ccde89']
    # if not removeFirstWord, return list of elements like ('6066', ['0075c1c5', '005cf4fb',..., '00ccde89'])
    return result if removeFirstWord else (idx, result)
    
    

st = "6060 SECOND LORD. That approaches apace. I would gladly have him see his PAROLLES. What the dèvil should move me to undertake the recovery cheek of two pile and a half, but his right cheek is worn bare. COUNTESS. To be young again, if we could, I will be a fool in LAFEU. He was excellent indeed, madam; the King very lately spoke Boys. He was my father; and he is thrice a villain that says such father. He that so generally is at all times good must of Half won is match well made; match, and well make it; PAROLLES. It is to be recovered. But that the merit of service is HELENA. 'Till I have no wife, I have nothing in France.' Here is a pur of Fortune's, sir, or of Fortune's cat, but not CLOWN. You must not think I am so simple but I know the devil not seem to understand him, unless some one among us, whom we FIRST LORD. I am heartily sorry that he'll be glad of this. His part o' th' isle. Then does he say he lent me a solemn leave. His lordship will next morning for France. The them whipt; or I would send them to th' Turk to make eunuchs of. PAROLLES. 'Five or six thousand horse' I said-I will say true- 'or But take the High'st to witness. Then, pray you, tell me: But do not speak to me. Lead me to my chamber. Exeunt "
print("k-shingle word", kShingleWord(5, st)[:10])
print("k-shingle letters", kShingle(5, st)[:20])

# Jaccard similarity from two lists/sets of strings
# if only given s1, assume s1 holds both of the two lists and unpack it
def jaccardSim(s1, s2=None):
    if s2 is None:
        s1, s2 = s1
    s1 = set(s1)
    s2 = set(s2)
    return len(s1 & s2) / len(s1 | s2)

# shingles should be given as list of strings
# this hashes all shingles (8 hash functions) and for each hash function find minimum value hashes.
# the hash might not be a number but okay if hash is consistent and there is a clear ordering (alphabetical here)
def minhash(shingles, h=16, l=8):
    #h = 16 # no. of hashes we want
    #l = 8 # length of each hash
    hashes = ['z'*l] * h # minhashes are initialized to 'zzzzzzzz'
    m = sha512()
    for shingle in shingles:
        m.update(shingle.encode('utf-8'))
        newhash = m.hexdigest()
        newhashes = [newhash[i:i+l] for i in range(0,l*h,l)] #divide 128 characters into 16 hashes of length 8
        hashes = [min(hashes[i], newhashes[i]) for i in range(h)]
    return hashes


#st1 is documents 6393 and 7378 combined, st2 is 6393
# similarity should be around 0.5 for both word-shingle and letter-shingle
# st1 = "6393 wear the surplice of humility over the black gown of a big heart. away; know it before the report come. If there be breadth enough BERTRAM. Why, if you have a stomach, to't, monsieur. If you think train'd me like a peasant, obscuring and hiding from me all BERTRAM. I'll lend it thee, my dear, but have no power KING. If it were yours by none of all these ways, See at the end of this file: * CONTENT NOTE (added in 2017) * face; if your lordship be in't, as I believe you are, you must COUNTESS. With very much content, my lord; and I wish it happily CHARMIAN. Nay, if an oily palm be not a fruitful prognostication, I LAFEU. I will buy me a son-in-law in a fair, and toll for this. FIRST SOLDIER. Boskos vauvado. I understand thee, and can speak thy PAROLLES. O my good lord, you were the first that found me. in death, which commits some loving act upon her, she hath such a PAROLLES. By the hand of a soldier, I will undertake it. child at fifty, to whom Herod of Jewry may do homage. Find me to sad a passage 'tis!-whose skill was almost as great as his in death, which commits some loving act upon her, she hath such a CLOWN. Faith, sir, 'a has an English name; but his fisnomy is more itself, which could not be her office to say is come, was 7378 whilst I have a tooth in my head. Why, he's able to lead her a against his valour; and my state that way is dangerous, since I PAROLLES. The Duke knows him for no other but a poor officer of to th' Queen? O that I knew this husband, which you say must ANTONY. That which is now a horse, even with a thought Fare you well, my lord; and believe this of me: there can be no beat thee. I think thou wast created for men to breathe ANTONY. Do so, we'll speak to them; and to-night I'll force much of my father in me as you, albeit I confess your coming dare not give. Wherefore, what's the instance? Tongue, I must put the toothpick, which wear not now. Your date is better in your ANTONY. I would they'd fight i' th' fire or i' th' air; PAROLLES. I know not what the success will be, my lord, but the neighbouring languages, therefore we must every one be a man of KING. Know you this ring? This ring was his of late. when old robes are worn out there are members to make new. If ENOBARBUS. Why, sir, give the gods a thankful sacrifice. When it sadness. My brother Jaques he keeps at school, and report speaks PAROLLES. I beseech your honour to hear me one single word. when he number'd thirty; 'a will be here to-morrow, or I am "
# st2 = "6393 wear the surplice of humility over the black gown of a big heart. away; know it before the report come. If there be breadth enough BERTRAM. Why, if you have a stomach, to't, monsieur. If you think train'd me like a peasant, obscuring and hiding from me all BERTRAM. I'll lend it thee, my dear, but have no power KING. If it were yours by none of all these ways, See at the end of this file: * CONTENT NOTE (added in 2017) * face; if your lordship be in't, as I believe you are, you must COUNTESS. With very much content, my lord; and I wish it happily CHARMIAN. Nay, if an oily palm be not a fruitful prognostication, I LAFEU. I will buy me a son-in-law in a fair, and toll for this. FIRST SOLDIER. Boskos vauvado. I understand thee, and can speak thy PAROLLES. O my good lord, you were the first that found me. in death, which commits some loving act upon her, she hath such a PAROLLES. By the hand of a soldier, I will undertake it. child at fifty, to whom Herod of Jewry may do homage. Find me to sad a passage 'tis!-whose skill was almost as great as his in death, which commits some loving act upon her, she hath such a CLOWN. Faith, sir, 'a has an English name; but his fisnomy is more itself, which could not be her office to say is come, was "
st1 = "if your lordship be in't, as I believe you are, you must your son was his return home, I moved the King my master to heed of the allurement of one Count Rousillon, a idle KING. Thou know'st has rais'd me from my sickly bed. but I must attend his command, to whom I am now in knows; 'tis a goodly patch of velvet. His left cheek is a exile with him, whose lands revenues enrich the new Duke; ENOBARBUS. This was but as a fly an eagle. We had much more COUNTESS. Sirrah, tell my gentlewoman would speak with her; Helen CLEOPATRA. Not to hear thee sing; I take no pleasure CLEOPATRA. I have mind to strike thee ere thou speak'st. difference betwixt their two estates; Love god, that would not nicer needs. The last was the greatest, that I have not ended ORLANDO. As I Adam, it was upon this fashion bequeathed me the King's sake, he were living! I it would be the death of [To CAESAR] Thus do they, sir: they take the flow o' th' ENOBARBUS. Why, sir, give the gods thankful sacrifice. When it IRAS. Am I not an inch of fortune better she? FIRST LORD. I heartily sorry that he'll be glad of this. could be contented to be what they there were no fear in "
st2 = "face; if your lordship be in't, as I believe you are, you must your son was upon his return home, I moved the King my master to heed of the allurement of one Count Rousillon, a foolish idle KING. Thou know'st she has rais'd me from my sickly bed. but I must attend his Majesty's command, to whom I am now in knows; but 'tis a goodly patch of velvet. His left cheek is a exile with him, whose lands and revenues enrich the new Duke; ENOBARBUS. This was but as a fly by an eagle. We had much more COUNTESS. Sirrah, tell my gentlewoman I would speak with her; Helen CLEOPATRA. Not now to hear thee sing; I take no pleasure CLEOPATRA. I have a mind to strike thee ere thou speak'st. difference betwixt their two estates; Love no god, that would not nicer needs. The last was the greatest, but that I have not ended ORLANDO. As I remember, Adam, it was upon this fashion bequeathed me the King's sake, he were living! I think it would be the death of ANTONY. [To CAESAR] Thus do they, sir: they take the flow o' th' ENOBARBUS. Why, sir, give the gods a thankful sacrifice. When it IRAS. Am I not an inch of fortune better than she? FIRST LORD. I am heartily sorry that he'll be glad of this. could be contented to be what they are, there were no fear in "
s1 = kShingle(5, st1)
s2 = kShingle(5, st2)
print("JS based on k-letter-shingles", jaccardSim(s1, s2))
s1 = kShingleWord(5, st1)
s2 = kShingleWord(5, st2)
print("JS based on k-word-shingles", jaccardSim(s1, s2))
print(minhash(s1))
print(minhash(s2))


# st2 = "6393 wear the surplice of humility over the black gown of a big heart. away; know it before the report come. If there be breadth enough BERTRAM. Why, if you have a stomach, to't, monsieur. If you think train'd me like a peasant, obscuring and hiding from me all BERTRAM. I'll lend it thee, my dear, but have no power KING. If it were yours by none of all these ways, See at the end of this file: * CONTENT NOTE (added in 2017) * face; if your lordship be in't, as I believe you are, you must COUNTESS. With very much content, my lord; and I wish it happily CHARMIAN. Nay, if an oily palm be not a fruitful prognostication, I LAFEU. I will buy me a son-in-law in a fair, and toll for this. FIRST SOLDIER. Boskos vauvado. I understand thee, and can speak thy PAROLLES. O my good lord, you were the first that found me. in death, which commits some loving act upon her, she hath such a PAROLLES. By the hand of a soldier, I will undertake it. child at fifty, to whom Herod of Jewry may do homage. Find me to sad a passage 'tis!-whose skill was almost as great as his in death, which commits some loving act upon her, she hath such a CLOWN. Faith, sir, 'a has an English name; but his fisnomy is more itself, which could not be her office to say is come, was "

startingTime = datetime.now()
print("minhashes of a single document", minhash(kShingle(5, st2)))
print("minhashes of a single document", minhash(kShingle(5, st1)))
print(datetime.now()-startingTime)

def C(lst, r):
    #returns all "choose r" combinations as a set
    return set(map(lambda x: tuple(sorted(x)), itertools.combinations(lst, r)))
