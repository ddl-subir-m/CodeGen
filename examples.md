**SAS - R** 

```
Simple Linear Regression and scatter plot with overlay in batch mode
data crack;
  input id age load;
  datalines;
  1  20 11.45
  2  20 10.42
  3  20 11.14
  4  25 10.84
  5  25 11.17
  6  25 10.54
  7  31  9.47
  8  31  9.19
  9  31  9.54
  ;
 
proc reg data=crack;
  model load = age / p;
  output out=crackreg p=pred r=resid;
run;
 
proc plot data=crackreg;
  plot load*age="*" pred*age="+"/ overlay;
run;
```

**English - R**

```
Give me code to run a monte carlo markov chain
```

