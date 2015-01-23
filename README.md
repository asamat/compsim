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
# returns a value between 0 - 1
cm.match_score(company_1, company_2)
```
