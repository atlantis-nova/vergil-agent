# Please cite
Algorithm: **guiding-mechanism**<br>
Author: **Michelangiolo Mazzeschi**<br>
Published: **2nd September 2024**

# Vergil agent: a guiding-mechanism enabled agent (gmA)

This tool is used to create **guiding-mechanism enabled agents (gmA)**: bots that are specialized in guiding the user towards specified goals with minimal interaction required from the devs (the so-called Socratic method). The main problem we are trying to address is that most times, if an agent is programmed to guide the user by asking questions, there might be no end to the depth of the granularity.

Ex. when conducting the Socratic method, a **regular agent** (without any integrated guiding mechanism) programmed to recommend artwork to a customer will ask a neverending set of questions (though below we are going to use fashion, art is an even better example, as it has a tendency to ask for questions endlessly):
```
Bot:    Do you already have an artwork in mind?
User:   not really
Bot:    What kind of art are you drawn to?
User:   Something classical
Bot:    Is there a particular period or style within classical art that interests you?
User:   Greek Art
Bot:    Are you looking for a specific type of Greek art, such as sculptures or pottery?
User:   sculptures',
Bot:    Are you interested in a specific Greek sculptor or a particular mythological theme?
User:   i like depiction of the gods
Bot:    Which god or goddess would you like to see depicted?
User:   Zeus
Bot:    Would you like the sculpture to be a bust, full figure, or a scene depicting Zeus in a specific mythological context?
User:   I prefer full figure'
Bot:    What kind of material would you like the sculpture to be made of?
...
```
Ideally, the agent should be able to reach a conclusion quickly, rather than providing an endless stream of questions.

## Supported LLM providers

- **Groq**

## Instructions




## Supported sub-mechanisms

While we have introduced a **base sub-mechanism**, the original prompting structure can be further tuned to adopt additional sub-mechanism, such as **rush**.

### base

The **base sub-mechanism** is based on a single component:
- **subject_description**
We keep track of whatever the user wishes for updated with the last request. If you look at the clothing description, it gets updated after every interaction with the bot.
- **objectives**
The *list of notions* the agent has to extract from the conversation.

The following is a snapshot of a conversation history that uses this mechanism:
```
[{'user_comment': '',
  'bot_comment': 'Do you already have an clothing in mind?'},
 {'user_comment': 'not really',
  'bot_comment': "What's the occasion you're looking to dress for?"},
 {'user_comment': 'a date',
  'bot_comment': "What's the style you're aiming for? Formal, casual, or something in between?"},
 {'user_comment': 'formal',
  'bot_comment': 'What type of clothing are you thinking of? A suit, a dress, or something else?'},
 {'user_comment': 'i am a woman, a dress',
  'bot_comment': 'Are you looking for a one-piece clothing or a single-piece?'},
 {'user_comment': 'single-piece is ok',
  'bot_comment': "What color are you thinking of for the dress?"},
 {'user_comment': 'red',
  'bot_comment': 'What kind of material would you like the dress to be made of?'},
 {'user_comment': 'cheap, plastic',
  'bot_comment': "Let me summarize, I've got it!"}]
```

### rush

By using the **rush sub-mechanism**, the agent tries to accomplish its goals as quickly as possible, and is based on multiple extra components:
- **iteration**
The question number: it is used to force the agent into reaching the objective as *quickly as possible*.
- **objectives_left**
The *list of notions* the agent has to extract from the conversation. Compared with the base sub-mechanism, we keep track of the remaining ones across the history.
As you can see from the example below, the objectives begin with iteration 1 *"determine clothing type, material, and color"*, and as soon they have been answered by the user, they are removed from the list and no longer considered a priority
- **subject_description**
We keep track of whatever the user wishes for updated with the last request. If you look at the field clothing_description in the example below, you will see that it gets updated after every interaction with vergil.

The following is a snapshot of a conversation history that uses this mechanism:
```
[{'iteration': 0,
  'user_comment': None,
  'bot_comment': 'Do you already know which clothes you want to choose?',
  'objectives_left': None,
  'clothing_description': None},
 {'iteration': 1,
  'user_comment': 'not really',
  'bot_comment': 'What will you be using the clothes for?',
  'objectives_left': 'determine clothing type, material, and color',
  'clothing_description': ''},
 {'iteration': 2,
  'user_comment': 'im going on a date',
  'bot_comment': "For a date, you'll want to make a good impression. Are you looking for something formal or casual?",
  'objectives_left': 'determine clothing type, material, and color',
  'clothing_description': 'date outfit'},
 {'iteration': 3,
  'user_comment': 'formal',
  'bot_comment': 'For a formal date, a suit and tie would be a great choice. What type of clothing are you most interested in? A shirt, trousers, or a full suit?',
  'objectives_left': 'determine clothing type and material, and color',
  'clothing_description': 'formal date outfit'},
 {'iteration': 4,
  'user_comment': 'I am a woman',
  'bot_comment': 'For a formal date, a dress or a skirt and top combination would be a great choice. What type of fabric are you interested in? Silk, cotton...?',
  'objectives_left': 'determine clothing material and color',
  'clothing_description': 'formal date outfit for woman'},
 {'iteration': 5,
  'user_comment': 'cheap plastic is good',
  'bot_comment': 'What color are you thinking of for your formal date outfit?',
  'objectives_left': 'determine clothing color',
  'clothing_description': 'formal date outfit for woman, made of cheap plastic'},
 {'iteration': 6,
  'user_comment': 'red',
  'bot_comment': "Great choice! I think I have a good idea of what you're looking for. Let me summarize: you want a formal date outfit for a woman, made of cheap plastic, and in the color red. Is that correct?",
  'objectives_left': '',
  'clothing_description': 'formal date outfit for woman, made of cheap plastic, red'}]
  ```

After several testing batches, we have noticed that this approach does not provide a remarkable speed improvement, compared to the base sub-mechanims. Said this, it accomplishes its objective of asking only the necessary questions to move forward, while the base mechanism may still ask non-necessary questions once in a while.
