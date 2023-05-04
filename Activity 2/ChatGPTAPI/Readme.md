## ChatGPT Prompt Engineering for Developers 
### Course Sections:

1. Introduction </br>
2. Guidelines </br>
3. Iterative </br>
4. Summarizing </br>
5. Inferring </br>
6. Transforming </br>
7. Expanding </br>
8. Chatbox </br>

## Section 1: Introduction
### Two types of large language models (LLMs)

1) **Base LLM:** Predicts next word, based on text training data

</br>

   Example:

    Input: Once upon a time, there was a unicorn

    Output: that lived in a magical forest with all her unicorn friends

</br>

2) **Instruction Tuned LLM:** Tries to follow instructions, fine-tune on instructions and good attempts at following those instructions.

RLHF: Reinforcement learning with Human Feedback 

</br>

  Example:

     Input: What is the capital of France?

     Output: The capital of France is Paris
     
     
### To install chatGPT

      !pip install openai
      

## Section 2: Guidelines

### Two Principles of Prompting

</br>

#### Principle 1: Write clear and specific instructions

**Tactic 1:** Use delimeters

```
    Triple quotes: """
    Triple backticks: ```
    Triple dashes: ---
    Angle brackets: <>
    XML tags: <tag> </tag>
```

**Tactic 2:** Ask for structured output

```
HTML, JSON
```

**Tactic 3:** Check whether conditions are satisfied 

```
Check assumptions required to do the task
```


**Tactic 4:** Few-shot prompting

```
Give successful examples of completing task, then ask model to perform the task
```

</br>

#### **Principle 2: Give the model time to think**

**Tactic 1:** Specify the steps to complete a task

```
    Step 1: ...
    Step 2: ...
    ...
    Step N: ...
```

**Tactic 2:** Instruct the model to work out its own solution before rushing to a conclusion

</br>

### Model Limitations

</br>

**Hallucination:** Makes statements that sound plausible but are not true

**Reducing hallucinations:** First find relevant information, then answer the question based on the relevant information


</br>


## Section 3: Iterative

### Iterative Prompt Development

**Prompt Guidelines:**
```
- Be clear and specific
- Analyze why result does not give desired output.
- Refine the idea and the prompt.
- Repeat.
```
</br>

**Iterative Process:**
```
- Try something.
- Analyze where the result does not give you what you want.
- Clarify instructions, give more time to think.
- Refine prompts with a batch of examples.
```



## Section 4: Summarizing

ChatGPT can be used to summarize text with a focus on specific topics

### Text to summarize
```
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""
```
</br>

### Summarize with a word/sentence/character limit

```
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)
```
Output:
```
Soft and cute panda plush toy loved by daughter, but a bit small for the price. Arrived early.
```

### Summarize with a focus on price and value
```
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the \
pricing deparmtment, responsible for determining the \
price of the product.  

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects \
that are relevant to the price and perceived value. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)
```
Output:
```
The panda plush toy is soft, cute, and loved by the recipient, but the price may be too high for its size.
```

### Try "extract" instead of "summarize"
```
prompt = f"""
Your task is to extract relevant information from \ 
a product review from an ecommerce site to give \
feedback to the Shipping department. 

From the review below, delimited by triple quotes \
extract the information relevant to shipping and \ 
delivery. Limit to 30 words. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)
```
Output:
```
The product arrived a day earlier than expected.
```

</br>

## Section 5: Inferring

ChatGPT can be used to infer sentiment and topics from product reviews and news articles

</br>

### Product review text
```
lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""
```

</br>

### Sentiment (positive/negative)
```
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
```
Output:
```
positive
```

</br>

### Identify types of emotions
```
prompt = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
```
Output:
```
happy, satisfied, grateful, impressed, content
```
</br>

### Extract product and company name from customer reviews

```
prompt = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
```
Output:
```
{
  "Sentiment": "positive",
  "Anger": false,
  "Item": "lamp with additional storage",
  "Brand": "Lumina"
}
```
</br>

### Inferring Topics
```
prompt = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""
response = get_completion(prompt)
print(response)
```
Output:
```
government survey, job satisfaction, NASA, Social Security Administration, employee concerns
```
</br>

## Section 6: Transforming

ChatGPT is trained with sources in many languages. It can be used for Translation, Tone Transformation, Format Conversion, and Spellcheck/Grammar check.

</br>

### Translation 

```
prompt = f"""
Translate the following  text to French and Spanish
and English pirate: \
```I want to order a basketball```
"""
response = get_completion(prompt)
print(response)
```
Output:
```
French pirate: ```Je veux commander un ballon de basket```
Spanish pirate: ```Quiero pedir una pelota de baloncesto```
English pirate: ```I want to order a basketball```
```

</br>

### Tone Transformation

```
prompt = f"""
Translate the following from slang to a business letter: 
'Dude, This is Joe, check out this spec on this standing lamp.'
"""
response = get_completion(prompt)
print(response)
```
Output:
```
Dear Sir/Madam,

I am writing to bring to your attention a standing lamp that I believe may be of interest to you. Please find attached the specifications for your review.

Thank you for your time and consideration.

Sincerely,

Joe
```

</br>

### Format Conversion

```
data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

prompt = f"""
Translate the following python dictionary from JSON to an HTML \
table with column headers and title: {data_json}
"""
response = get_completion(prompt)
print(response)
```
Output:
```
<table>
  <caption>Restaurant Employees</caption>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Shyam</td>
      <td>shyamjaiswal@gmail.com</td>
    </tr>
    <tr>
      <td>Bob</td>
      <td>bob32@gmail.com</td>
    </tr>
    <tr>
      <td>Jai</td>
      <td>jai87@gmail.com</td>
    </tr>
  </tbody>
</table>
```

</br>

### Spellcheck/Grammar Check
```
text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
prompt = f"proofread and correct this review: ```{text}```"
response = get_completion(prompt)
print(response)
```
Output:
```
I got this for my daughter's birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it's super soft and cute. However, one of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. Additionally, it's a bit small for what I paid for it. I think there might be other options that are bigger for the same price. On the positive side, it arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
```



## Section 7: Expanding

ChatGPT can be used to generate customer service emails that are tailored to each customer's review.

```
# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""
```
```
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
response = get_completion(prompt)
print(response)
```

Output:
```
Dear Valued Customer,

Thank you for taking the time to leave a review about our product. We are sorry to hear that you experienced an increase in price and that the quality of the product did not meet your expectations. We apologize for any inconvenience this may have caused you.

We would like to assure you that we take all feedback seriously and we will be sure to pass your comments along to our team. If you have any further concerns, please do not hesitate to reach out to our customer service team for assistance.

Thank you again for your review and for choosing our product. We hope to have the opportunity to serve you better in the future.

Best regards,

AI customer agent
```

We can use the parameter "temperature" to adjust the randomness of the response

```
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
response = get_completion(prompt, temperature=0.7)
print(response)
```

Output:
```
Dear Valued Customer,

Thank you for taking the time to leave a review for our 17 piece system. We are sorry to hear that you were not satisfied with the pricing and quality of the product. We apologize for any inconvenience this may have caused you.

Please know that we take your feedback seriously and will do our best to improve our products and services. If you have any further concerns, please do not hesitate to reach out to our customer service team. They will be more than happy to assist you.

Thank you again for your feedback and for choosing our product. We hope to have the opportunity to serve you better in the future.

Sincerely,

AI customer agent
```


## Section 8: Chatbot

Three roles in the messages
```
1. System: Sets behavior of assistant
2. Assistant: Chat model
3. User: You
```

### Chatbot

Example:
```
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},    
{'role':'user', 'content':'Hi, my name is Isa'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
```
Output: Hi Isa! How can I assist you today?

</br>

Example:
```
messages =  [  
{'role':'system', 'content':'You are friendly chatbot.'},
{'role':'user', 'content':'Hi, my name is Isa'},
{'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
Is there anything I can help you with today?"},
{'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
```
Output:
```
Of course, your name is Isa!
```

</br>

### Orderbot

Automate the collection of user prompt and assistant responses to build a OrderBot.

![](orderbot.png)

Summarize the order as a json format and input to the system

```
{
  "pizza": [
    {
      "type": "pepperoni",
      "size": "large",
      "price": 12.95
    },
    {
      "type": "cheese",
      "size": "medium",
      "price": 9.25
    }
  ],
  "toppings": [
    {
      "type": "extra cheese",
      "price": 2.00
    },
    {
      "type": "mushrooms",
      "price": 1.50
    }
  ],
  "drinks": [
    {
      "type": "coke",
      "size": "large",
      "price": 3.00
    },
    {
      "type": "sprite",
      "size": "small",
      "price": 2.00
    }
  ],
  "sides": [
    {
      "type": "fries",
      "size": "large",
      "price": 4.50
    }
  ],
  "total_price": 35.20
}
```
