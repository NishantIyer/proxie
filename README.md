Hello there,
we've have made a voice assistant by training it on various nueral networks like GPT-3, Tensorflow, Brainshop AI and Rasa.
the programming language used is python and the entire working principle is based on different APIs
it is trained on over 70 billion nueral cells and parameters and its possiblities are only limited to your imagination.
it is entirely capable of having a full fledged conversation with a human with different modes and tools like grammar correction, factual answering of questions, summarization of the most difficult concepts to a 2ndd grader, codex which can write code based natural language input.
The most prominent application of this is the summarization mode.
This mode is powered by da-vinci-002 engine and can convert extremely long essays or text inputs into summarisies of just a few lines.
Also, we are planning to add the official govt. api's of parliament, constitution and courts which will summarise the sessions taken place in courts into just a few lines. the basic principle is that we'll take the live RSS feed from eg-the hyderabad high court and covert the entire debate or proceedings of the court in text format. this text will be later feeded into gpt-3 model of summarization and it will give out the final verdict etc 
in just a few lines. this can be used by jounalists to keep a track on the cases going on. another example is that it can break the constitution into different sections, acts, bills and can summarize it to even a layman who has no knowledge about law.
these are just a few impilcations of our program, we are planning to add many more such unique functionalities
breaking down the code, it is just of 3 parts
first - voice is extracted from mic and is converted into text using the whisper module of open ai 
second - a request is made to all the api of nueral engines and others and data is extracted from them
third - the text is then converted into speech using gtts 
we have already figured out on making the voice asssistant portable and pocket-sized so that ppl can carry it anywhere.
the components are rasberry pi zero, a small mic and speaker and a esp 8211 wifi chip

# Features :
It is trained on over 75 billion nueral cells so its possiblities are limitless. Here are just a few of them -
- Full fledged conversation with human 
- Huge database of facts, answers and responses
- Summarization (For eg. condensing 12th grade concepts to a 2nd grade child)
- Grammar, GK, Science, Advanced Calculations, Note taking
Intergration of various plugins like - 
- APISetu : Official data of Indian Govt.
- Condensation of Court Sessions into just a few lines : Here, the live RSS feed of tens of pages is extracted and condensed using various algorithms into just a few lines
- News : Addition of APIs from Economic Times, Forbes, NewYork times, Reuters etc 
- Data on various topics like Sports, Finance, Health
