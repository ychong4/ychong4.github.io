## Clustering analysis in a Credit Card customer dataset

**Project goal:** The goal of this project is to perform clustering analysis in a credit card customer dataset, which can provide business insights and values by using different marketing strategies to each customer groups.

### Columns in dataset

(1) CUST_ID <br>
(2) BALANCE <br>
(3) BALANCE_FREQUENCY <br>
(4) PURCHASES <br>
(5) ONEOFF_PURCHASES <br>
(6) INSTALLMENTS_PURCHASES <br>
(7) CASH_ADVANCE <br>
(8) PURCHASES_FREQUENCY <br>
(9) ONEOFF_PURCHASES_FREQUENCY <br>
(10) PURCHASES_INSTALLMENTS_FREQUENCY <br>
(11) CASH_ADVANCE_FREQUENCY <br>
(12) CASH_ADVANCE_TRX <br>
(13) PURCHASES_TRX <br>
(14) CREDIT_LIMIT <br>
(15) PAYMENTS <br>
(16) MINIMUM_PAYMENTS <br>
(17) PRC_FULL_PAYMENT <br>
(18) TENURE <br>

### Fill in Missing values

There are some missing values in the credit_limit and minimum payments columns. Due to these columns are numerical variables, I will fill in the mean values in the missing rows.

### Plotting the columns

![](univariate_analysis.png)

### Removing outliers

I checked the mean and standard deviation of each columns. Then, the upper limit is calculated as [mean + 3 * standard deviation] and the lower limit is calculated as [mean - 3 * standard deviation]. The outliers are the rows that have values either lower than lower limit or higher than upper limit. There are a total of 102 outliers removed from this process.

### Correlation matrix

![](cm.png)

We can see there are some columns highly correlated with others, such as **oneoff purchases** is highly correlated with **purchases**, **purchases frequency** is highly correlated with **purchases installment frequency**, and **cash advance frequency** is highly correlated with **cash advance trx**.
