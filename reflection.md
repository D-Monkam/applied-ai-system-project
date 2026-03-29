# PawPal+ Project Reflection

## 1. System Design

- User should be able to add a pet, add tasks, and be able to properly view all tasks added.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- My initial UML design included an `Owner` class containing a `Scheduler` class. The `Scheduler` was designed to hold all tasks, manage the owner's available time, and assign tasks accordingly. Each `Task` had a completion status, and the `Pet` class tracked all pets, along with their dietary and medication needs.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- Yes, my design changed after Copilot pointed out that there wasn't a clear relationship between the `Pet` and `Task` classes. Keeping them separate would have added unnecessary complexity when implementing the prioritization algorithm in the scheduler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- My scheduler considers both time and priority. Time is a given, as a scheduler needs to inform the user when tasks should start. Priority is also essential, as there will always be a measure of importance that needs to be considered, and giving users the ability to assign priority helps them manage these implications.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- The scheduler does not take the duration of tasks into account, at most checking only for an exact time overlap. This is a reasonable tradeoff in this scenario because calculating all overlapping time intervals would require a more complex algorithm. I wanted to keep most of the functions running in linear time if possible.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used AI tools most for building and debugging. Anytime I had an idea in mind, I would give Copilot a prompt that was as specific as possible to generate what I needed. I don't blindly trust what it outputs, so I always make sure to look it over to ensure it's logical. If there were any fallacies, I would debug using inline chat to quickly fix the issues. The most useful prompts were those explaining an issue and a fix, as well as prompts that suggested possible implementations from which I could decide which worked best.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- Copilot initially based its scheduling logic solely on the `time` attribute, which was a misunderstanding of my intent. I had to write a long prompt explaining what I was looking for and how its current thinking was incorrect. I evaluate everything the AI suggests by reviewing it for logical consistency. As a double-check, I would also ask it to do a quick scan of its own suggestions to see if any mistakes were made.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- I tested functionality related to adding and completing tasks, sorting by start time, handling task frequencies (daily, weekly, or once), and conflict detection. These tests are important because they cover the core functionality of the application. To ensure correctness, it's necessary to make sure these core principles are working correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- On a scale of 1 to 5, I'm a 4 in confidence that the scheduler works correctly. It's not a 5, though, since there are many moving parts, and under certain circumstances, things can break. If I had more time, I would test what happens when the owner has 0 minutes of available time, what happens when no pet is scheduled, and how invalid time format inputs are handled.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I'm most satisfied with the system design of the entire application. It's simple yet very effective, and its implementation was straightforward and tight. Even with this system design, I can see it being extended in various ways, such as having a new `Day` class that extends the scheduler beyond just a glorified list.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- I would improve the core logic used for the scheduler. I think the way tasks are laid out and organized could be made more complex with more regard to priority, time, and duration, compared to just priority and time. Also, the presentation of the tasks could look better, rather than just being a top-down list. I'm thinking of a timeline view for the current day.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- I learned that AI doesn't have all the answers. There were times when I fell into pitfalls by trusting the AI too much. I have to constantly be skeptical about what it outputs. For system design, I learned that thinking about that before actually going on with designing the application is the right way to go about development in general.