# Project Evaluation:

- introduction of problem, description of methods, discussion of results: 18/20
- data preparation 10/10
- implementation of methods: 19/20
- runnable by third party: 9/10
- cross-validation and model selection: 10/10
- visualization: 9/10
- model checking: 8/10
- evaluation of performance characteristics: 10/10

## Comments: 

Nice work overall! Data processing is really good (I think), though it would have been nice to have more explicit narrative around your processes. Its not generally a good idea to throw out extreme (but biologically plausible) values; not all extreme values are wrong, and some are very informative. Its not entirely clear how you dealt with the non-independence of individuals with multiple admissions. On the model evaluation side, be careful about your choice of metric for classification; with the class imbalance in this dataset, its easy to get 75-90% accuracy by just predicting no readmission for everyone. The Bayes approach meeded a more flexible approach than just the `glm` module (e.g. better priors, hierarchical structure).

No need to generate HTML reports, as notebooks are auto-rendered to HTML on GitHub anyway.

SCORE: 93/100