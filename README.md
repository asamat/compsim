compsim
==============

Python library form computing similarity between 2 company names<br />
The implementation uses an algorithm which is a combination of jaccard distance, 
tfidf score and levenshtein distance

Installation
============

pip install compsim

Usage
=====
```python
from compsim.company_name_similarity import CompanyNameSimilarity
cm = CompanyNameSimilarity()
cm.match_score(company_1, company_2)

#Example
>>> cm.match_score("Rombus Solutions ltd.", "Axia Solutions pvt ltd")
-0.007964495887409403
>>> cm.match_score("Axia Solutions", "Axia Solutions pvt ltd")
0.808220063856011
>>> cm.match_score("Axia Computers", "Axia Solutions pvt ltd")
0.2897981866800011
```
