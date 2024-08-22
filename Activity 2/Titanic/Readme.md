## Titanic: Machine Learning from Disaster

![](overview-Titanic.webp)

**Overview**

This is a dataset from Kaggle where data professionals are requested to training machine learning models to predict if the passengers in the test set will survive from the disaster. 

</br>

**Data Dictionary**
 
| Variable | Definition |
| --- | --- |
| survival | Survival 0=No, 1=Yes |
| pclass | Ticket class 1=1st, 2=2nd, 3=3rd |
| sex | Sex |
| age | Age in years |
| sibsp | # of siblings / spouses aboard the Titanic |
| parch | # of parents / children aboard the Titanic |
| ticket | Ticket number |
| fare | Passenger fare |
| cabin | Cabin number |
| embarked | Port of Embarkation C=Cherbourg, Q=Queenstown, S=Southampton |

</br>

**Variable Notes** </br>

pclass: A proxy for socio-economic status (SES) </br>
1st = Upper </br>
2nd = Middle </br>
3rd = Lower </br>
age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5 </br>
sibsp: The dataset defines family relations in this way... </br>
Sibling = brother, sister, stepbrother, stepsister </br>
Spouse = husband, wife (mistresses and fiancés were ignored) </br>
parch: The dataset defines family relations in this way... </br>
Parent = mother, father </br>
Child = daughter, son, stepdaughter, stepson </br>
Some children travelled only with a nanny, therefore parch=0 for them. </br>


**Data Visualization** </br>

![](plots.png)

The plots show the distributions of the variables. We observe the right skew on the passenger age. Also, there is an outlier in the ticket fare variable.


**Data Transformation** </br>
A few data transformation is done on this dataset. </br>
1. Fill Age missing values </br>
2. Create column CabinGroup using first letter of Cabin </br>
3. Examine the survival rate of Cabin Groups
4.  Create column price = ticket number / number of passenger with same number
5.  Imputed fare price outliers with mean price
6.  Create column FamilyOnBoard to calculate the number to family members

</br>

Interestingly, the cabin groups with its survival rate is shown below:

| Cabin Group | Value Count | Survival Rate |
| --- | --- | -- |
| N | 1014 | 0.300 |
| C | 94 | 0.593 |
| B | 65 | 0.745 |
| D | 46 | 0.758 |
| E | 41 | 0.750 |
| A | 22 | 0.467 |
| F | 21 | 0.615 |
| G | 5 | 0.500 |
| T | 1 | 0.000 |

</br>

Also, we examined the correlation of 'Survived' variable with other variables:

| Survived | Correlation |
| --- | --- |
| Survived | 1.000 |
| Price | 0.270 |
| Fare | 0.252 |
| Parch | 0.082 |
| FamilyOnBoard | 0.017 |
| SibSp | -0.035 |
| Age | -0.070 |
| Pclass | -0.338 |

We can see there are a few variables that have some correlation with the survival rate. For example, Pclass, Price, and Fare.

</br>

A few plots are created to examine the relationship betweent the survival rate and the variables:</br>

(1) Survived vs Age

![](survival_age.png)

We observe that the survival rate for children and senior are much higher compare to the age group from 15-35.


(2) Survived vs Price

![](survival_price.png)

We observe that the survival rate for price > 15 are much higher than the passenger with lower price ticket. 

(3) Survived vs Family members

![](survival_family.png)

We did not have meaningful conclusion from the plot.

</br>

**Machine Learning Model** </br>

We train a few machine learning models with cross-validation method used. The conclusion are shown below:

| Model | Train_Set_Accuracy | Dev_Set_Accuracy |
| --- | --- | --- |
| Random Forest | 0.860 | 0.860 |
| Gradient Boosting Classifier | 0.992 | 0.782 |
| Support Vector Kernel | 0.836 | 0.849 |
| Cat Boost Classifier | 0.881 | 0.838 |

It appears that the Gradient Boosting Classifier is overtrained. Also, it appears that the best performing model for this dataset prediction is the Random Forest model.
