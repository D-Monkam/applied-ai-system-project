### What are the limitations or biases in your system?

The system's RAG architecture means its knowledge is limited to the documents in its knowledge base and those uploaded by users. Because the default knowledge base focuses on dogs and cats, there is an inherent bias toward those animal types unless documentation for other animals is provided.

Additionally, the retrieval mechanism uses TF-IDF, which is effective at finding shared keywords but does not have a deep understanding of a query's meaning. This can lead to relevant context being missed. For example, a query about "puppy care" might fail to retrieve a highly relevant document titled "A Guide for Young Canines" if the word "puppy" isn't explicitly mentioned.

### Could your AI be misused, and how would you prevent that?

Yes, the AI could be misused. I can imagine a scenario where someone ignores the platform's primary purpose and tries to use it as a standard chatbot. To prevent this, domain-specific prompting can be implemented. Instructing the AI to only answer questions relating to animal and pet care is a straightforward solution.

### What surprised you while testing your AI's reliability?

While testing, I was surprised by how well the system seemed to perform on my first attempt, passing most of the evaluation tests. The tests were structured to pass if an AI response contained a certain number of keywords.

However, I soon realized the high pass rate was because the AI was simply copying large chunks of text directly from the knowledge base, which was enough to hit the keyword threshold. This led me to refine the prompts to ensure the system was reliable in its answers while also encouraging it to synthesize information rather than just copy and paste it.

### Describe your collaboration with AI during this project.

I used AI (GitHub Copilot) primarily for feature implementation and to evaluate potential ideas. For feature implementation, I was not completely sure how to properly make a call to the Gemini API, so I asked Copilot to draft the code. I then cross-referenced its output with one of the tinker activities from class to ensure it was correct. This process was applied to multiple scenarios, including the UI and the document retrieval system, to ensure the AI's output was meaningful and without issues.

I also fed it ideas and asked it to break them down or compare them against different options. For example, the retrieval system initially worked on a keyword-scoring basis, and I felt there had to be a better way. I asked Copilot for better options, and it recommended TF-IDF, presenting all the benefits and downsides. This was a very helpful suggestion.

One instance where its suggestion was flawed was when I asked what LLM I should use. It suggested Gemini, which I did use, but it specified the `gemini-pro` model instead of `gemini-1.5-flash`. I kept telling it I didn't have access to `pro`, but every time it generated code for a new implementation, it would reference the `pro` model, which I had to correct manually.